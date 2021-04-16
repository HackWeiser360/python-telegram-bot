#!/usr/bin/env python



import pytest

from telegram import Dice, BotCommand


@pytest.fixture(scope="class", params=Dice.ALL_EMOJI)
def dice(request):
    return Dice(value=5, emoji=request.param)


class TestDice:
    value = 4

    @pytest.mark.parametrize('emoji', Dice.ALL_EMOJI)
    def test_de_json(self, bot, emoji):
        json_dict = {'value': self.value, 'emoji': emoji}
        dice = Dice.de_json(json_dict, bot)

        assert dice.value == self.value
        assert dice.emoji == emoji
        assert Dice.de_json(None, bot) is None

    def test_to_dict(self, dice):
        dice_dict = dice.to_dict()

        assert isinstance(dice_dict, dict)
        assert dice_dict['value'] == dice.value
        assert dice_dict['emoji'] == dice.emoji

    def test_equality(self):
        a = Dice(3, '🎯')
        b = Dice(3, '🎯')
        c = Dice(3, '🎲')
        d = Dice(4, '🎯')
        e = BotCommand('start', 'description')

        assert a == b
        assert hash(a) == hash(b)

        assert a != c
        assert hash(a) != hash(c)

        assert a != d
        assert hash(a) != hash(d)

        assert a != e
        assert hash(a) != hash(e)
