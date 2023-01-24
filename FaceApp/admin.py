from django.contrib import admin
from .models import User
from django.utils.html import mark_safe


@admin.register(User)

class UserAdmin(admin.ModelAdmin):
    list_display = ['email','image_tag','uid']
    def image_tag(self,object):
        return mark_safe(f'<img src="/media/{object.image}" width="100" height="100"/>')