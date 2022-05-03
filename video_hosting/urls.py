from django.urls import path

from video_hosting.views import *

urlpatterns = [
    path('videolist/', VideoAPIView.as_view()),
    path('videolistput/<int:pk>', VideoAPIView.as_view()),
    path('videolist/<int:pk>', VideoSpecificAPIView.as_view()),
    path('commentlist/', CommentAPIView.as_view()),
]
