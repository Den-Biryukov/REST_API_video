from rest_framework import generics
from rest_framework.views import APIView

from video_hosting.pagination import HashTagPagination
from video_hosting.serializers import HashTagSerializer
from video_hosting.models import *


class HashTagListCreateView(generics.ListCreateAPIView):
    serializer_class = HashTagSerializer
    queryset = HashTag.objects.all()
    pagination_class = HashTagPagination


class HasTagListRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HashTagSerializer
    queryset = HashTag.objects.all()

    # Тупо пример был
    # def get_queryset(self):
    #     id = self.kwargs['id']
    #     hash_tags = HashTag.objects.filter(id=id)
    #     return hash_tags
