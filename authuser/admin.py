from django.contrib import admin

from .models import User, Profile, Post, Message, Comment

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Message)
admin.site.register(Comment)
