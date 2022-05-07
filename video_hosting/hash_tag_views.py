from rest_framework import generics

from video_hosting.serializers import HashTagSerializer
from video_hosting.models import *


class HashTagListCreateView(generics.ListCreateAPIView):
    serializer_class = HashTagSerializer
    queryset = HashTag.objects.all()


class HasTagListRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HashTagSerializer
    queryset = HashTag.objects.all()
