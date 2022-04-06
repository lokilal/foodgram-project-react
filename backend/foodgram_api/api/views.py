from django.shortcuts import render
from rest_framework import viewsets
from reviews.models import Recipe, Tag
from .serializers import RecipeSerializer


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
