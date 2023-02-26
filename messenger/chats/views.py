from chats.serializers import ChatSerializer, ChatMemberSerializer
from chats.models import Chat, ChatMember
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, DestroyAPIView, UpdateAPIView
from django.shortcuts import render
from django.views.decorators.http import require_GET
from users.models import User
from chats.tasks import send_admin_email


@require_GET
def render_home_page(request):
    return render(request, 'home.html')


def login(request):
    return render(request, 'login.html')


def my_login_required(func):
    def wrapper(*args, **kwargs):
        try:
            request = args[1]

        except IndexError:
            request = args[0]

        finally:
            if request.user.is_anonymous:
                return login(request)

        return func(*args, **kwargs)

    return wrapper


class ShowChatsCreateChat(ListCreateAPIView):
    serializer_class = ChatSerializer

    def get_queryset(self):
        # user = self.request.user
        user = 1
        chat_members = ChatMember.objects.filter(user_id = 1) # user.id было

        detail_chats = [Chat.objects.get(id=chat_member.chat_id) for chat_member in chat_members]
        return detail_chats

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if 'users' not in request.data:
            return Response({'error': 'users - обязательное поле'}, status=400)

        if request.data['users'] == '':
            return Response({'error': 'в поле users ничего не передано!'}, status=400)

        if not isinstance(request.data['users'], list):
            return Response({'error': 'поле users не является типом list'}, status=400)
        lst_users_id = request.data['users']

        self.perform_create(serializer)

        chat = Chat.objects.all().last()
        creator = request.data['creator']
        category = request.data['category']

        if category == 2 and len(lst_users_id) > 2:
            return Response({'error': 'Вы не можете создать личный чат более чем на 2 участника'}, status=400)

        prepare_users = []
        for user_id in lst_users_id:
            user = get_object_or_404(User, id=user_id)
            prepare_users.append(
                ChatMember(
                    user_id=user.id,
                    chat_id=chat.id,
                    is_admin=True if creator == user.id and category == 1 else False
                ))
        ChatMember.objects.bulk_create(prepare_users)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ShowEditDeleteChat(RetrieveUpdateDestroyAPIView):
    serializer_class = ChatSerializer
    queryset = Chat.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        chat = kwargs['pk']
        user = get_object_or_404(
            ChatMember, user_id=request.user.id, chat_id=chat)
        if user.is_admin == False:
            return Response({'error': 'Чтобы удалить чат, нужно быть администратором!'}, status=400)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShowChatMembersAddChatMember(ListCreateAPIView):
    serializer_class = ChatMemberSerializer

    def get_queryset(self):
        chat = self.kwargs['pk']

        obj = get_list_or_404(ChatMember, chat_id=chat)
        return obj

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.data.get('user')
        chat_id = request.data.get('chat')
        if ChatMember.objects.filter(user_id=user, chat_id=chat_id).exists():
            return Response({'error': 'Указанный пользователь уже добавлен в чат!'}, status=400)

        category = Chat.objects.get(id=chat_id).category.id
        count_users_chat = ChatMember.objects.filter(chat=chat_id)
        if category == 2 and len(count_users_chat) >= 2:
            return Response({'error': 'В личном чате не может состоять больше двух участников!'}, status=400)

        curr_user = get_object_or_404(ChatMember, user_id=user, chat_id=chat_id)
        if curr_user.is_admin == False:
            return Response({'error': 'Чтобы добавить пользователя в чат, нужно быть администратором!'}, status=400)

        self.perform_create(serializer)
       
        admins = ChatMember.objects.filter(chat_id=chat_id, is_admin=True)
        if admins.exists():
            list_emails_admins = [User.objects.get(id=admin.user_id).email for admin in admins]
            send_admin_email.apply_async(
                kwargs={
                    'subject': 'New chat member added',
                    'message': 'Hey, a new user has been added to the chat', 
                    'email_admins': list_emails_admins
                    })

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class DelChatMember(DestroyAPIView):
    serializer_class = ChatMemberSerializer
    queryset = ChatMember.objects.all()

    def get_object(self):
        user = self.kwargs['user_id']
        chat = self.kwargs['chat_id']

        obj = get_object_or_404(ChatMember, user_id=user, chat_id=chat)
        return obj

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        chat = kwargs['chat_id']
        curr_user = get_object_or_404(
            ChatMember, user_id=request.user.id, chat_id=chat)
        if curr_user.is_admin == False:
            return Response({'error': 'Чтобы удалять пользователей из чата, нужно быть администратором!'}, status=400)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddRemoveAdmin(UpdateAPIView):
    serializer_class = ChatMemberSerializer

    def get_object(self):
        user = self.kwargs['user_id']
        chat = self.kwargs['chat_id']

        obj = get_object_or_404(ChatMember, chat_id=chat, user_id=user)
        return obj

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        chat = self.kwargs['chat_id']
        curr_user = get_object_or_404(ChatMember, user_id=request.user.id, chat_id=chat)
        if curr_user.is_admin == False:
            return Response({'error': 'Чтобы добавлять и удалять администраторов в чат, нужно быть администратором!'}, status=400)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


