from rest_framework import serializers
from .models import *

# Написали этот небольшой сериализатор на уроке с Антоном
# class VideoSerializer(serializers.ModelSerializer):
#     class Meta:
#         fields = ('id', 'name', 'likes_count', 'user', 'comments', 'title', 'link')
#         model = Video
#--------------------

class VideoSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    title = serializers.CharField(max_length=255, default='Empty')
    uploaded = serializers.DateTimeField(read_only=True)
    likes_count = serializers.IntegerField(default=0)
    user = serializers.CharField(allow_blank=True, allow_null=True, read_only=True)
    link = serializers.URLField()

    def create(self, validated_data):
        return Video.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.title = validated_data.get('title', instance.title)
        instance.likes_count = validated_data.get('likes_count', instance.likes_count)
        instance.user = validated_data.get('user', instance.user)
        instance.link = validated_data.get('link', instance.link)
        instance.save()
        return instance



class CommentSerializer(serializers.Serializer):
    owner = serializers.CharField(allow_blank=True, allow_null=True, read_only=True)
    video = serializers.CharField()
    content = serializers.CharField
    likes_count = serializers.IntegerField(default=0)

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)