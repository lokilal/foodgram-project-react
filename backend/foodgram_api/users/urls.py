from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet


router_v1 = DefaultRouter()
router_v1.register('users', CustomUserViewSet)


urlpatterns = [
    path('', include(router_v1.urls)),
]
