import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from .models import *
from .serializers import *

# initialize the APIClient app
client = Client()


class CheckUnbannTest(TestCase):
    """ Test module for GET all puppies API """

    def setUp(self):
        User.objects.create(
            first_name='Muffin', is_banned=True, email="muffin@gmail.com")

    def test_unbann_user(self):
        # get API response
        muffin = User.objects.get(first_name="Muffin")
        muffin.unbann_user()
        self.assertEqual(muffin.is_banned, False)


class GetPostVideoTest(TestCase):

    def setUp(self) -> None:
        muffin = User.objects.create(
            first_name='Muffin', is_banned=True, email="muffin@gmail.com")

        self.valid_payload = {
            "name": "TestVideo 1",
            "title": "Just test video",
            "user_id": muffin,
            "link": "google.com"
        }

    def test_create_video(self):
        response = client.post("/api/videos/create/", json.dumps(self.valid_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        video_object = Video.objects.get(id=response.data.get("id"))
        serialized_video = VideoSerializer(video_object).data
        self.assertEqual(response.data, serialized_video)

    def test_get_video(self):
        response = client.get("/api/video/")
        videos = Video.objects.all()
        serializer_video = VideoSerializer(videos, many=True).data
        self.assertEqual(response.data, serializer_video)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
