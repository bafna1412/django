# This is the admin file. Here you can register your database models with the admin interface

from django.contrib import admin
from .models import EndUser, Post, Photo

class EndUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'posts')

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('post', 'image')

admin.site.register(EndUser, EndUserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Photo, PhotoAdmin)
