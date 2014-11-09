from django.conf.urls import patterns, url, include

from .api import EndUserList, EndUserDetail
from .api import PostList, PostDetail, EndUserPostList
from .api import PhotoList, PhotoDetail, PostPhotoList

enduser_urls = patterns('',
                        # url(r'^/(?P<username>[0-9a-zA-Z_-]+)/feed$', EndUserFeed.as_view(), name='enduserpost-feed'),
                        url(r'^/(?P<username>[0-9a-zA-Z_-]+)/posts$', EndUserPostList.as_view(), name='enduserpost-list'),
                        url(r'^/(?P<username>[0-9a-zA-Z_-]+)$', EndUserDetail.as_view(), name='enduser-detail'),
                        url(r'^$', EndUserList.as_view(), name='enduser-list')
)

post_urls = patterns('',
                     url(r'^/(?P<pk>\d+)/photos$', PostPhotoList.as_view(), name='postphoto-list'),
                     url(r'^/(?P<pk>\d+)$', PostDetail.as_view(), name='post-detail'),
                     url(r'^$', PostList.as_view(), name='post-list')
)

photo_urls = patterns('',
                      url(r'^/(?P<pk>\d+)$', PhotoDetail.as_view(), name='photo-detail'),
                      url(r'^$', PhotoList.as_view(), name='photo-list')
)

urlpatterns = patterns('',
                       url(r'^endusers', include(enduser_urls)),
                       url(r'^posts', include(post_urls)),
                       url(r'^photos', include(photo_urls)),
)
