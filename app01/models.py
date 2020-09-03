from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, username=None, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )

        if username:
            user.name = self.model.normalize_username(username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email=email,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=50, default='Anonymous')
    email = models.EmailField(max_length=100, unique=True)

    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # 自定义认证
    session_token = models.CharField(max_length=10, default=0)

    active = models.BooleanField(default=True)
    # a admin user; non super-user
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)  # a superuser

    friends = models.ManyToManyField('self', verbose_name="好友", blank=True, related_name="user_friends")

    created_at = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()


class UserLog(models.Model):
    name = models.CharField(max_length=20, default="xxx", null=True, blank=True)
    info = models.CharField(max_length=20, default="xxx", null=True, blank=True)
