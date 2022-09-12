from rest_framework import serializers
from .models import UserApiBack
from django.contrib.auth import authenticate


class UserRegisterSerializersBackend(serializers.ModelSerializer):
    password2 = serializers.CharField()

    class Meta:
        model = UserApiBack
        fields = ["email", "username", "phone", "password", "password2"]

    def save(self, *args, **kwargs):
        user = UserApiBack(
            email=self.validated_data["email"],
            username=self.validated_data["username"],
            phone=self.validated_data["phone"],
        )
        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]
        if password != password2:
            raise serializers.ValidationError({password: "Пароль не совпадает"})
        user.set_password(password)
        user.save()
        return user


class LoginSerializersBackend(serializers.Serializer):
    phone = serializers.CharField()
    username = serializers.CharField(max_length=255, read_only=True, required=False)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        phone = data.get("phone", None)
        password = data.get("password", None)

        if phone is None:
            raise serializers.ValidationError("A phone number is required to log in.")

        if password is None:
            raise serializers.ValidationError("A password is required to log in.")

        user = authenticate(phone=phone, password=password)

        if user is None:
            raise serializers.ValidationError("A user was not found.")

        if not user.is_active:
            raise serializers.ValidationError("This user has been deactivated.")
        return {
            "phone": user.phone,
            "token": user.token,
        }