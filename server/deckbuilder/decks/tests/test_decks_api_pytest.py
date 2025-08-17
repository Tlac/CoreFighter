import random
import pytest
from django.urls import reverse
from rest_framework import status

from decks.factories import (
    UserFactory,
    DeckListFactory,
    GundamCardFactory,
)
from deckbuilder.constants.card_data import (
    CARD_SETS,
    CARD_COLOURS,
    BLUE,
    RED,
    GREEN,
    WHITE,
)
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


@pytest.mark.django_db
def test_list_public_and_own_private(auth_client):
    client, USER_ONE = auth_client()

    DECK_ONE_COLOURS = [RED, GREEN]
    DECK_ONE_NAME = "User one private deck"
    DECK_ONE_IS_PRIVATE = True

    url = reverse("deck-list")
    res1 = client.post(
        url,
        {
            "name": DECK_ONE_NAME,
            "is_private": DECK_ONE_IS_PRIVATE,
            "cards": generate_deck_list(num_cards=50, card_colours=DECK_ONE_COLOURS),
        },
        format="json",
    )
    assert res1.status_code == status.HTTP_201_CREATED

    DECK_TWO_COLOURS = [GREEN, WHITE]
    DECK_TWO_NAME = "User two's public deck"
    USER_TWO = UserFactory()
    client.force_authenticate(user=USER_TWO)
    res2 = client.post(
        url,
        {
            "name": DECK_TWO_NAME,
            "is_private": False,
            "cards": generate_deck_list(num_cards=50, card_colours=DECK_TWO_COLOURS),
        },
        format="json",
    )

    assert res2.status_code == status.HTTP_201_CREATED

    user_two_request = client.get(url)
    assert user_two_request.status_code == status.HTTP_200_OK
    names = [d["name"] for d in user_two_request.json()]
    assert DECK_TWO_NAME in names
    assert DECK_ONE_NAME not in names

    client.force_authenticate(user=USER_ONE)
    user_one_request = client.get(url)
    assert user_one_request.status_code == status.HTTP_200_OK
    names = [d["name"] for d in user_one_request.json()]
    assert DECK_ONE_NAME in names
    assert DECK_TWO_NAME in names


@pytest.mark.django_db
def test_retrieve_private_forbidden_to_non_owner(auth_client):
    client, USER_ONE = auth_client()
    DECK_ONE_COLOURS = [RED, GREEN]

    # User one creates private deck
    list_url = reverse("deck-list")
    res = client.post(
        list_url,
        {
            "name": "Secret",
            "is_private": True,
            "cards": generate_deck_list(num_cards=50, card_colours=DECK_ONE_COLOURS),
        },
        format="json",
    )
    deck_id = res.json()["id"]
    detail_url = reverse("deck-detail", args=[deck_id])

    # User two tries to get User one's deck
    USER_TWO = UserFactory()
    client.force_authenticate(user=USER_TWO)
    r = client.get(detail_url)
    assert r.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_update_validations_and_ownership(auth_client):
    client, USER_ONE = auth_client()
    DECK_ONE_COLOURS = [RED, GREEN]

    # User one creates public deck
    list_url = reverse("deck-list")
    create = client.post(
        list_url,
        {
            "name": "Updatable",
            "is_private": False,
            "cards": generate_deck_list(num_cards=50, card_colours=DECK_ONE_COLOURS),
        },
        format="json",
    )
    assert create.status_code == status.HTTP_201_CREATED
    deck_id = create.json()["id"]
    detail_url = reverse("deck-detail", args=[deck_id])

    # User two should not be able to update user one's deck
    USER_TWO = UserFactory()
    client.force_authenticate(user=USER_TWO)
    forbidden = client.patch(detail_url, {"name": "Hacked"}, format="json")
    assert forbidden.status_code == status.HTTP_403_FORBIDDEN

    # User one should be able to update their own deck
    client.force_authenticate(user=USER_ONE)
    ok = client.patch(detail_url, {"name": "Updated Name"}, format="json")
    assert ok.status_code == status.HTTP_200_OK
    assert ok.json()["name"] == "Updated Name"

    current = client.get(detail_url).json()

    new_decklist = {}
    for card in current["cards"][:49]:
        new_decklist[card["id"]] = new_decklist.get(card["id"], 0) + 1

    green_id = GundamCardFactory(colour="GREEN", cost=1).id
    new_decklist[green_id] = new_decklist.get(green_id, 0) + 1

    illegal_decklist_edit_request = client.patch(
        detail_url, {"cardlist": new_decklist}, format="json"
    )
    assert illegal_decklist_edit_request.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_user_can_only_delete_their_own_decks(auth_client):
    client, USER_ONE = auth_client()
    DECK_ONE_COLOURS = [RED, GREEN]

    list_url = reverse("deck-list")
    create = client.post(
        list_url,
        {
            "name": "Delete Me",
            "cards": generate_deck_list(num_cards=50, card_colours=DECK_ONE_COLOURS),
        },
        format="json",
    )
    deck_id = create.json()["id"]
    detail_url = reverse("deck-detail", args=[deck_id])

    # User two should not be able to delete user one's deck
    USER_TWO = UserFactory()
    client.force_authenticate(user=USER_TWO)
    user_two_delete_user_one_deck_request = client.delete(detail_url)
    assert (
        user_two_delete_user_one_deck_request.status_code == status.HTTP_403_FORBIDDEN
    )

    # User one can delete their own deck
    client.force_authenticate(user=USER_ONE)
    user_one_delete_user_one_deck_request = client.delete(detail_url)
    assert (
        user_one_delete_user_one_deck_request.status_code == status.HTTP_204_NO_CONTENT
    )
