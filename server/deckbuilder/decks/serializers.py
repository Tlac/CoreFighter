from rest_framework import serializers
from .models import DeckList, GundamCard


class DeckListSerializer(serializers.ModelSerializer):
    REQUIRED_NUMBER_OF_CARDS = 50
    cards = serializers.ListField(
        child=serializers.CharField(), write_only=True
    )
    class Meta:
        model = DeckList
        fields = ['id', 'name', 'cards', 'is_private']
        read_only_fields = ['id']

    def validate_cards(self, card_ids):
        cards = GundamCard.objects.filter(id__in=card_ids)
        colours = {card.colour for card in cards}

        if len(cards) != len(set(card_ids)):
            raise serializers.ValidationError("Some card IDs are invalid.")

        if len(card_ids) != self.REQUIRED_NUMBER_OF_CARDS:
            raise serializers.ValidationError("The deck requires 50 cards")

        if len(colours) > 3:
            raise serializers.ValidationError("A deck cannot contain more than 3 unique colours.")

        if len(set(card_ids)) != len(cards):
            raise serializers.ValidationError("Some cards are not valid")

        self.context['valid_cards'] = cards
        self.context['colours'] = list(colours)
        return card_ids

    def create(self, validated_data):
        user = self.context['request'].user
        colours = self.context['colours']
        card_ids = validated_data['cards']

        deck = DeckList.objects.create(
            name=validated_data['name'],
            created_by=user,
            cards=card_ids,
            colours=colours,
            is_private=validated_data.get('is_private', True),
        )
        return deck

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if instance.created_by != user:
            raise serializers.ValidationError("You are not allowed to update this deck.")

        if 'cards' in validated_data:
            card_ids = validated_data['cards']
            cards = GundamCard.objects.filter(id__in=card_ids)
            if len(cards) != len(set(card_ids)):
                raise serializers.ValidationError("Some card IDs are invalid.")
            colours = {card.colour for card in cards}
            if len(colours) > 3:
                raise serializers.ValidationError("A deck cannot contain more than 3 unique colours.")
            instance.cards = card_ids
            instance.colours = list(colours)

        if 'name' in validated_data:
            instance.name = validated_data['name']

        if 'is_private' in validated_data:
            instance.is_private = validated_data['is_private']

        instance.save()
        return instance
