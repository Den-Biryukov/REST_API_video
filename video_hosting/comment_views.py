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
        comment_sirialized = CommentsSerializer(comment).data
        return Response(comment_sirialized)

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
            return Response({'message': 'oops! 404 <>_<>.This comment does not exist'},
                            status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Method DELETE not allowed'})

        try:
            instance = Comment.objects.get(id=pk)
            instance.delete()
        except:
            return Response({'error': 'Object not found'})

        return Response({'post': 'delete comment ' + str(pk)})


    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Method PUT not allowed'})

        try:
            instance = Comment.objects.get(pk=pk)
        except:
            return Response({'error': "Object doesn't exists"})

        serializer = CommentsSerializer(data=request.data, instance=instance) # когда прописано два аргумента data и instance, у сериалайзера автоматически вызовется метод update, который прописан в serializes.py
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'post': serializer.data})
