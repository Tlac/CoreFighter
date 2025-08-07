from django.urls import path
from .views import (
    DeckListCreateView,
    DeckListRetrieveUpdateDeleteView,
)

urlpatterns = [
    path('', DeckListCreateView.as_view(), name='deck-create'),
    path('<uuid:pk>/', DeckListRetrieveUpdateDeleteView.as_view(), name='deck-detail'),
]
