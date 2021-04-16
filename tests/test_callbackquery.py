#!/usr/bin/env python


import pytest

from telegram import CallbackQuery, User, Message, Chat, Audio


@pytest.fixture(scope='class', params=['message', 'inline'])
def callback_query(bot, request):
    cbq = CallbackQuery(
        TestCallbackQuery.id_,
        TestCallbackQuery.from_user,
        TestCallbackQuery.chat_instance,
        data=TestCallbackQuery.data,
        game_short_name=TestCallbackQuery.game_short_name,
        bot=bot,
    )
    if request.param == 'message':
        cbq.message = TestCallbackQuery.message
        cbq.message.bot = bot
    else:
        cbq.inline_message_id = TestCallbackQuery.inline_message_id
    return cbq


class TestCallbackQuery:
    id_ = 'id'
    from_user = User(1, 'test_user', False)
    chat_instance = 'chat_instance'
    message = Message(3, None, Chat(4, 'private'), from_user=User(5, 'bot', False))
    data = 'data'
    inline_message_id = 'inline_message_id'
    game_short_name = 'the_game'

    def test_de_json(self, bot):
        json_dict = {
            'id': self.id_,
            'from': self.from_user.to_dict(),
            'chat_instance': self.chat_instance,
            'message': self.message.to_dict(),
            'data': self.data,
            'inline_message_id': self.inline_message_id,
            'game_short_name': self.game_short_name,
        }
        callback_query = CallbackQuery.de_json(json_dict, bot)

        assert callback_query.id == self.id_
        assert callback_query.from_user == self.from_user
        assert callback_query.chat_instance == self.chat_instance
        assert callback_query.message == self.message
        assert callback_query.data == self.data
        assert callback_query.inline_message_id == self.inline_message_id
        assert callback_query.game_short_name == self.game_short_name

    def test_to_dict(self, callback_query):
        callback_query_dict = callback_query.to_dict()

        assert isinstance(callback_query_dict, dict)
        assert callback_query_dict['id'] == callback_query.id
        assert callback_query_dict['from'] == callback_query.from_user.to_dict()
        assert callback_query_dict['chat_instance'] == callback_query.chat_instance
        if callback_query.message:
            assert callback_query_dict['message'] == callback_query.message.to_dict()
        else:
            assert callback_query_dict['inline_message_id'] == callback_query.inline_message_id
        assert callback_query_dict['data'] == callback_query.data
        assert callback_query_dict['game_short_name'] == callback_query.game_short_name

    def test_answer(self, monkeypatch, callback_query):
        def test(*args, **kwargs):
            return args[0] == callback_query.id

        monkeypatch.setattr(callback_query.bot, 'answer_callback_query', test)
        # TODO: PEP8
        assert callback_query.answer()

    def test_edit_message_text(self, monkeypatch, callback_query):
        def test(*args, **kwargs):
            text = args[0] == 'test'
            try:
                id_ = kwargs['inline_message_id'] == callback_query.inline_message_id
                return id_ and text
            except KeyError:
                chat_id = kwargs['chat_id'] == callback_query.message.chat_id
                message_id = kwargs['message_id'] == callback_query.message.message_id
                return chat_id and message_id and text

        monkeypatch.setattr(callback_query.bot, 'edit_message_text', test)
        assert callback_query.edit_message_text(text='test')
        assert callback_query.edit_message_text('test')

    def test_edit_message_caption(self, monkeypatch, callback_query):
        def test(*args, **kwargs):
            caption = kwargs['caption'] == 'new caption'
            try:
                id_ = kwargs['inline_message_id'] == callback_query.inline_message_id
                return id_ and caption
            except KeyError:
                id_ = kwargs['chat_id'] == callback_query.message.chat_id
                message = kwargs['message_id'] == callback_query.message.message_id
                return id_ and message and caption

        monkeypatch.setattr(callback_query.bot, 'edit_message_caption', test)
        assert callback_query.edit_message_caption(caption='new caption')
        assert callback_query.edit_message_caption('new caption')

    def test_edit_message_reply_markup(self, monkeypatch, callback_query):
        def test(*args, **kwargs):
            reply_markup = kwargs['reply_markup'] == [['1', '2']]
            try:
                id_ = kwargs['inline_message_id'] == callback_query.inline_message_id
                return id_ and reply_markup
            except KeyError:
                id_ = kwargs['chat_id'] == callback_query.message.chat_id
                message = kwargs['message_id'] == callback_query.message.message_id
                return id_ and message and reply_markup

        monkeypatch.setattr(callback_query.bot, 'edit_message_reply_markup', test)
        assert callback_query.edit_message_reply_markup(reply_markup=[['1', '2']])
        assert callback_query.edit_message_reply_markup([['1', '2']])

    def test_edit_message_media(self, monkeypatch, callback_query):
        def test(*args, **kwargs):
            message_media = kwargs.get('media') == [['1', '2']] or args[0] == [['1', '2']]
            try:
                id_ = kwargs['inline_message_id'] == callback_query.inline_message_id
                return id_ and message_media
            except KeyError:
                id_ = kwargs['chat_id'] == callback_query.message.chat_id
                message = kwargs['message_id'] == callback_query.message.message_id
                return id_ and message and message_media

        monkeypatch.setattr(callback_query.bot, 'edit_message_media', test)
        assert callback_query.edit_message_media(media=[['1', '2']])
        assert callback_query.edit_message_media([['1', '2']])

    def test_edit_message_live_location(self, monkeypatch, callback_query):
        def test(*args, **kwargs):
            latitude = kwargs.get('latitude') == 1 or args[0] == 1
            longitude = kwargs.get('longitude') == 2 or args[1] == 2
            try:
                id_ = kwargs['inline_message_id'] == callback_query.inline_message_id
                return id_ and latitude and longitude
            except KeyError:
                id_ = kwargs['chat_id'] == callback_query.message.chat_id
                message = kwargs['message_id'] == callback_query.message.message_id
                return id_ and message and latitude and longitude

        monkeypatch.setattr(callback_query.bot, 'edit_message_live_location', test)
        assert callback_query.edit_message_live_location(latitude=1, longitude=2)
        assert callback_query.edit_message_live_location(1, 2)

    def test_stop_message_live_location(self, monkeypatch, callback_query):
        def test(*args, **kwargs):
            try:
                id_ = kwargs['inline_message_id'] == callback_query.inline_message_id
                return id_
            except KeyError:
                id_ = kwargs['chat_id'] == callback_query.message.chat_id
                message = kwargs['message_id'] == callback_query.message.message_id
                return id_ and message

        monkeypatch.setattr(callback_query.bot, 'stop_message_live_location', test)
        assert callback_query.stop_message_live_location()

    def test_set_game_score(self, monkeypatch, callback_query):
        def test(*args, **kwargs):
            user_id = kwargs.get('user_id') == 1 or args[0] == 1
            score = kwargs.get('score') == 2 or args[1] == 2
            try:
                id_ = kwargs['inline_message_id'] == callback_query.inline_message_id
                return id_ and user_id and score
            except KeyError:
                id_ = kwargs['chat_id'] == callback_query.message.chat_id
                message = kwargs['message_id'] == callback_query.message.message_id
                return id_ and message and user_id and score

        monkeypatch.setattr(callback_query.bot, 'set_game_score', test)
        assert callback_query.set_game_score(user_id=1, score=2)
        assert callback_query.set_game_score(1, 2)

    def test_get_game_high_scores(self, monkeypatch, callback_query):
        def test(*args, **kwargs):
            user_id = kwargs.get('user_id') == 1 or args[0] == 1
            try:
                id_ = kwargs['inline_message_id'] == callback_query.inline_message_id
                return id_ and user_id
            except KeyError:
                id_ = kwargs['chat_id'] == callback_query.message.chat_id
                message = kwargs['message_id'] == callback_query.message.message_id
                return id_ and message and user_id

        monkeypatch.setattr(callback_query.bot, 'get_game_high_scores', test)
        assert callback_query.get_game_high_scores(user_id=1)
        assert callback_query.get_game_high_scores(1)

    def test_delete_message(self, monkeypatch, callback_query):
        if callback_query.inline_message_id:
            pytest.skip("Can't delete inline messages")

        def make_assertion(*args, **kwargs):
            id_ = kwargs['chat_id'] == callback_query.message.chat_id
            message = kwargs['message_id'] == callback_query.message.message_id
            return id_ and message

        monkeypatch.setattr(callback_query.bot, 'delete_message', make_assertion)
        assert callback_query.delete_message()

    def test_pin_message(self, monkeypatch, callback_query):
        if callback_query.inline_message_id:
            pytest.skip("Can't pin inline messages")

        def make_assertion(*args, **kwargs):
            _id = callback_query.message.chat_id
            try:
                return kwargs['chat_id'] == _id
            except KeyError:
                return args[0] == _id

        monkeypatch.setattr(callback_query.bot, 'pin_chat_message', make_assertion)
        assert callback_query.pin_message()

    def test_unpin_message(self, monkeypatch, callback_query):
        if callback_query.inline_message_id:
            pytest.skip("Can't unpin inline messages")

        def make_assertion(*args, **kwargs):
            _id = callback_query.message.chat_id
            try:
                return kwargs['chat_id'] == _id
            except KeyError:
                return args[0] == _id

        monkeypatch.setattr(callback_query.bot, 'unpin_chat_message', make_assertion)
        assert callback_query.unpin_message()

    def test_copy_message(self, monkeypatch, callback_query):
        if callback_query.inline_message_id:
            pytest.skip("Can't copy inline messages")

        def make_assertion(*args, **kwargs):
            id_ = kwargs['from_chat_id'] == callback_query.message.chat_id
            chat_id = kwargs['chat_id'] == 1
            message = kwargs['message_id'] == callback_query.message.message_id
            return id_ and message and chat_id

        monkeypatch.setattr(callback_query.bot, 'copy_message', make_assertion)
        assert callback_query.copy_message(1)

    def test_equality(self):
        a = CallbackQuery(self.id_, self.from_user, 'chat')
        b = CallbackQuery(self.id_, self.from_user, 'chat')
        c = CallbackQuery(self.id_, None, '')
        d = CallbackQuery('', None, 'chat')
        e = Audio(self.id_, 'unique_id', 1)

        assert a == b
        assert hash(a) == hash(b)
        assert a is not b

        assert a == c
        assert hash(a) == hash(c)

        assert a != d
        assert hash(a) != hash(d)

        assert a != e
        assert hash(a) != hash(e)
