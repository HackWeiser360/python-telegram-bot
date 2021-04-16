#!/usr/bin/env python


import pytest

from telegram import User, ChosenInlineResult, Location, Voice


@pytest.fixture(scope='class')
def user():
    return User(1, 'First name', False)


@pytest.fixture(scope='class')
def chosen_inline_result(user):
    return ChosenInlineResult(TestChosenInlineResult.result_id, user, TestChosenInlineResult.query)


class TestChosenInlineResult:
    result_id = 'result id'
    query = 'query text'

    def test_de_json_required(self, bot, user):
        json_dict = {'result_id': self.result_id, 'from': user.to_dict(), 'query': self.query}
        result = ChosenInlineResult.de_json(json_dict, bot)

        assert result.result_id == self.result_id
        assert result.from_user == user
        assert result.query == self.query

    def test_de_json_all(self, bot, user):
        loc = Location(-42.003, 34.004)
        json_dict = {
            'result_id': self.result_id,
            'from': user.to_dict(),
            'query': self.query,
            'location': loc.to_dict(),
            'inline_message_id': 'a random id',
        }
        result = ChosenInlineResult.de_json(json_dict, bot)

        assert result.result_id == self.result_id
        assert result.from_user == user
        assert result.query == self.query
        assert result.location == loc
        assert result.inline_message_id == 'a random id'

    def test_to_dict(self, chosen_inline_result):
        chosen_inline_result_dict = chosen_inline_result.to_dict()

        assert isinstance(chosen_inline_result_dict, dict)
        assert chosen_inline_result_dict['result_id'] == chosen_inline_result.result_id
        assert chosen_inline_result_dict['from'] == chosen_inline_result.from_user.to_dict()
        assert chosen_inline_result_dict['query'] == chosen_inline_result.query

    def test_equality(self, user):
        a = ChosenInlineResult(self.result_id, user, 'Query', '')
        b = ChosenInlineResult(self.result_id, user, 'Query', '')
        c = ChosenInlineResult(self.result_id, user, '', '')
        d = ChosenInlineResult('', user, 'Query', '')
        e = Voice(self.result_id, 'unique_id', 0)

        assert a == b
        assert hash(a) == hash(b)
        assert a is not b

        assert a == c
        assert hash(a) == hash(c)

        assert a != d
        assert hash(a) != hash(d)

        assert a != e
        assert hash(a) != hash(e)
