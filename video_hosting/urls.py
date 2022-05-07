from django.urls import path

from video_hosting.comment_views import CommentView
from video_hosting.views import *
from video_hosting.hash_tag_views import *
from .hash_tag_views import HasTagListRetrieveUpdateDeleteView, HashTagListCreateView


# Video
urlpatterns = [
    path('videolist/', VideoAPIView.as_view()),
    path('videolistput/<int:pk>', VideoAPIView.as_view()),
    path('videolist/<int:pk>', VideoSpecificAPIView.as_view()),
    # path('commentlist/', CommentAPIView.as_view()),
]

# Comments
urlpatterns += [
    path('comment/create/', CommentView.as_view()),
    path('comment/get/<int:pk>', CommentView.as_view()),
    path('comment/get', CommentView.as_view())
]

# hash tag
urlpatterns += [
    path('hashtag/', HashTagListCreateView.as_view()),
    path('hashtag/<int:pk>', HasTagListRetrieveUpdateDeleteView.as_view())
]