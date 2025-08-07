from rest_framework import generics, permissions
from .models import DeckList
from .serializers import DeckListSerializer
from rest_framework.exceptions import PermissionDenied


class DeckListCreateView(generics.CreateAPIView):
    queryset = DeckList.objects.all()
    serializer_class = DeckListSerializer
    permission_classes = [permissions.IsAuthenticated]


class DeckListRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DeckList.objects.all()
    serializer_class = DeckListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        deck = super().get_object()
        user = self.request.user

        if self.request.method == 'GET' and deck.is_private and deck.created_by != user:
            raise PermissionDenied("This deck is private.")
        elif self.request.method in ['PUT', 'PATCH', 'DELETE'] and deck.created_by != user:
            raise PermissionDenied("You can only modify your own decks.")
        return deck
