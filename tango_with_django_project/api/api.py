from rest_framework import generics, permissions
from django.http import HttpResponse, HttpResponseServerError

from .serializers import EndUserSerializer, PostSerializer, PhotoSerializer
from .models import EndUser, Post, Photo
from .permissions import PostAuthorCanEditPermission

import redis

# class EndUserFeed(generics.ListAPIView):
#    model = EndUser
#    serializer_class = EndUserSerializer
#    lookup_field = 'username'
#    permission_classes = [
#        permissions.AllowAny
#    ]
   
     # Getting list of followers and their posts for a user
    # followers = []
#    posts = {}
    # followers = EndUser.objects.get(followers)
    # posts.update(EndUser.objects.all())
    # feed = {"posts": posts}

    # Now push the collected posts on site
#    r = redis.StrictRedis(host = 'localhost', port = 6379, db = 0)
#    r.publish('feed', Post.objects.all())

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


    
