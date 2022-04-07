from .serializers import FollowSerializer, ShowFollowSerializer
from reviews.models import Follow
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework import permissions
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    @action(
        detail=True, methods=['GET', 'DELETE'],
        url_path='subscribe', url_name='subscribe',
        permission_classes=[permissions.IsAuthenticated]
    )
    def subscribe(self, request, id):
        author = get_object_or_404(User, id=id)
        serializer = FollowSerializer
        if request.method == 'GET':
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)
            serializer = ShowFollowSerializer(author)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        follow = get_object_or_404(Follow, user=request.user, author__id=id)
        follow.delete()
        return Response(
            f'{request.user} отписался от {follow.author}'
        )

    @action(
        detail=False, methods=['GET'],
        url_path='subscriptions', url_name='subscriptions',
        permissions_classes=[permissions.IsAuthenticated]
    )
    def show_follows(self, request):
        user_ojb = User.objects.filter(following__user=request.user)
        paginator = PageNumberPagination()
        paginator.page_size = 6
        result_page = paginator.paginate_queryset(user_ojb, request)
        serializer = ShowFollowSerializer(
            result_page, many=True, context={'current_user': request.user}
        )
        return paginator.get_paginated_response(serializer.data)
