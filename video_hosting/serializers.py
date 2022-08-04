from rest_framework import serializers
from .models import *
from .models import User
from djoser.serializers import UserCreateSerializer


class UserCreateCustomSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password')





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


# этот сериализатор сделали на занятии от 04.05.2022 (lesson_27)
class CommentsSerializer(serializers.ModelSerializer):
    video = VideoSerializer(many=False)

    class Meta:
        fields = ('id', 'owner', 'video', 'content', 'likes_count')
        model = Comment


class CommentsPutSerializer(serializers.ModelSerializer):
    # video = VideoSerializer(many=False)

    class Meta:
        fields = ('id', 'owner', 'video', 'content', 'likes_count')
        model = Comment


class HashTagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('__all__') # все поля
        model = HashTag


class VideoRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'videos', 'recommendation_name', 'is_top_rated')
        model = VideoRecommendation


class VideoMoreSimplySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('__all__') # все поля
        model = Video


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "name", "subscribers", "owner")
        model = Channel


class UserSubscriptionsSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ("id", "email", "subscriptions")
        model = User