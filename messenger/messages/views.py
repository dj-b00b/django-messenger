from django.http import Http404
from messages.models import Message, UserReaction
from django.shortcuts import get_object_or_404, get_list_or_404
from messages.serializers import MessageSerializer, UserReactionSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
from messages.tasks import publish_message
from django.shortcuts import render



class EditDeleteMessage(UpdateAPIView, DestroyAPIView):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        curr_user = request.user
        chat = kwargs['pk']
        message = Message.objects.get(id=chat)
        if message.sender != curr_user:
            return Response({'error': 'Вы не можете удалить чужое сообщение!'}, status=400)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        curr_user = request.user
        chat = kwargs['pk']
        message = Message.objects.get(id=chat)
        if message.sender != curr_user:
            return Response({'error': 'Вы не можете редактировать чужое сообщение!'}, status=400)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class ShowMessagesCreateMessage(ListCreateAPIView):  
    serializer_class = MessageSerializer

    def get_queryset(self):
        chat = self.kwargs['pk']
        
        obj = get_list_or_404(Message, chat_id=chat)
        return obj


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        publish_message.delay(serializer.data)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


def messages(request):
    return render(request, 'index.html')


class AddReaction(CreateAPIView): 
    serializer_class = UserReactionSerializer
    queryset = UserReaction.objects.all()  

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.data.get('user')
        message = request.data.get('message')
  
        if UserReaction.objects.filter(message_id=message, user_id=user).exists():
            return Response({'error': 'Вы уже поставили реакцию!'}, status=400)
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UpdateDeleteReaction(UpdateAPIView, DestroyAPIView):   
   serializer_class = UserReactionSerializer

   def get_object(self):
        message = self.kwargs.get('message_id')  
        user = self.kwargs.get('user_id')

        obj = get_object_or_404(UserReaction, message_id=message, user_id=user)
        return obj
    
   def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        curr_user = request.user
        if curr_user != instance.user: 
            return Response({'error': 'Вы не можете удалить чужую реакцию'}, status=400)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

   def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        curr_user = request.user
        if curr_user != instance.user: 
            return Response({'error': 'Вы не можете изменить чужую реакцию'}, status=400)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

