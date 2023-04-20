from django.http import Http404
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from authuser.models import Profile, Post, Message, Comment
from authuser.serializers import ProfileSerializer, PostSerializer, MessageSerializer, CommentSerializer


class ProfilesList(APIView):

    def get(self, request, format=None):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)

        return Response(serializer.data)


class ProfileDetail(APIView):
    def get_object(self, profile_slug):
        try:
            return Profile.objects.get(slug=profile_slug)
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, profile_slug, format=None):
        profile = self.get_object(profile_slug)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)


class PostsList(APIView):

    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):

        print('-------POST LIST DEBUG:-------------------')
        print('request user is: ', request.user)
        user_email = request.user.email
        end_idx = user_email.find('@')
        slug = user_email[:end_idx]

        data = {
            'name': request.data.get('name'),
            'description': request.data.get('description'),
            'comments': request.data.get('comments')
        }

        print('data is: ', data)

        serializer = PostSerializer(data=data, context={'slug': slug})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentsList(APIView):
    def get(self, request, format=None):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)



class MessageList(APIView):
    def get(self, request, format=None):
        messages = Message.objects.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request):
        user_email = request.user.email
        end_idx = user_email.find('@')

        user_slug = user_email[:end_idx]
        recip_slug  = request.data.get('recipSlug')


        data = {
            'title': request.data.get('title'),
            'text_msg': request.data.get('text_msg')
        }

        serializer = MessageSerializer(data=data, context={'user_slug': user_slug, 'recip_slug': recip_slug})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)