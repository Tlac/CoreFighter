from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import DeckList
from .serializers import DeckListCreateSerializer, DeckListUpdateSerializer


class DeckListViewSet(viewsets.ModelViewSet):
    queryset = DeckList.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return DeckListCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return DeckListUpdateSerializer
        return DeckListUpdateSerializer  # could also have a read-only serializer for retrieve/list

    def get_object(self):
        deck = super().get_object()
        user = self.request.user

        if self.action == 'retrieve' and deck.is_private and deck.created_by != user:
            raise PermissionDenied("This deck is private.")
        elif self.action in ['update', 'partial_update', 'destroy'] and deck.created_by != user:
            raise PermissionDenied("You can only modify your own decks.")
        return deck
