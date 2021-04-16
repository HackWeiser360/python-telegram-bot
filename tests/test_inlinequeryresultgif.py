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
    InlineKeyboardButton,
    InputTextMessageContent,
    InlineQueryResultGif,
    InlineQueryResultVoice,
    InlineKeyboardMarkup,
    MessageEntity,
)


@pytest.fixture(scope='class')
def inline_query_result_gif():
    return InlineQueryResultGif(
        TestInlineQueryResultGif.id_,
        TestInlineQueryResultGif.gif_url,
        TestInlineQueryResultGif.thumb_url,
        gif_width=TestInlineQueryResultGif.gif_width,
        gif_height=TestInlineQueryResultGif.gif_height,
        gif_duration=TestInlineQueryResultGif.gif_duration,
        title=TestInlineQueryResultGif.title,
        caption=TestInlineQueryResultGif.caption,
        parse_mode=TestInlineQueryResultGif.parse_mode,
        caption_entities=TestInlineQueryResultGif.caption_entities,
        input_message_content=TestInlineQueryResultGif.input_message_content,
        reply_markup=TestInlineQueryResultGif.reply_markup,
        thumb_mime_type=TestInlineQueryResultGif.thumb_mime_type,
    )


class TestInlineQueryResultGif:
    id_ = 'id'
    type_ = 'gif'
    gif_url = 'gif url'
    gif_width = 10
    gif_height = 15
    gif_duration = 1
    thumb_url = 'thumb url'
    thumb_mime_type = 'image/jpeg'
    title = 'title'
    caption = 'caption'
    parse_mode = 'HTML'
    caption_entities = [MessageEntity(MessageEntity.ITALIC, 0, 7)]
    input_message_content = InputTextMessageContent('input_message_content')
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('reply_markup')]])

    def test_expected_values(self, inline_query_result_gif):
        assert inline_query_result_gif.type == self.type_
        assert inline_query_result_gif.id == self.id_
        assert inline_query_result_gif.gif_url == self.gif_url
        assert inline_query_result_gif.gif_width == self.gif_width
        assert inline_query_result_gif.gif_height == self.gif_height
        assert inline_query_result_gif.gif_duration == self.gif_duration
        assert inline_query_result_gif.thumb_url == self.thumb_url
        assert inline_query_result_gif.thumb_mime_type == self.thumb_mime_type
        assert inline_query_result_gif.title == self.title
        assert inline_query_result_gif.caption == self.caption
        assert inline_query_result_gif.parse_mode == self.parse_mode
        assert inline_query_result_gif.caption_entities == self.caption_entities
        assert (
            inline_query_result_gif.input_message_content.to_dict()
            == self.input_message_content.to_dict()
        )
        assert inline_query_result_gif.reply_markup.to_dict() == self.reply_markup.to_dict()

    def test_to_dict(self, inline_query_result_gif):
        inline_query_result_gif_dict = inline_query_result_gif.to_dict()

        assert isinstance(inline_query_result_gif_dict, dict)
        assert inline_query_result_gif_dict['type'] == inline_query_result_gif.type
        assert inline_query_result_gif_dict['id'] == inline_query_result_gif.id
        assert inline_query_result_gif_dict['gif_url'] == inline_query_result_gif.gif_url
        assert inline_query_result_gif_dict['gif_width'] == inline_query_result_gif.gif_width
        assert inline_query_result_gif_dict['gif_height'] == inline_query_result_gif.gif_height
        assert inline_query_result_gif_dict['gif_duration'] == inline_query_result_gif.gif_duration
        assert inline_query_result_gif_dict['thumb_url'] == inline_query_result_gif.thumb_url
        assert (
            inline_query_result_gif_dict['thumb_mime_type']
            == inline_query_result_gif.thumb_mime_type
        )
        assert inline_query_result_gif_dict['title'] == inline_query_result_gif.title
        assert inline_query_result_gif_dict['caption'] == inline_query_result_gif.caption
        assert inline_query_result_gif_dict['parse_mode'] == inline_query_result_gif.parse_mode
        assert inline_query_result_gif_dict['caption_entities'] == [
            ce.to_dict() for ce in inline_query_result_gif.caption_entities
        ]
        assert (
            inline_query_result_gif_dict['input_message_content']
            == inline_query_result_gif.input_message_content.to_dict()
        )
        assert (
            inline_query_result_gif_dict['reply_markup']
            == inline_query_result_gif.reply_markup.to_dict()
        )

    def test_equality(self):
        a = InlineQueryResultGif(self.id_, self.gif_url, self.thumb_url)
        b = InlineQueryResultGif(self.id_, self.gif_url, self.thumb_url)
        c = InlineQueryResultGif(self.id_, '', self.thumb_url)
        d = InlineQueryResultGif('', self.gif_url, self.thumb_url)
        e = InlineQueryResultVoice(self.id_, '', '')

        assert a == b
        assert hash(a) == hash(b)
        assert a is not b

        assert a == c
        assert hash(a) == hash(c)

        assert a != d
        assert hash(a) != hash(d)

        assert a != e
        assert hash(a) != hash(e)
