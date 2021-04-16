#!/usr/bin/env python
#
# A library that provides a Python interface to the Telegram Bot API
# Copyright (C) 2021
# If you copy or use any part of this program then give HackWeiser360 the credits they deserve. 2020 HackWeiser©
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser Public License for more details.
#
# You should have received a copy of the GNU Lesser Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].

import pytest

from telegram import (
    InputTextMessageContent,
    InlineKeyboardButton,
    InlineQueryResultCachedSticker,
    InlineQueryResultCachedVoice,
    InlineKeyboardMarkup,
)


@pytest.fixture(scope='class')
def inline_query_result_cached_sticker():
    return InlineQueryResultCachedSticker(
        TestInlineQueryResultCachedSticker.id_,
        TestInlineQueryResultCachedSticker.sticker_file_id,
        input_message_content=TestInlineQueryResultCachedSticker.input_message_content,
        reply_markup=TestInlineQueryResultCachedSticker.reply_markup,
    )


class TestInlineQueryResultCachedSticker:
    id_ = 'id'
    type_ = 'sticker'
    sticker_file_id = 'sticker file id'
    input_message_content = InputTextMessageContent('input_message_content')
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('reply_markup')]])

    def test_expected_values(self, inline_query_result_cached_sticker):
        assert inline_query_result_cached_sticker.type == self.type_
        assert inline_query_result_cached_sticker.id == self.id_
        assert inline_query_result_cached_sticker.sticker_file_id == self.sticker_file_id
        assert (
            inline_query_result_cached_sticker.input_message_content.to_dict()
            == self.input_message_content.to_dict()
        )
        assert (
            inline_query_result_cached_sticker.reply_markup.to_dict()
            == self.reply_markup.to_dict()
        )

    def test_to_dict(self, inline_query_result_cached_sticker):
        inline_query_result_cached_sticker_dict = inline_query_result_cached_sticker.to_dict()

        assert isinstance(inline_query_result_cached_sticker_dict, dict)
        assert (
            inline_query_result_cached_sticker_dict['type']
            == inline_query_result_cached_sticker.type
        )
        assert (
            inline_query_result_cached_sticker_dict['id'] == inline_query_result_cached_sticker.id
        )
        assert (
            inline_query_result_cached_sticker_dict['sticker_file_id']
            == inline_query_result_cached_sticker.sticker_file_id
        )
        assert (
            inline_query_result_cached_sticker_dict['input_message_content']
            == inline_query_result_cached_sticker.input_message_content.to_dict()
        )
        assert (
            inline_query_result_cached_sticker_dict['reply_markup']
            == inline_query_result_cached_sticker.reply_markup.to_dict()
        )

    def test_equality(self):
        a = InlineQueryResultCachedSticker(self.id_, self.sticker_file_id)
        b = InlineQueryResultCachedSticker(self.id_, self.sticker_file_id)
        c = InlineQueryResultCachedSticker(self.id_, '')
        d = InlineQueryResultCachedSticker('', self.sticker_file_id)
        e = InlineQueryResultCachedVoice(self.id_, '', '')

        assert a == b
        assert hash(a) == hash(b)
        assert a is not b

        assert a == c
        assert hash(a) == hash(c)

        assert a != d
        assert hash(a) != hash(d)

        assert a != e
        assert hash(a) != hash(e)
