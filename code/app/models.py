from django.db import models
from django.contrib.auth.models import User
import uuid


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    file = models.ImageField(blank=True, default='')
    upvote_count = models.PositiveBigIntegerField(default=0)
    downvote_count = models.PositiveBigIntegerField(default=0)
    favourite_count = models.PositiveBigIntegerField(default=0)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    shared_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    comment_of = models.ForeignKey(Post, on_delete=models.DO_NOTHING, null=True)
    text = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    shared_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)


class Vote(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True)
    post = models.ForeignKey(Post, on_delete=models.DO_NOTHING)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True)
    vote_weight = models.IntegerField(default=0)
    sent_at = models.DateTimeField(auto_now_add=True)


class Fav(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    post = models.ForeignKey(Post, on_delete=models.DO_NOTHING)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True)
    sent_at = models.DateTimeField(auto_now_add=True)


class Achievements(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    daily_post_view = models.IntegerField(default=0)
