from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import authentication
from firebase_admin import auth
from fotojenicoServer.settings import ACHIEVEMENTS
from app.models import Profile, AchievementProgress


class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get('auth')
        if not token:
            return None

        try:
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token['user_id']
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
            for achievement in ACHIEVEMENTS:
                AchievementProgress.objects.get_or_create(achievement=achievement, owner=user, step_count=ACHIEVEMENTS[achievement]['step_count'])
            return [user, token]

        except Exception as e:
            print(e)
            return None
