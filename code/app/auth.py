from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from rest_framework import authentication
from firebase_admin import auth

from app.models import Profile, Achievements, AchievementProgress


class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get('auth')
        if not token:
            return None

        try:
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token['uid']
            email = decoded_token['email']
            username = ''
            if 'name' in decoded_token:
                username = decoded_token['name']
        except Exception as e:
            print(e)
            return None

        try:
            user, result = User.objects.get_or_create(username=uid, email=email)
            user.last_login = timezone.now()
            user.save()
            profile, _ = Profile.objects.get_or_create(owner=user)
            if username != '':
                profile.shown_username = username
            profile.save()
            all_achievements = Achievements.objects.all()
            for achievement in all_achievements:
                AchievementProgress.objects.get_or_create(achievement=achievement, owner=user)
            return [user, token]

        except Exception as e:
            print(e)
            return None
