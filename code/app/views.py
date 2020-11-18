from datetime import timedelta

from django.contrib.auth.models import Group
from django.http import Http404
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.response import Response

from app.models import Post, Vote, User, Fav, Profile
from app.serializers import UserSerializer, GroupSerializer, PostSerializer, VoteSerializer, FavSerializer
from app.permissions import IsOwner


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAdminUser]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('shared_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]


class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [IsOwner]


class FavViewSet(viewsets.ModelViewSet):
    queryset = Fav.objects.all()
    serializer_class = FavSerializer
    permission_classes = [IsOwner]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        post = instance.post
        post.favourite_count -= 1
        post.save()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


def api_root(request):
    raise Http404


def buy_multiplier(request, multiplier, hours):
    multiplier_list = [2, 5, 10, 50, 100]
    hours_list = [1, 24, 168, 720]
    user = request.user

    if hours in hours_list and multiplier in multiplier_list:
        user_profile = Profile(owner=user)
        user_profile.point_multiplier = multiplier
        user_profile.multiplier_end_time = timezone.now() + timedelta(hours=hours)
        user_profile.save()
        return Response(status=status.HTTP_200_OK)
    else:
        # TODO mark user for hacking
        return Response(status=status.HTTP_403_FORBIDDEN)
