from rest_framework import serializers
from .models import DeckList, GundamCard


class BaseDeckListEditSerializer(serializers.ModelSerializer):
    REQUIRED_NUMBER_OF_CARDS = 50
    MAX_COPIES_OF_CARDS = 4
    MIN_COPIES_OF_CARDS = 1
    MAX_UNIQUE_COLOURS = 2

    cards = serializers.DictField(
        child=serializers.IntegerField(
            min_value=MIN_COPIES_OF_CARDS, max_value=MAX_COPIES_OF_CARDS
        ),
        write_only=True,
        required=False,
        help_text="Mapping of card_id -> quantity",
    )

    class Meta:
        model = DeckList
        fields = ["id", "name", "cards", "is_private", "vote_count"]
        read_only_fields = ["id"]

    def validate_cards(self, card_map):
        """
        Validates the incoming {card_id: qty} mapping.
        """
        if not isinstance(card_map, dict):
            raise serializers.ValidationError(
                "Card list must be a dictionary of {card_id: quantity}."
            )

        # Flatten to a list of IDs repeated by qty
        expanded_ids = [
            card_id for card_id, qty in card_map.items() for _ in range(qty)
        ]

        # Query the DB for all cards
        cards = GundamCard.objects.filter(id__in=card_map.keys())
        if cards.count() != len(card_map):
            # TODO: output invalid card ids in the validation error
            raise serializers.ValidationError("Some card IDs are invalid.")

        # Check total count
        if len(expanded_ids) != self.REQUIRED_NUMBER_OF_CARDS:
            raise serializers.ValidationError(
                f"The deck requires {self.REQUIRED_NUMBER_OF_CARDS} total cards, {len(expanded_ids)} was given"
            )

        # Colour restriction
        colours = {card.colour for card in cards}
        if len(colours) > self.MAX_UNIQUE_COLOURS:
            raise serializers.ValidationError(
                "A deck cannot contain more than 2 unique colours."
            )

        # Store for create/update use
        self.context["valid_cards"] = cards
        self.context["colours"] = list(colours)

        return card_map


class DeckListCreateSerializer(BaseDeckListEditSerializer):
    class Meta(BaseDeckListEditSerializer.Meta):
        extra_kwargs = {"cards": {"required": True}}
        fields = list(BaseDeckListEditSerializer.Meta.fields)

    def create(self, validated_data):
        user = self.context["request"].user
        colours = self.context["colours"]
        cardlist = validated_data["cards"]

        return DeckList.objects.create(
            name=validated_data["name"],
            created_by=user,
            cards=cardlist,
            colours=colours,
            is_private=validated_data.get("is_private", True),
        )


class DeckListUpdateSerializer(BaseDeckListEditSerializer):
    def validate(self, attrs):
        if not attrs:
            raise serializers.ValidationError(
                "At least one of name, cards, or is_private must be provided."
            )
        return attrs

    def update(self, instance, validated_data):
        user = self.context["request"].user
        if instance.created_by != user:
            raise serializers.ValidationError(
                "You are not allowed to update this deck."
            )

        if "cards" in validated_data:
            instance.cards = validated_data["cards"]
            instance.colours = self.context["colours"]

        if "name" in validated_data:
            instance.name = validated_data["name"]

        if "is_private" in validated_data:
            instance.is_private = validated_data["is_private"]

        instance.save()
        return instance


class GundamCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = GundamCard
        fields = [
            "id",
            "rarity",
            "name",
            "level",
            "cost",
            "colour",
            "type",
            "effect",
            "zone",
            "trait",
            "link",
            "ap",
            "hp",
            "title",
            "set",
            "image_url",
            "original_image_url",
        ]


class DeckListSerializer(serializers.ModelSerializer):
    cards = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = DeckList
        fields = ["id", "name", "cards", "is_private", "colours", "vote_count"]

    def get_cards(self, obj):
        card_map = obj.cards
        card_ids = card_map.keys()
        cards = GundamCard.objects.filter(id__in=card_ids)
        card_dict = {card.id: card for card in cards}

        result = []
        for card_id, qty in card_map.items():
            card = card_dict.get(card_id)
            if card:
                card_data = GundamCardSerializer(card).data
                card_data["quantity"] = qty
                result.append(card_data)
        return result
