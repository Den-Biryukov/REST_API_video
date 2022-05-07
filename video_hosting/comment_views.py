from .models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CommentsSerializer

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status


class CommentView(APIView):

    def post(self, request):
        video_id = request.data.get('video')
        content = request.data.get('content')
        video = Video.objects.get(id=video_id)
        comment = Comment.objects.create(video=video, content=content)
        comment_sirealized = CommentsSerializer(comment).data
        return Response(comment_sirealized)

    def get(self, request, pk=None):
        try:
            if not pk:
                comments = Comment.objects.all()
                comment_serialized = CommentsSerializer(comments, many=True).data
                return Response(comment_serialized)
            comment = Comment.objects.get(id=pk)
            comment_serialized = CommentsSerializer(comment).data
            return Response(comment_serialized)
        except ObjectDoesNotExist as e:
            return Response({'message': 'oops! 404 <>_<>'}, status=status.HTTP_404_NOT_FOUND)

