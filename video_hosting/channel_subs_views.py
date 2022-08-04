from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from video_hosting.models import Channel, User

from requests import Response

from video_hosting.serializers import UserSubscriptionsSerializer, ChannelSerializer


@permission_classes((IsAuthenticated,))
class ChannelSubscribeView(APIView):

    def post(self, request):
        channel_id = request.data.get('channel_id')
        channel = Channel.objects.get(id=channel_id)
        subscriber = User.objects.get(id=request.user.id)
        subscriber.subscriptions.add(channel)
        subscriber.save()
        serialized = UserSubscriptionsSerializer(subscriber).data
        return Response(serialized)

    def get(self, request, pk):
        channel = Channel.objects.get(id=pk)
        serialized = ChannelSerializer(channel).data
        return Response(serialized)
