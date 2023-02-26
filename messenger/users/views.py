from django.http import Http404
from users.models import User, Contact
from django.shortcuts import get_object_or_404, get_list_or_404
from users.serializers import UserSerializer, ContactSerializer
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, DestroyAPIView
from rest_framework import status
from rest_framework.response import Response


class ShowInfoRemoveChangeDelUser(RetrieveUpdateDestroyAPIView):  
    serializer_class = UserSerializer
    queryset = User.objects.all()


class ShowContactsAddContact(ListCreateAPIView):
    serializer_class = ContactSerializer

    def get_queryset(self):
        user = self.kwargs['user_id']

        obj = get_list_or_404(Contact, user=user)
        return obj

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        curr_user = request.user
        if curr_user.id == kwargs['user_id']:
            return Response({'error': 'Вы не можете добавить сами себя в конткты!'})

        phone_number = request.data.get('phone_number')
        if not User.objects.filter(phone_number=phone_number).exists():
            return Response({
                'error': 'Данный номер телефона не зарегистрирован в мессенджере!'}, status=400)
        
        friend = User.objects.filter(phone_number=request.data.get('phone_number'))
        if Contact.objects.filter(user_id=request.data.get('user'), friend=friend[0]).exists():
            return Response({'error': 'Такой пользователь уже добавлен в контакты!'}, status=400)
        
        friend = User.objects.get(phone_number=request.data.get('phone_number')) 
        Contact.objects.create(
            user = User.objects.get(id=request.data.get('user')),
            name = request.data.get('name'),
            surname = request.data.get('surname'),
            phone_number = request.data.get('phone_number'),
            friend = friend
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        curr_user = request.user
        if curr_user.id != kwargs['user_id']:
            return Response({'error': 'Вы не можете просматривать чужие контакты!'})

        return Response(serializer.data)


class DelContact(DestroyAPIView):

   def get_object(self):
        friend = self.kwargs.get('friend_id')  
        user = self.kwargs.get('user_id')

        obj = get_object_or_404(Contact, friend_id=friend, user_id=user)
        return obj

   def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        curr_user = request.user
        if instance.user != curr_user:
            return Response({'error': 'Вы можете удалять только свои контакты!'}, status=400)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
