from django.shortcuts import render
from rest_framework import generics

from rest_framework.views import APIView
from rest_framework.response import Response
from django.forms import model_to_dict

from .models import *
from .serializers import *


# class VideoAPIView(generics.ListAPIView):
#     queryset = Video.objects.all()
#     serializer_class = VideoSerializer


#---------------------
# ДЗ урок 25-26 от 27.04.2022: три эндпоинта на получение конкретного видео,
# получение всех видео и создание видео, плюс по возможности добавление коммента к видео
# пробую реализовать примитивным образом по видео selfedu №3 без сериализаторов,
# что-то получилось, добавил часть из 4 видео, что-то получилось, добавил часть из 5 видео:

class VideoAPIView(APIView):
    def get(self, request):
        videos = Video.objects.all()
        '''если рабоатем без сериалайзера и в Responce используем 
        many_to_dcit и будет просто Video.objects.all(), то ошибка,
        т.к. нам нужен не QuerySet, а набор конкретных значений'''
        return Response({'videos': VideoSerializer(videos, many=True).data}) # many=True говорит о том, что сериализатор должен обрабатывать не одну какую-то запись, а список записей, и, соответственно, выдавать тоже список этих записей

    def post(self, request):
        serializer = VideoSerializer(data=request.data)  # создаём сериализатор, на основе тех данных, которые поступили с пост запроса
        serializer.is_valid(raise_exception=True)  # проверяем корректность принятых данных
        serializer.save()
        # post_new = Video.objects.create(
        #     name=request.data['name'],
        #     title=request.data['title'],
        #     link=request.data['link']
        # )
        # return Response({'post': VideoSerializer(post_new).data})
        return Response({'post': serializer.data})

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Method PUT not allowed'})

        try:
            instance = Video.objects.get(pk=pk)
        except:
            return Response({'error': "Object doesn't exists"})

        serializer = VideoSerializer(data=request.data, instance=instance) # когда прописано два аргумента data и instance, у сериалайзера автоматически вызовется метод update, который прописан в serializes.py
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'post': serializer.data})

    # помиомо get и post запроссов, есть ещё put, patch, delete, и, думаю, это не все

class VideoSpecificAPIView(APIView):
    def get(self, request, pk):
        video = Video.objects.filter(id=pk)
        '''если рабоатем без сериалайзера и в Responce используем 
        many_to_dcit и будет просто Video.objects.all(), то ошибка,
        т.к. нам нужен не QuerySet, а набор конкретных значений'''
        return Response({'videos': VideoSerializer(video, many=True).data})


#TODO: хм, что-то не получилось, попробую вернуться к этому позже, или спрошу у Антона
class CommentAPIView(APIView):
    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # post_new = Comment.objects.create(
        #     video=request.data['video'],
        #     content=request.data['content']
        # )
        # return Response({'post': CommentSerializer(post_new).data})
        return Response({'post': serializer.data})
        '''model_to_dict(post_new) было вместо CommentSerializer(post_new).data,
         которое было вместо serializer.data :) -
        стандартная джанговская функция, 
        преобразовывает объект класса Video в словарь'''
# ---------------------
