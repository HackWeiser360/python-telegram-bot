#!/usr/bin/env python
#

import pytest
from flaky import flaky

from telegram import constants
from telegram.error import BadRequest


class TestConstants:
    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_max_message_length(self, bot, chat_id):
        bot.send_message(chat_id=chat_id, text='a' * constants.MAX_MESSAGE_LENGTH)

        with pytest.raises(
            BadRequest,
            match='Message is too long',
            message='MAX_MESSAGE_LENGTH is no longer valid',
        ):
            bot.send_message(chat_id=chat_id, text='a' * (constants.MAX_MESSAGE_LENGTH + 1))

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_max_caption_length(self, bot, chat_id):
        good_caption = 'a' * constants.MAX_CAPTION_LENGTH
        with open('tests/data/telegram.png', 'rb') as f:
            good_msg = bot.send_photo(photo=f, caption=good_caption, chat_id=chat_id)
        assert good_msg.caption == good_caption

        bad_caption = good_caption + 'Z'
        with pytest.raises(
            BadRequest,
            match="Media_caption_too_long",
            message='MAX_CAPTION_LENGTH is no longer valid',
        ):
            with open('tests/data/telegram.png', 'rb') as f:
                bot.send_photo(photo=f, caption=bad_caption, chat_id=chat_id)
