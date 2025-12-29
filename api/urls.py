from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PostViewSet, CommentViewSet

router_v1 = DefaultRouter()
router_v1.register('posts', PostViewSet, basename='posts')
router_v1.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='comments',
)

urlpatterns = [
    path('', include(router_v1.urls)),
]
