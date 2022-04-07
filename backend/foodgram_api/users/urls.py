from django.urls import path, include
from rest_framework.routers import DefaultRouter


router_v1 = DefaultRouter()
router_v1.register('users', '')


urlpatterns = [
    path('', include(router_v1.urls))
]