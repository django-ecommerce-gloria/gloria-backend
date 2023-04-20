from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

from io import BytesIO
from PIL import Image
from django.core.files import File


class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("You have not provided a valid e-mail address")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(blank=True, default='', unique=True)
    name = models.CharField(max_length=255, blank=True, default='')

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name or self.email.split('@')[0]


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default='Some')
    lastname = models.CharField(max_length=255)
    slug = models.SlugField()
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_profile_url(self):
        return f'/profiles/' + self.slug + '/'

    def get_message_url(self):
        return f'/message-form/' + self.slug + '/'

    def get_absolute_url(self):
        return f'/{self.slug}/'

    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        return ''

    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://127.0.0.1:8000' + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return 'http://127.0.0.1:8000' + self.thumbnail.url
            else:
                return ''

    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail


class Post(models.Model):
    profile = models.ForeignKey(Profile, related_name='posts', null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_added',)

    def __str__(self):
        return self.name

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', null=True, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    profile = models.ForeignKey(Profile, related_name='messages_to', null=True, on_delete=models.CASCADE)
    profile_from = models.ForeignKey(Profile, related_name='messages_from', null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    text_msg = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_added',)

    def __str__(self):
        return self.title



@receiver(post_save, sender=User)
def user_is_created(sender, instance, created, **kwargs):
    if created:
        email = instance.email
        end_idx = email.find('@')
        slug = email[:end_idx]

        Profile.objects.create(name=instance.email, slug=slug, user=instance)
        print('User created!!!!!!!!!')
        print(Profile.objects)
        print(sender)
        print(instance.email)
        print(created)
    else:
        instance.profile.save()










