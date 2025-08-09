from django.db import models
from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import DeckList
from .serializers import (
    DeckListCreateSerializer,
    DeckListUpdateSerializer,
    DeckListSerializer,
)


class DeckListViewSet(viewsets.ModelViewSet):
    queryset = DeckList.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["retrieve", "list"]:
            return DeckListSerializer
        elif self.action == "create":
            return DeckListCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return DeckListUpdateSerializer
        return DeckListSerializer

    def get_queryset(self):
        user = self.request.user
        if self.action == "list":
            return DeckList.objects.filter(
                models.Q(is_private=False) | models.Q(created_by=user)
            )

        return DeckList.objects.all()

    def get_object(self):
        deck = super().get_object()
        user = self.request.user

        if self.action == "retrieve" and deck.is_private and deck.created_by != user:
            raise PermissionDenied("This deck is private.")
        elif (
            self.action in ["update", "partial_update", "destroy"]
            and deck.created_by != user
        ):
            raise PermissionDenied("You can only modify your own decks.")
        return deck
