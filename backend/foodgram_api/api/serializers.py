from rest_framework import serializers
from reviews.models import Recipe, Tag, Ingredient, NumberOfIngredients
from drf_extra_fields.fields import Base64ImageField
from rest_framework.validators import UniqueTogetherValidator


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'


class NumberOfIngredientsSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = NumberOfIngredients
        fields = ('id', 'name', 'measurement_unit', 'amount')
        validators = [
            UniqueTogetherValidator(
                queryset=NumberOfIngredients.objects.all(),
                fields=['ingredient', 'recipe']
            )
        ]


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(
        many=True, read_only=True
    )
    image = Base64ImageField()
    ingredients = NumberOfIngredients()

    class Meta:
        model = Recipe
        exclude = ('pub_date', )
