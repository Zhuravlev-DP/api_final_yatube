from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import PostViewSet, GroupViewSet, CommentViewSet, FollowViewSet

router_v1 = DefaultRouter()
router_v1.register(r'posts', PostViewSet)
router_v1.register(r'groups', GroupViewSet)
router_v1.register(
    r'posts/(?P<post_id>[1-9]\d*)/comments',
    CommentViewSet,
    basename='comments'
)
router_v1.register(r'follow', FollowViewSet, basename='follow')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/', include('djoser.urls.jwt')),
]
