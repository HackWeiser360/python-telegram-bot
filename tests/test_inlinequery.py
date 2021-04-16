#!/usr/bin/env python


import pytest

from telegram import User, Location, InlineQuery, Update


@pytest.fixture(scope='class')
def inline_query(bot):
    return InlineQuery(
        TestInlineQuery.id_,
        TestInlineQuery.from_user,
        TestInlineQuery.query,
        TestInlineQuery.offset,
        location=TestInlineQuery.location,
        bot=bot,
    )


class TestInlineQuery:
    id_ = 1234
    from_user = User(1, 'First name', False)
    query = 'query text'
    offset = 'offset'
    location = Location(8.8, 53.1)

    def test_de_json(self, bot):
        json_dict = {
            'id': self.id_,
            'from': self.from_user.to_dict(),
            'query': self.query,
            'offset': self.offset,
            'location': self.location.to_dict(),
        }
        inline_query_json = InlineQuery.de_json(json_dict, bot)

        assert inline_query_json.id == self.id_
        assert inline_query_json.from_user == self.from_user
        assert inline_query_json.location == self.location
        assert inline_query_json.query == self.query
        assert inline_query_json.offset == self.offset

    def test_to_dict(self, inline_query):
        inline_query_dict = inline_query.to_dict()

        assert isinstance(inline_query_dict, dict)
        assert inline_query_dict['id'] == inline_query.id
        assert inline_query_dict['from'] == inline_query.from_user.to_dict()
        assert inline_query_dict['location'] == inline_query.location.to_dict()
        assert inline_query_dict['query'] == inline_query.query
        assert inline_query_dict['offset'] == inline_query.offset

    def test_answer(self, monkeypatch, inline_query):
        def test(*args, **kwargs):
            return args[0] == inline_query.id

        monkeypatch.setattr(inline_query.bot, 'answer_inline_query', test)
        assert inline_query.answer()

    def test_answer_auto_pagination(self, monkeypatch, inline_query):
        def make_assertion(*args, **kwargs):
            inline_query_id_matches = args[0] == inline_query.id
            offset_matches = kwargs.get('current_offset') == inline_query.offset
            return offset_matches and inline_query_id_matches

        monkeypatch.setattr(inline_query.bot, 'answer_inline_query', make_assertion)
        assert inline_query.answer(auto_pagination=True)

    def test_equality(self):
        a = InlineQuery(self.id_, User(1, '', False), '', '')
        b = InlineQuery(self.id_, User(1, '', False), '', '')
        c = InlineQuery(self.id_, User(0, '', False), '', '')
        d = InlineQuery(0, User(1, '', False), '', '')
        e = Update(self.id_)

        assert a == b
        assert hash(a) == hash(b)
        assert a is not b

        assert a == c
        assert hash(a) == hash(c)

        assert a != d
        assert hash(a) != hash(d)

        assert a != e
        assert hash(a) != hash(e)
