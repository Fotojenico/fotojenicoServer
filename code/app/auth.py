from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import authentication
from firebase_admin import auth


class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):

        token = request.headers.get('auth')
        if not token:
            return None

        try:
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token['uid']
            email = decoded_token['email']
        except Exception as e:
            print(e)
            return None

        try:
            user = User.objects.get(username=uid)
            return [user, token]

        except ObjectDoesNotExist:
            User.objects.create_user(username=uid, email=email)
            user = User.objects.get(username=uid)
            return [user, token]

        except Exception as e:
            print(e)
            return None
