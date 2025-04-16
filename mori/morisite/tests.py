# from django.test import TestCase

# Create your tests here.


# {
#     "user_id": 1,
# 	"albums": [
#         {
#             "title": "Holiday Album",
#             "description": "Photos from my holiday trip."
#         },
#         {
#             "title": "Holiday Album",
#             "description": "Photos from my holiday trip."
#         }
#     ]
# }

# from pathlib import Path
# from datetime import timedelta
# import os
# BASE_DIR = Path(__file__).resolve().parent.parent
# MEDIA_URL = '/moriste/static/img/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'moriste', 'static', 'img')
# print(MEDIA_ROOT)

# import os
# import django
# from django.utils import timezone
# import pytz

# # Cấu hình Django settings nếu chưa có
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mori.settings')  # Thay 'mori.settings' bằng module settings của bạn
# django.setup()  # Khởi tạo Django

# # Lấy giờ Việt Nam
# vietnam_tz = pytz.timezone("Asia/Ho_Chi_Minh")
# vietnam_time = timezone.now().astimezone(vietnam_tz)
# print(vietnam_time)


import torch
print("CUDA available:", torch.cuda.is_available())
print("CUDA device count:", torch.cuda.device_count())
print("Current CUDA device:", torch.cuda.current_device())
print("CUDA device name:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "No CUDA device")
