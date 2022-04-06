from django.urls import path, include
from .views import RecipesViewSet
from rest_framework.routers import DefaultRouter

router_v1 = DefaultRouter()
router_v1.register('recipes', RecipesViewSet, basename='recipes')

urlpatterns = [
    path('', include(router_v1.urls)),
]
