from rest_framework import serializers

class SignupRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8)


class SignupResponseSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()


class LoginRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class SendFriendRequestSerializer(serializers.Serializer):
    to_user_id = serializers.IntegerField()

class RespondFriendRequestSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=['accepted', 'rejected'])