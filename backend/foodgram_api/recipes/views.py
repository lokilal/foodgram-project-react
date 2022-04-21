from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from users.paginator import CustomPageNumberPaginator

from .filters import IngredientsFilter, RecipeFilter
from .models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                     ShoppingList, Tag)
from .permissions import IsAdminOrReadOnly, IsAuthorOrAdmin
from .serializers import (AddRecipeSerializer, FavouriteSerializer,
                          IngredientsSerializer, ShoppingListSerializer,
                          ShowRecipeFullSerializer, TagsSerializer)
from .utils import download_file_response


class IngredientsViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientsFilter


class TagsViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    permission_classes = [IsAdminOrReadOnly]


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all().order_by('-id')
    permission_classes = [IsAuthorOrAdmin]
    filter_backends = (DjangoFilterBackend, )
    filterset_class = RecipeFilter
    pagination_class = CustomPageNumberPaginator

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ShowRecipeFullSerializer
        return AddRecipeSerializer

    def add(self, request, pk, serializer_class):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = serializer_class(data=data,
                                      context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def deletion(self, request, pk, model):
        recipe = get_object_or_404(Recipe, id=pk)
        obj = get_object_or_404(
            model, user=request.user,
            recipe=recipe
        )
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True,
            permission_classes=[permissions.IsAuthenticated], methods=['POST']
            )
    def favorite(self, request, pk=None):
        return self.add(request, pk, FavouriteSerializer)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk=None):
        return self.deletion(request, pk, Favorite)

    @action(detail=True,
            permission_classes=[permissions.IsAuthenticated], methods=['POST']
            )
    def shopping_cart(self, request, pk=None):
        return self.add(request, pk, ShoppingListSerializer)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk=None):
        return self.deletion(request, pk, ShoppingList)

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    def download_shopping_cart(self, request):
        ingredients_list = RecipeIngredient.objects.filter(
            recipe__shopping_cart__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(count=Sum('amount'))
        return download_file_response(ingredients_list)
