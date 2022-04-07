import django_filters as filters

from reviews.models import Recipe, Ingredient


class IngredientNameFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name', 'measurement_unit')


class RecipeFilter(filters.FilterSet):
    tags = filters.AllValuesFilter(field_name='tags__slug')

    class Meta:
        model = Recipe
        fields = ('author', 'tags')
