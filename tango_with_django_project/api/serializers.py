from rest_framework import serializers
from .models import EndUser, Post, Photo

#Create your serializers here

class EndUserSerializer(serializers.ModelSerializer):
    posts = serializers.HyperlinkedIdentityField('posts', view_name = 'enduserpost-list', lookup_field = 'username')

    class Meta:
        model = EndUser
        fields = ('id', 'username', 'first_name', 'last_name', 'posts', )

class PostSerializer(serializers.ModelSerializer):
    author = EndUserSerializer(required = False)
    photos = serializers.HyperlinkedIdentityField('photos', view_name = 'postphoto-list')
    # author = serializers.HyperlinkedRelatedField(view_name='user-detail', lookup_field='username')

    def get_validation_exclusions(self):
        # Need to exclude `author` since we'll add that later based off the request
        exclusions = super(PostSerializer, self).get_validation_exclusions()
        return exclusions + ['authors']

    class Meta:
        model = Post

class PhotoSerializer(serializers.ModelSerializer):
    image = serializers.Field('image.url')

    class Meta:
        model = Photo
