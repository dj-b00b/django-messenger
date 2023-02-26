from rest_framework import serializers
from messages.models import Message, UserReaction


class UserReactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserReaction
        fields = ('reaction', 'user', 'message', 'time')


class MessageSerializer(serializers.ModelSerializer):
    reactions = serializers.SerializerMethodField(source='get_reactions', read_only=True)

    class Meta:
        model = Message
        fields = ('chat', 'sent_at', 'sender', 'content','is_readed', 'is_editing', 'reactions')

    def get_reactions(self, instance):
        reactions = UserReaction.objects.filter(message_id=instance.pk)
        return UserReactionSerializer(instance=reactions, context=self.context, many=True).data
