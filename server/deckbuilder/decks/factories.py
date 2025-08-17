import factory
from django.contrib.auth import get_user_model
from factory.fuzzy import FuzzyChoice, FuzzyInteger
from .models import DeckList, GundamCard

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    password = factory.PostGenerationMethodCall("set_password", "pass1234")


class GundamCardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GundamCard
        django_get_or_create = ("id",)

    id = factory.Sequence(lambda n: f"GD01-{n:03d}")
    rarity = FuzzyChoice(["C", "U", "R", "LR"])
    name = factory.Sequence(lambda n: f"Card {n}")
    level = FuzzyInteger(1, 8)
    cost = FuzzyInteger(1, 8)
    colour = FuzzyChoice(["BLUE", "RED", "GREEN", "WHITE", "PURPLE"])
    type = FuzzyChoice(["UNIT", "PILOT", "COMMAND", "BASE"])
    effect = "-"
    zone = factory.LazyFunction(lambda: ["Earth"])
    trait = factory.LazyFunction(lambda: ["Test"])
    link = "-"
    ap = "1"
    hp = "1"
    title = "Test Title"
    set = "GD01"
    image_url = None
    original_image_url = "www.someCDN.com/bestcard.png"


class DeckListFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DeckList

    name = factory.Sequence(lambda n: f"Deck {n}")
    created_by = factory.SubFactory(UserFactory)
    cards = factory.LazyFunction(dict)
    colours = factory.LazyFunction(list)
    is_private = True
