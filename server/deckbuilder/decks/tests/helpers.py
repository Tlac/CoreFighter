import random

from decks.factories import GundamCardFactory
from deckbuilder.constants.card_data import CARD_SETS, CARD_COLOURS


def generate_card_id():
    base = random.choice(CARD_SETS)
    suffix = f"{random.randint(0, 200):03}"
    return f"{base}-{suffix}"


def generate_deck_list(num_cards: int = 50, card_colours: list[str] | None = None):
    card_list = {}

    if card_colours is None:
        card_colours = random.sample(set(CARD_COLOURS), 1)

    for index in range(num_cards):
        card_id = generate_card_id()
        GundamCardFactory(id=card_id, colour=card_colours[index % len(card_colours)])

        card_list[card_id] = card_list.get(card_id, 0) + 1

    return card_list
