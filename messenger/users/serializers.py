from rest_framework import serializers
from users.models import User, Contact


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'about_user', 'phone_number', 'avatar')


class ContactSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Contact
        read_only_fields = ['friend']  
        fields = ('user', 'name', 'surname', 'phone_number', 'friend')  



