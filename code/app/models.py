from os.path import splitext
from django.db import models
from django.contrib.auth.models import User
import uuid


def photo_path(instance, filename):
    _, file_extension = splitext(filename)
    return f'user-uploads/{instance.owner.id}/{str(uuid.uuid4())}{file_extension}'


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    shown_username = models.TextField(default='', max_length=25)
    points = models.BigIntegerField(default=0)
    suspicion_level = models.IntegerField(default=0)
    point_multiplier = models.IntegerField(default=1)
    give_point_multiplier = models.IntegerField(default=1)
    get_point_multiplier = models.IntegerField(default=1)
    multiplier_end_time = models.DateTimeField(auto_now_add=True)


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    file = models.ImageField(blank=True, default='', upload_to=photo_path)
    view_count = models.PositiveBigIntegerField(default=0)
    upvote_count = models.PositiveBigIntegerField(default=0)
    downvote_count = models.PositiveBigIntegerField(default=0)
    favourite_count = models.PositiveBigIntegerField(default=0)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    shared_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)


class PostPriority(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    post = models.ForeignKey(Post, on_delete=models.DO_NOTHING)
    priority = models.IntegerField(default=0)


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
    watch_seconds = models.IntegerField(default=0)
    sent_at = models.DateTimeField(auto_now_add=True)


class Fav(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    post = models.ForeignKey(Post, on_delete=models.DO_NOTHING)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True)
    sent_at = models.DateTimeField(auto_now_add=True)


class AchievementProgress(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    achievement = models.TextField()
    step_count = models.IntegerField(default=1)
    progress_step = models.IntegerField(default=0)
    progress_reset_time = models.DateTimeField(null=True)


class Multiplier(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    multiply_times = models.IntegerField(default=1)
    bought_at = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True)
    stackable = models.BooleanField(default=False)


class Sent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    post = models.ForeignKey(Post, on_delete=models.DO_NOTHING)
    sent_at = models.DateTimeField(auto_now_add=True)
