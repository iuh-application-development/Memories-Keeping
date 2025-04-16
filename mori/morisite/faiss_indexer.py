import os
import torch
import faiss
import numpy as np
from PIL import Image
import open_clip
from django.conf import settings
from .models import Photo
import time

class FaissImageIndexer:
    def __init__(self, user=None):
        self.device = "cpu"
        self.feature_dim = 768
        self.user = user
        self.index = self.load_faiss_index()

        # Load model và tokenizer của OpenCLIP
        self.model, _, self.preprocess = open_clip.create_model_and_transforms(
            'ViT-L-14', device=self.device, pretrained='datacomp_xl_s13b_b90k'
        )
        self.tokenizer = open_clip.get_tokenizer('ViT-L-14')

    @property
    def faiss_index_path(self):
        if self.user:
            file_name = f"faiss_index_user_{self.user.id_user}.bin"
        else:
            file_name = "faiss_index_global.bin"
        return os.path.join(settings.MEDIA_ROOT, file_name)

    def create_faiss_index(self):
        """Tạo FAISS Index mới"""
        print(f"⚠️ Tạo mới FAISS Index tại {self.faiss_index_path}")
        index = faiss.IndexFlatIP(self.feature_dim)
        self.save_faiss_index(index)  # ✅ Đảm bảo FAISS được lưu trước khi thêm dữ liệu
        time.sleep(0.5)  # ✅ Chờ FAISS hoàn thành lưu trước khi sử dụng
        return index

    def load_faiss_index(self):
        """Tải hoặc tạo FAISS index riêng cho từng user hoặc global"""
        try:
            if os.path.exists(self.faiss_index_path):
                print(f"✅ FAISS index loaded từ {self.faiss_index_path}")
                return faiss.read_index(self.faiss_index_path)
            else:
                # 🔥 Tự động tạo mới FAISS nếu không tồn tại
                print(f"⚠️ Không tìm thấy {self.faiss_index_path}, tạo FAISS index mới.")
                return self.create_faiss_index()
        except Exception as e:
            print(f"❌ Lỗi khi tải FAISS index: {e}")
            return self.create_faiss_index()

    def save_faiss_index(self, index):
        """Lưu FAISS index vào file"""
        try:
            os.makedirs(os.path.dirname(self.faiss_index_path), exist_ok=True)
            faiss.write_index(index, self.faiss_index_path)
            print(f"✅ FAISS index đã được lưu vào {self.faiss_index_path}")
        except Exception as e:
            print(f"❌ Lỗi khi lưu FAISS index: {e}")

    def extract_image_features(self, image_path):
        """Trích xuất đặc trưng ảnh"""
        try:
            if not os.path.exists(image_path):
                print(f"❌ Ảnh không tồn tại: {image_path}")
                return None

            image = Image.open(image_path).convert("RGB")
            image_input = self.preprocess(image).to(self.device).unsqueeze(0)

            with torch.no_grad():
                image_features = self.model.encode_image(image_input)

            image_features /= image_features.norm(dim=-1, keepdim=True)
            return image_features.cpu().detach().numpy().astype(np.float32)
        except Exception as e:
            print(f"❌ Lỗi khi trích xuất đặc trưng ảnh: {e}")
            return None

    def add_photo_to_faiss(self, photo):
        try:
            if not os.path.exists(photo.photo.path):
                print(f"❌ Ảnh không tồn tại: {photo.photo.path}")
                return False

            feature_vector = self.extract_image_features(photo.photo.path)
            if feature_vector is None:
                print(f"⚠️ Ảnh {photo   .id_photo} không thể trích xuất đặc trưng.")
                return False

            # ✅ Chỉ tạo FAISS mới nếu hoàn toàn chưa tồn tại
            if self.index is None:
                print(f"⚠️ FAISS chưa tồn tại → Tạo FAISS mới")
                self.index = faiss.IndexFlatIP(feature_vector.shape[1])
                self.index.add(feature_vector)
                faiss_id = self.index.ntotal - 1
            else:
                # ✅ Kiểm tra kích thước vector trước khi ghi vào FAISS
                if feature_vector.shape[1] != self.index.d:
                    print(f"❌ Kích thước vector của ảnh {photo.id_photo} ({feature_vector.shape[1]}) "
                        f"không khớp với FAISS ({self.index.d}) → Bỏ qua ảnh này.")
                    return False
                
                faiss_id = self.index.ntotal
                self.index.add(feature_vector)

            if self.user is None:
                print(f"FAISS index global: {faiss_id}")
                photo.faiss_id_public = faiss_id
            else:
                print(f"FAISS index user {self.user.id_user}: {faiss_id}")
                photo.faiss_id = faiss_id
            photo.save()
            if photo.faiss_id is None:
                raise ValueError(f"❌ Không thể cập nhật faiss_id cho ảnh {photo.id_photo}")

            # ✅ Lưu lại FAISS index sau khi thêm ảnh mới
            self.save_faiss_index(self.index)
            time.sleep(0.5)  # Đảm bảo FAISS đã được lưu

            print(f"✅ Ảnh {photo.id_photo} đã được thêm vào FAISS với ID: {faiss_id}")
            return faiss_id

        except Exception as e:
            print(f"❌ Lỗi khi thêm ảnh vào FAISS: {e}")
            return False
