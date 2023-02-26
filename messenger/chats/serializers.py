from rest_framework import serializers
from chats.models import Chat, ChatMember
from users.models import User


class ChatMemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChatMember
        fields = ('id', 'is_admin', 'adding_time', 'user', 'chat')
        read_only_fields = ['adding_time']


class ChatSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField(source='get_users')
    admins = serializers.SerializerMethodField(source='get_admins')  
    class Meta:
        model = Chat
        fields = ('title', 'description', 'creator','category', 'users', 'admins')
    
    def get_users(self, instance):    
        members = ChatMember.objects.filter(chat_id=instance.pk).select_related('user') 
        users = [member.user for member in members]
        return ChatUserSerializer(instance=users, context=self.context, many=True).data

    def get_admins(self, instance):
        members = ChatMember.objects.filter(chat_id=instance.pk, is_admin=True).select_related('user')
        admins = [member.user for member in members]
        return ChatUserSerializer(instance=admins, context=self.context, many=True).data
        

class ChatUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'avatar')   
