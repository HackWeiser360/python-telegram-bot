#!/usr/bin/env python


import pytest
from flaky import flaky

from telegram import ForceReply, ReplyKeyboardRemove


@pytest.fixture(scope='class')
def force_reply():
    return ForceReply(TestForceReply.force_reply, TestForceReply.selective)


class TestForceReply:
    force_reply = True
    selective = True

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_send_message_with_force_reply(self, bot, chat_id, force_reply):
        message = bot.send_message(chat_id, 'text', reply_markup=force_reply)

        assert message.text == 'text'

    def test_expected(self, force_reply):
        assert force_reply.force_reply == self.force_reply
        assert force_reply.selective == self.selective

    def test_to_dict(self, force_reply):
        force_reply_dict = force_reply.to_dict()

        assert isinstance(force_reply_dict, dict)
        assert force_reply_dict['force_reply'] == force_reply.force_reply
        assert force_reply_dict['selective'] == force_reply.selective

    def test_equality(self):
        a = ForceReply(True, False)
        b = ForceReply(False, False)
        c = ForceReply(True, True)
        d = ReplyKeyboardRemove()

        assert a == b
        assert hash(a) == hash(b)

        assert a != c
        assert hash(a) != hash(c)

        assert a != d
        assert hash(a) != hash(d)
