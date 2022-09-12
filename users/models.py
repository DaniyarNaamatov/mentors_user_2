from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
import jwt
from phonenumber_field.modelfields import PhoneNumberField
from datetime import datetime, timedelta
from django.conf import settings


class MyUserManager(BaseUserManager):
    def _create_user(self, email, username, password, phone, **extra_fields):
        if not email:
            raise ValueError("Вы не ввели Email")
        if not username:
            raise ValueError("Вы не ввели Логин")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            phone=phone,
            **extra_fields,
        )
        if user.is_superuser:
            self.model(
                email=self.normalize_email(email),
                username=username,
                phone=username,
                **extra_fields,
            )
            user.set_password(password)
            user.save(using=self._db)
            return user
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, phone, password):
        return self._create_user(email, username, phone, password)

    def create_superuser(self, email, username, password, phone=None):
        if UserApiBack.is_superuser:
            phone = username
        return self._create_user(
            email, username, password, phone, is_staff=True, is_superuser=True
        )



class UserApiBack(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True, unique=True)  # Идентификатор
    username = models.CharField(max_length=50, unique=True)  # Логин
    email = models.EmailField(max_length=100, unique=True)  # Email
    phone = PhoneNumberField(unique=True)
    is_active = models.BooleanField(default=True)  # Статус активации
    is_staff = models.BooleanField(default=False)  # Статус админа

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["username", "email"]

    objects = MyUserManager()

    def __str__(self):
        return str(self.phone)

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        """
        Генерирует веб-токен JSON, в котором хранится идентификатор этого
        пользователя, срок действия токена составляет 1 день от создания
        """
        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode({
            'id': self.pk,
            'exp': dt.strftime('%S')
        }, settings.SECRET_KEY, algorithm='HS256')

        return token