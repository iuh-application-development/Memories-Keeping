from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Photo)
admin.site.register(Album)
admin.site.register(Trash)
admin.site.register(Favorite)
admin.site.register(Search_history)
# admin.site.register(Search_rating)
# admin.site.register(Filter)
admin.site.register(Like)
admin.site.register(Avatar)
admin.site.register(Comment)