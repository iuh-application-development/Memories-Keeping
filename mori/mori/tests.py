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

import os
from pathlib import Path
from datetime import timedelta
import os
BASE_DIR = Path(__file__).resolve().parent.parent

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
print(MEDIA_ROOT)