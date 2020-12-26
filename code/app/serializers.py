from django.contrib.auth.models import User, Group
from rest_framework import serializers, status
from rest_framework.response import Response

from app.models import Post, Vote, Fav, Profile, AchievementProgress


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
        fields = ['id', 'upvote_count', 'downvote_count', 'view_count', 'favourite_count', 'file', 'owner', 'shared_at', 'last_modified']

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
        fields = ['id', 'post', 'owner', 'vote_weight', 'sent_at', 'watch_seconds']

    def create(self, validated_data):
        post = validated_data.pop('post')
        vote_weight = int(validated_data.pop('vote_weight'))
        watch_seconds = int(validated_data.pop('watch_seconds'))
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            user_profile = Profile.objects.get(owner=user)
            if vote_weight == 1:
                post.upvote_count += user_profile.give_point_multiplier * user_profile.point_multiplier
            elif vote_weight == -1:
                post.downvote_count += user_profile.give_point_multiplier * user_profile.point_multiplier
            else:
                user_profile = Profile.objects.get(owner=request.user)
                user_profile.suspicion_level += 1
                user_profile.save()
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            post.view_count += 1
            user_profile.points += user_profile.get_point_multiplier * user_profile.point_multiplier
            user_profile.save()
            post.save()
            vote = Vote.objects.create(owner=user, post=post, vote_weight=vote_weight, watch_seconds=watch_seconds)
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
        # TODO Mark user for hacking


class AchievementProgressSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AchievementProgress
        fields = ['id', 'owner', 'achievement', 'step_count', 'progress_step']
