from django.contrib import admin
from .models import Post, Profile


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = ()


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)