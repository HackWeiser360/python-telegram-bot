#!/usr/bin/env python


import pytest

from telegram import BotCommand, Dice


@pytest.fixture(scope="class")
def bot_command():
    return BotCommand(command='start', description='A command')


class TestBotCommand:
    command = 'start'
    description = 'A command'

    def test_de_json(self, bot):
        json_dict = {'command': self.command, 'description': self.description}
        bot_command = BotCommand.de_json(json_dict, bot)

        assert bot_command.command == self.command
        assert bot_command.description == self.description

        assert BotCommand.de_json(None, bot) is None

    def test_to_dict(self, bot_command):
        bot_command_dict = bot_command.to_dict()

        assert isinstance(bot_command_dict, dict)
        assert bot_command_dict['command'] == bot_command.command
        assert bot_command_dict['description'] == bot_command.description

    def test_equality(self):
        a = BotCommand('start', 'some description')
        b = BotCommand('start', 'some description')
        c = BotCommand('start', 'some other description')
        d = BotCommand('hepl', 'some description')
        e = Dice(4, 'emoji')

        assert a == b
        assert hash(a) == hash(b)

        assert a != c
        assert hash(a) != hash(c)

        assert a != d
        assert hash(a) != hash(d)

        assert a != e
        assert hash(a) != hash(e)
