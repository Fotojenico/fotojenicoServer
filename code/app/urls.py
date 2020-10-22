from django.urls import include, path
from rest_framework import routers
from app.views import UserViewSet, GroupViewSet, PostViewSet, VoteViewSet, FavViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('groups', GroupViewSet)
router.register('posts', PostViewSet)
router.register('votes', VoteViewSet)
router.register('fav', FavViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]