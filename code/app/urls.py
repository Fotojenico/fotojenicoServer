from django.urls import include, path
from rest_framework import routers

from app.views import UserViewSet, GroupViewSet, PostViewSet, VoteViewSet, AchievementProgressViewSet, FavViewSet, api_root, buy_multiplier, post_list
from fotojenicoServer.settings import DEBUG

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('groups', GroupViewSet)
router.register('posts', PostViewSet)
router.register('votes', VoteViewSet)
router.register('fav', FavViewSet)
router.register('achievement_progress', AchievementProgressViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('posts/', post_list, name='post_list'),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('buy_multiplier/<int:multiplier>/<int:hours>/', buy_multiplier, name='buy_multiplier'),
]
if not DEBUG:
    urlpatterns.insert(0, path('', api_root))
