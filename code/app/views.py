from datetime import timedelta
from os import getenv

from django.contrib.auth.models import Group
from django.http import Http404
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from app.models import Post, Vote, User, Fav, Profile, Sent, AchievementProgress
from app.serializers import UserSerializer, GroupSerializer, PostSerializer, VoteSerializer, FavSerializer, AchievementProgressSerializer
from app.permissions import IsOwner, OwnerReadOnly
from fotojenicoServer.settings import ACHIEVEMENTS


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


class AchievementProgressViewSet(viewsets.ModelViewSet):
    pagination_class = None
    queryset = AchievementProgress.objects.all()
    serializer_class = AchievementProgressSerializer
    permission_classes = [OwnerReadOnly]

    def get_queryset(self):
        # after get all products on DB it will be filtered by its owner and return the queryset
        owner_queryset = self.queryset.filter(owner=self.request.user)
        return owner_queryset


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


@api_view(['POST'])
def buy_multiplier(request, multiplier, hours):
    multiplier_list = [2, 5, 10, 50, 100]
    hours_list = [1, 24, 168, 720]
    user = request.user

    if hours in hours_list and multiplier in multiplier_list:
        user_profile = Profile(owner=user)
        user_profile.point_multiplier = multiplier
        user_profile.multiplier_end_time = timezone.now() + timedelta(hours=hours)
        user_profile.save()
        return Response(status=status.HTTP_201_CREATED)
    else:
        # TODO mark user for hacking
        return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(['GET', 'POST'])
def post_list(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            top_posts = Post.objects.all().exclude(sent__owner=request.user).order_by('view_count', 'upvote_count')[:int(getenv('REST_PAGE_SIZE'))]
            for post in top_posts:
                Sent.objects.create(owner=request.user, post=post)
            if len(top_posts) == 0:
                achievement_progress, achievement_created = AchievementProgress.objects.get_or_create(
                    owner=request.user,
                    achievement='daily_list_end',
                    step_count=ACHIEVEMENTS['daily_list_end']['step_count'],
                )
                if achievement_progress.progress_reset_time is None:
                    achievement_progress.progress_reset_time = timezone.now() + timedelta(days=1)
                    achievement_progress.save()

                if not achievement_created and achievement_progress.progress_reset_time > timezone.now():
                    achievement_progress.progress_step += 1
                    achievement_progress.save()

            return Response(PostSerializer(top_posts, many=True).data)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
    elif request.method == 'POST':

        if request.user.is_authenticated:
            user = request.user
            return_post = Post.objects.create(owner=user, file=request.FILES['file'])
            return Response(PostSerializer(return_post).data)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)
