import random
import pytest
from django.urls import reverse
from rest_framework import status

from decks.factories import (
    UserFactory,
    DeckListFactory,
    GundamCardFactory,
)
from deckbuilder.constants.card_data import CARD_SETS, CARD_COLOURS, BLUE, RED, GREEN
from decks.tests.helpers import generate_card_id, generate_deck_list


@pytest.mark.django_db
def test_create_deck_success(auth_client):
    client, user = auth_client()

    COLOURS = [BLUE, RED]
    DECK_NAME = "My First Deck"
    IS_PRIVATE = True

    payload = {
        "name": DECK_NAME,
        "is_private": IS_PRIVATE,
        "cards": generate_deck_list(card_colours=COLOURS),
    }

    url = reverse("deck-list")
    res = client.post(url, payload, format="json")

    assert res.status_code == status.HTTP_201_CREATED, res.data
    body = res.json()

    assert body["name"] == DECK_NAME
    assert body["is_private"] is IS_PRIVATE
    assert sorted(body["colours"]) == COLOURS


@pytest.mark.django_db
@pytest.mark.parametrize(
    "card_count",
    [0, 1, 49, 51, 100],
)
def test_create_deck_fails_if_not_50(auth_client, card_count):
    client, _ = auth_client()

    COLOURS = [BLUE, RED]
    DECK_NAME = "My Second Deck"
    IS_PRIVATE = True

    payload = {
        "name": DECK_NAME,
        "is_private": IS_PRIVATE,
        "cards": generate_deck_list(num_cards=card_count, card_colours=COLOURS),
    }

    url = reverse("deck-list")
    res = client.post(url, payload, format="json")
    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert "cards" in res.json()
    assert (
        res.json()["cards"][0]
        == f"The deck requires 50 total cards, {card_count} was given"
    )


@pytest.mark.django_db
def test_create_deck_fails_if_more_than_two_colours(auth_client):
    client, _ = auth_client()

    COLOURS = [BLUE, RED, GREEN]
    DECK_NAME = "My Third Deck"
    IS_PRIVATE = True

    payload = {
        "name": DECK_NAME,
        "is_private": IS_PRIVATE,
        "cards": generate_deck_list(num_cards=50, card_colours=COLOURS),
    }

    url = reverse("deck-list")
    res = client.post(url, payload, format="json")
    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert "cards" in res.json()
    assert res.json()["cards"][0] == "A deck cannot contain more than 2 unique colours."
