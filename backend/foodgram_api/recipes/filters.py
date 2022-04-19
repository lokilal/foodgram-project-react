import django_filters as filters
from django.contrib.auth import get_user_model

from .models import Ingredient, Recipe

User = get_user_model()


class IngredientsFilter(filters.FilterSet):
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
    )

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(filters.FilterSet):
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = filters.CharFilter(method='filter_is_favorited')
    is_in_shopping_cart = filters.CharFilter(
        method='filter_is_in_shopping_cart'
    )

    class Meta:

        model = Recipe
        fields = ('tags', 'author', 'is_in_shopping_cart', 'is_favorited')

    def filter_is_favorited(self, queryset, name, item_value):
        if bool(int(item_value)):
            queryset = queryset.filter(in_favorite__user=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, item_value):
        if bool(int(item_value)):
            queryset = queryset.filter(shopping_cart__user=self.request.user)
        return queryset
