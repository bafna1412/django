from rest_framework import generics, permissions

from .serializers import EndUserSerializer, PostSerializer, PhotoSerializer
from .models import EndUser, Post, Photo
from .permissions import PostAuthorCanEditPermission

class EndUserList(generics.ListCreateAPIView):
    model = EndUser
    serializer_class = EndUserSerializer
    permission_classes = [
        permissions.AllowAny
    ]

class EndUserDetail(generics.RetrieveUpdateDestroyAPIView):
    model = EndUser
    serializer_class = EndUserSerializer
    lookup_field = 'username'

class PostMixin(object):
    model = Post
    serializer_class = PostSerializer
    permission_classes = [
        PostAuthorCanEditPermission
    ]

    def pre_save(self, obj):
         """Force author to the current user on save"""
         obj.author = self.request.author
         return super(PostMixin, self).pre_save(obj)

class PostList(PostMixin, generics.ListCreateAPIView):
    pass

   #model = Post
   #serializer_class = PostSerializer
   #permission_classes = [
   #    permissions.AllowAny
   #] Remove PostMixin and then uncomment

class PostDetail(PostMixin, generics.RetrieveUpdateDestroyAPIView):
    pass

   #model = Post
   #serializer_classes = PostSerializer
   #permission_classes = [
   #    permissions.AllowAny
   #]Remove PostMixin and then uncomment

class EndUserPostList(generics.ListAPIView):
    model = Post
    serializer_classes = PostSerializer

    def get_queryset(self):
        queryset = super(EndUserPostList, self).get_queryset()
        return queryset.filter(author__username = self.kwargs.get('username'))

class PhotoList(generics.ListAPIView):
    model = Photo
    serializer_class = PhotoSerializer
    permission_classes = [
        permissions.AllowAny
    ]

class PhotoDetail(generics.RetrieveAPIView):
    model = Photo
    serializer_class = PhotoSerializer
    permission_classes = [
        permissions.AllowAny
    ]
class PostPhotoList(generics.ListAPIView):
    model = Photo
    serializer_class = PhotoSerializer

    def get_queryset(self):
        queryset = super(PostPhotoList, self).get_queryset()
        return queryset.filter(post__pk = self.kwargs.get('pk'))


    
