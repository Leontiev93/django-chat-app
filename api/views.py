
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import HttpResponseRedirect

from users.models import User
from .serializers import (
    ConversationListSerializer,
    ConversationSerializer,
    UserSerializer)
from chat.models import Conversation


@api_view(['GET'])
def get_conversation(request, convo_id):
    conversation = Conversation.objects.filter(id=convo_id)
    if not conversation.exists():
        return Response({'message': 'Conversation does not exist'})
    else:
        serializer = ConversationSerializer(instance=conversation[0])
        return Response(serializer.data)


@api_view(['POST'])
def start_convo(request, ):
    data = request.data
    print(data)
    username = data.pop('username')
    try:
        participant = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({'message': 'You cannot chat with a non existent user'})
    conversation = Conversation.objects.filter(Q(initiator=request.user, receiver=participant) |
                                               Q(initiator=participant, receiver=request.user))
    if conversation.exists():
        x = args=(conversation[0].id)
        print(x)

        return redirect(reverse('get_conversation', args=(conversation[0].id,)))
    else:
        conversation = Conversation.objects.create(initiator=request.user, receiver=participant)
        return Response(ConversationSerializer(instance=conversation).data)


@api_view(['GET'])
def conversations(request):
    conversation_list = Conversation.objects.filter(Q(initiator=request.user) |
                                                    Q(receiver=request.user))
    print("1111111")
    print(conversation_list)
    serializer = ConversationListSerializer(instance=conversation_list, many=True)
    print(serializer.data)
    return Response(serializer.data)


@api_view(['GET'])
def user_list(request, ):
    users = User.objects.all().order_by('username')
    serializer = UserSerializer(instance=users, many=True)
    return Response(serializer.data)
