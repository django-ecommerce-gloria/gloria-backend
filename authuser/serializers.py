from rest_framework import serializers

from .models import Profile, Post, Message, Comment
from product.serializers import ProductSerializer, OrderSerializer


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = (
            "id",
            "text",
            "date_added"
        )


class PostSerializer(serializers.ModelSerializer):

    #profile = serializers.CharField(source="profile.name", read_only=True)
    comments = CommentSerializer(many=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "name",
            "description",
            "comments",
            "date_added"
        )

    def create(self, validated_data):
        comments_data = validated_data.pop('comments')

        profile_slug = self.context.get('slug')
        profile = Profile.objects.get(slug=profile_slug)

        post = Post.objects.create(profile=profile, **validated_data)

        for comment in comments_data:
            Comment.objects.create(post=post, **comment)

        return post


class MessageSerializer(serializers.ModelSerializer):

    profile = serializers.CharField(source ='profile.slug', read_only = True)
    profile_from = serializers.CharField(source ='profile_from.slug', read_only = True)


    class Meta:
        model = Message
        fields = (
            "id",
            "title",
            "text_msg",
            "date_added",
            "profile",
            "profile_from"
        )

    def create(self, validated_data):

        profile_from_slug = self.context.get('user_slug')
        profile_from = Profile.objects.get(slug=profile_from_slug)

        profile_slug = self.context.get('recip_slug')
        profile = Profile.objects.get(slug=profile_slug)

        message = Message.objects.create(profile=profile, profile_from=profile_from, **validated_data)

        return message


class ProfileSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
    posts = PostSerializer(many=True)
    messages_to = MessageSerializer(many=True)
    orders = OrderSerializer(many=True)


    class Meta:
        model = Profile
        depth = 2
        fields = (
            "id",
            "name",
            "lastname",
            "get_absolute_url",
            "get_profile_url",
            "get_message_url",
            "get_image",
            "get_thumbnail",
            "products",
            "posts",
            "messages_to",
            "orders"
        )


