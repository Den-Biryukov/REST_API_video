from django.urls import path

from video_hosting.comment_views import *
from video_hosting.video_views import *
from video_hosting.channel_subs_views import *
from video_hosting.hash_tag_views import *
from .hash_tag_views import HasTagListRetrieveUpdateDeleteView, HashTagListCreateView
from .usersviews import ListUsersView

# Video
urlpatterns = [
    path('videolist/', VideoAPIView.as_view()),
    path('videolistput/<int:pk>', VideoAPIView.as_view()),
    path('videolist/<int:pk>', VideoSpecificAPIView.as_view()),
    # path('commentlist/', CommentAPIView.as_view()),
]

# Video more simply decision
urlpatterns += [
    path('video/', VideoListCreateView.as_view()),
    path('video/<int:pk>', VideoListRetrieveUpdateDeleteView.as_view())
]

# Comments
urlpatterns += [
    path('comment/create/', CommentView.as_view()),
    path('comment/get/<int:pk>', CommentView.as_view()),
    path('comment/get', CommentView.as_view()),
    path('comment/delete/<int:pk>', CommentView.as_view()),
    path('comment/update/<int:pk>', CommentPutView.as_view())
]

# Hash tag
urlpatterns += [
    path('hashtag/', HashTagListCreateView.as_view()),
    path('hashtag/<int:pk>', HasTagListRetrieveUpdateDeleteView.as_view())
]

urlpatterns += [
    path('users/', ListUsersView.as_view())
]

# subcriptions
urlpatterns += [
    path("subscribe/", ChannelSubscribeView.as_view()),
]

urlpatterns += [
    path("export/comments/", ExportMyCommentsView.as_view())
]