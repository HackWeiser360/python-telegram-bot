#!/usr/bin/env python


import pytest

from telegram import Location, ChatLocation, User


@pytest.fixture(scope='class')
def chat_location(bot):
    return ChatLocation(TestChatLocation.location, TestChatLocation.address)


class TestChatLocation:
    location = Location(123, 456)
    address = 'The Shire'

    def test_de_json(self, bot):
        json_dict = {
            'location': self.location.to_dict(),
            'address': self.address,
        }
        chat_location = ChatLocation.de_json(json_dict, bot)

        assert chat_location.location == self.location
        assert chat_location.address == self.address

    def test_to_dict(self, chat_location):
        chat_location_dict = chat_location.to_dict()

        assert isinstance(chat_location_dict, dict)
        assert chat_location_dict['location'] == chat_location.location.to_dict()
        assert chat_location_dict['address'] == chat_location.address

    def test_equality(self, chat_location):
        a = chat_location
        b = ChatLocation(self.location, self.address)
        c = ChatLocation(self.location, 'Mordor')
        d = ChatLocation(Location(456, 132), self.address)
        e = User(456, '', False)

        assert a == b
        assert hash(a) == hash(b)
        assert a is not b

        assert a == c
        assert hash(a) == hash(c)

        assert a != d
        assert hash(a) != hash(d)

        assert a != e
        assert hash(a) != hash(e)
