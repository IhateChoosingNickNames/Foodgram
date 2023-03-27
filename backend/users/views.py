from django.db.models import Count, Exists, OuterRef
from djoser.views import UserViewSet as DefaultUserViewSet
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView

from .models import Subscription, User
from .serializers import CustomUserSerializer, SubscribeSerializer
from api.permissions import IsNotBlockedOrReadOnly
from api.pagination import CustomPagination


class UserViewSet(DefaultUserViewSet):
    """Вьюсет пользователей."""

    http_method_names = ("get", "post")

    def get_queryset(self):
        return (
            User.objects.all()
            .annotate(recipes_count=Count("recipes"))
            .annotate(
                is_subscribed=Exists(
                    Subscription.objects.filter(
                        user=self.request.user, author=OuterRef("pk")
                    )
                )
            )
        )


class SubscribeView(CreateAPIView, DestroyAPIView):
    """Вью подписки/отписки."""

    queryset = Subscription.objects.all()
    serializer_class = SubscribeSerializer
    permission_classes = (IsNotBlockedOrReadOnly,)

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

    permission_classes = (IsNotBlockedOrReadOnly,)
    serializer_class = CustomUserSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        return User.objects.filter(
            id__in=Subscription.objects.filter(user=self.request.user).values(
                "author"
            )
        ).annotate(recipes_count=Count("recipes"))
