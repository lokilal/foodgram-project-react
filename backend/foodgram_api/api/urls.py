from django.urls import path, include
from .views import RecipesViewSet, TagsViewSet, IngredientViewSet, download_shopping_cart, ShoppingCartView
from rest_framework.routers import DefaultRouter

router_v1 = DefaultRouter()
router_v1.register('recipes', RecipesViewSet, basename='recipes')
router_v1.register('tags', TagsViewSet, basename='tags')
router_v1.register('ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    path('recipes/<int:recipe_id>/shopping_cart/', ShoppingCartView.as_view(),
         name='shopping_cart'),
    path('recipes/download_shopping_cart/', download_shopping_cart,
         name='download_shopping_cart'),
    path('', include(router_v1.urls)),
]
