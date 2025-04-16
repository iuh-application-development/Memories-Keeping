import os
import faiss
import torch
import numpy as np
from PIL import Image
import open_clip
import time
from django.conf import settings
from .models import Photo
from .serializers import PhotoCommunitySerializer
from .utils import translate_text

class FaissSearch:
    def __init__(self, user=None):
        self.user = user
        self.device = "cpu"
        
        if user:
            self.index_path = os.path.join(settings.MEDIA_ROOT, f"faiss_index_user_{user.id_user}.bin")
        else:
            self.index_path = os.path.join(settings.MEDIA_ROOT, "faiss_index_global.bin")

        self.model, _, self.preprocess = open_clip.create_model_and_transforms(
            'ViT-L-14', device=self.device, pretrained='datacomp_xl_s13b_b90k'
        )
        self.tokenizer = open_clip.get_tokenizer('ViT-L-14')

        if os.path.exists(self.index_path):
            print(f"✅ FAISS index loaded từ {self.index_path}")
            self.index = faiss.read_index(self.index_path)
        else:
            print(f"⚠️ Không tìm thấy FAISS index tại {self.index_path}, tạo FAISS index mới.")
            self.index = faiss.IndexFlatIP(768)
            self.save_faiss_index()

    def save_faiss_index(self):
        try:
            os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
            faiss.write_index(self.index, self.index_path)
            print(f"✅ FAISS index đã được lưu vào {self.index_path}")
        except Exception as e:
            print(f"❌ Lỗi khi lưu FAISS index: {e}")

    def _extract_features(self, query, mode="text"):
        if mode == "text":
            query = str (translate_text(query,  to_lang='en'))
            print("query: ", query) 
            query = self.tokenizer([query]).to(self.device)
            features = self.model.encode_text(query)
        elif mode == "image":
            query = self.preprocess(Image.open(query).convert("RGB")).to(self.device).unsqueeze(0)
            features = self.model.encode_image(query)
        else:
            raise ValueError("❌ Mode không hợp lệ!")

        features = features / features.norm(dim=-1, keepdim=True)
        return features.cpu().detach().numpy().astype(np.float32)

    def _get_photos_from_indices(self, indices):
        photo_ids = [int(i) for i in indices if i >= 0]
        photos = Photo.objects.filter(
            faiss_id_public__in=photo_ids,
            is_public=True,
            is_deleted=False
        )
        return PhotoCommunitySerializer(photos, many=True).data

    def _get_photos_from_indices_for_user(self, indices):
        photo_ids = [int(i) for i in indices if i >= 0]
        return Photo.objects.filter(
            faiss_id__in=photo_ids,
            album__user=self.user,
            is_deleted=False
        ).values('id_photo', 'photo', 'name', 'description', 'location','tags', 'colors', 'objects_photo','caption', 'is_favorited', 'like_count', 'is_public', 'created_at','updated_at', 'album__id_album', 'album__title', 'album__description', 'album__is_main')

    # 🔥 Tìm kiếm theo user
    def search_for_user(self, query, mode="text", k=5):
        start_time = time.perf_counter()
        print(f"search cho user {self.user}")
        if not self.user:
            raise ValueError("❌ User không hợp lệ!")

        query_features = self._extract_features(query, mode)
        scores, idx_images = self.index.search(query_features, k=k)
        print("scores: ", scores.flatten())
        print("id images: ", idx_images.flatten())

        results = self._get_photos_from_indices_for_user(idx_images.flatten())
        end_time = time.perf_counter()
        print(f"✅ Thời gian model truy xuất bin: {end_time - start_time:.5f} giây")
        return list(results)

    # 🔥 Tìm kiếm toàn cục
    def search_global(self, query, mode="text", k=5):
        start_time = time.perf_counter()
        print("search toàn cục")
        query_features = self._extract_features(query, mode)
        scores, idx_images = self.index.search(query_features, k=k)
        print("id images: ", idx_images.flatten())
        results = self._get_photos_from_indices(idx_images.flatten())
        print("results: ", results)
        # return list(results)
        end_time = time.perf_counter()
        print(f"✅ Thời gian truy xuất bin: {end_time - start_time:.5f} giây")
        return results
