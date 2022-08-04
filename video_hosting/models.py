from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import User, PermissionsMixin

from rest_api_video.settings import DEFAULT_FROM_EMAIL


class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        responce = self._create_user(email, password, **extra_fields)
        send_mail(subject="Account Approved",
                  message="Hello we are TeachMeSkill Infocigans and we are "
                          "approved your account",
                  from_email=DEFAULT_FROM_EMAIL,
                  recipient_list=[email])
        return responce

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    created = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(unique=True, blank=False)
    first_name = models.CharField(max_length=30, blank=True, default="")
    last_name = models.CharField(max_length=100, blank=True, default="")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(blank=False, default=False)
    delete_at = models.DateTimeField(null=True, default=None)
    is_banned = models.BooleanField(null=False, blank=True, default=False)
    abuse_comments_counter = models.IntegerField(default=0)
    subscriptions = models.ManyToManyField(to='video_hosting.Channel', blank=True, null=True,
                                           related_name="subscribers")
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return True

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def unbann_user(self):
        self.is_banned = False
        self.save()

class Video(models.Model):
    name = models.CharField(max_length=255, default='Untitled')
    title = models.CharField(max_length=255, default='Empty')
    uploaded = models.DateTimeField(auto_now_add=True, blank=True)
    likes_count = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    link = models.URLField(max_length=255, null=False, blank=False)
    # channel = models.ForeignKey('Channel', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.name} -- {self.id}'


class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, blank=False, null=False, related_name='comments')
    content = models.TextField()
    likes_count = models.IntegerField(default=0)

    def __str__(self):
        return f'some_comment -- {self.id}'


class HashTag(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, blank=True, null=True, related_name='hashtag')
    tag = models.CharField(max_length=255, default='#')


class VideoRecommendation(models.Model):
    videos = models.ManyToManyField(Video, blank=True, null=True, related_name='recommendation')
    recommendation_name = models.CharField(max_length=255, default='')
    is_top_rated = models.BooleanField()


class Channel(models.Model):
    name = models.CharField(max_length=255, default='Untitled')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='channel')
    # subscriber = models.ManyToManyField('Subscriber', blank=True, null=True)


# class Subscriber(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     channel = models.ManyToManyField(Channel, on_delete=models.CASCADE)


