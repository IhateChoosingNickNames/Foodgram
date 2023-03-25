from djoser.views import UserViewSet as UVS
from rest_framework import mixins
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    GenericAPIView,
    ListAPIView,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from api.pagination import CustomPagination
from api.permissions import IsAdminOrReadOnly
from rest_framework import pagination
from .models import Subscription, User
from .serializers import (
    SubscribeSerializer,
    SubscriptionListSerializer,
    CustomUserSerializer,
)


class UserViewSet(UVS):
    """Вьюсет пользователей."""

    # permission_classes = (IsAdminOrReadOnly,)
    # pagination_class = CustomPagination
    http_method_names = ("get", "post")


class SubscribeView(CreateAPIView, DestroyAPIView):
    """Вью подписки/отписки."""

    queryset = Subscription.objects.all()
    serializer_class = SubscribeSerializer

    def get_object(self):
        return User.objects.get(
            id=self.request.parser_context["kwargs"]["user_id"]
        )

    def perform_create(self, serializer):

        if self.request.user == self.get_object():
            raise ValidationError("Нельзя подписываться на самом себя.")

        Subscription.objects.create(
            user=self.request.user, author=self.get_object()
        )

    def perform_destroy(self, instance):
        to_delete = Subscription.objects.filter(
            user=self.request.user, author=instance
        )
        if to_delete.exists():
            to_delete.delete()


class SubscribeListView(ListAPIView):
    """Получение всех текущих подписок."""

    serializer_class = CustomUserSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        return User.objects.filter(
            id__in=Subscription.objects.filter(user=self.request.user).values(
                "author"
            )
        )
