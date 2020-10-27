from django.contrib.auth.models import User, Group
from rest_framework import serializers, status
from rest_framework.response import Response

from app.models import Post, Vote, Fav, Profile


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        Profile.objects.create(owner=user)
        return user


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'upvote_count', 'downvote_count', 'favourite_count', 'file', 'owner', 'shared_at', 'last_modified']

    def create(self, validated_data):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            post = Post.objects.create(owner=user, file=validated_data.pop('file'))
            return post
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id', 'post', 'owner', 'vote_weight', 'sent_at']

    def create(self, validated_data):
        post = validated_data.pop('post')
        vote_weight = int(validated_data.pop('vote_weight'))
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            if vote_weight == 1:
                post.upvote_count += 1
            elif vote_weight == -1:
                post.downvote_count += 1
            else:
                # Mark user for hacking
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            post.save()
            vote = Vote.objects.create(owner=user, post=post, vote_weight=vote_weight)
            return vote


class FavSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fav
        fields = ['id', 'post', 'owner', 'sent_at']

    def create(self, validated_data):
        post = validated_data.pop('post')
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            post.favourite_count += 1
            post.save()
            fav = Fav.objects.create(owner=user, post=post)
            return fav
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        # Mark user for hacking
