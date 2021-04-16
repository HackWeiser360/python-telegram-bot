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
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InputTextMessageContent,
    InlineQueryResultCachedVideo,
    InlineQueryResultCachedVoice,
    MessageEntity,
)


@pytest.fixture(scope='class')
def inline_query_result_cached_video():
    return InlineQueryResultCachedVideo(
        TestInlineQueryResultCachedVideo.id_,
        TestInlineQueryResultCachedVideo.video_file_id,
        TestInlineQueryResultCachedVideo.title,
        caption=TestInlineQueryResultCachedVideo.caption,
        parse_mode=TestInlineQueryResultCachedVideo.parse_mode,
        caption_entities=TestInlineQueryResultCachedVideo.caption_entities,
        description=TestInlineQueryResultCachedVideo.description,
        input_message_content=TestInlineQueryResultCachedVideo.input_message_content,
        reply_markup=TestInlineQueryResultCachedVideo.reply_markup,
    )


class TestInlineQueryResultCachedVideo:
    id_ = 'id'
    type_ = 'video'
    video_file_id = 'video file id'
    title = 'title'
    caption = 'caption'
    parse_mode = 'Markdown'
    caption_entities = [MessageEntity(MessageEntity.ITALIC, 0, 7)]
    description = 'description'
    input_message_content = InputTextMessageContent('input_message_content')
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('reply_markup')]])

    def test_expected_values(self, inline_query_result_cached_video):
        assert inline_query_result_cached_video.type == self.type_
        assert inline_query_result_cached_video.id == self.id_
        assert inline_query_result_cached_video.video_file_id == self.video_file_id
        assert inline_query_result_cached_video.title == self.title
        assert inline_query_result_cached_video.description == self.description
        assert inline_query_result_cached_video.caption == self.caption
        assert inline_query_result_cached_video.parse_mode == self.parse_mode
        assert inline_query_result_cached_video.caption_entities == self.caption_entities
        assert (
            inline_query_result_cached_video.input_message_content.to_dict()
            == self.input_message_content.to_dict()
        )
        assert (
            inline_query_result_cached_video.reply_markup.to_dict() == self.reply_markup.to_dict()
        )

    def test_to_dict(self, inline_query_result_cached_video):
        inline_query_result_cached_video_dict = inline_query_result_cached_video.to_dict()

        assert isinstance(inline_query_result_cached_video_dict, dict)
        assert (
            inline_query_result_cached_video_dict['type'] == inline_query_result_cached_video.type
        )
        assert inline_query_result_cached_video_dict['id'] == inline_query_result_cached_video.id
        assert (
            inline_query_result_cached_video_dict['video_file_id']
            == inline_query_result_cached_video.video_file_id
        )
        assert (
            inline_query_result_cached_video_dict['title']
            == inline_query_result_cached_video.title
        )
        assert (
            inline_query_result_cached_video_dict['description']
            == inline_query_result_cached_video.description
        )
        assert (
            inline_query_result_cached_video_dict['caption']
            == inline_query_result_cached_video.caption
        )
        assert (
            inline_query_result_cached_video_dict['parse_mode']
            == inline_query_result_cached_video.parse_mode
        )
        assert inline_query_result_cached_video_dict['caption_entities'] == [
            ce.to_dict() for ce in inline_query_result_cached_video.caption_entities
        ]
        assert (
            inline_query_result_cached_video_dict['input_message_content']
            == inline_query_result_cached_video.input_message_content.to_dict()
        )
        assert (
            inline_query_result_cached_video_dict['reply_markup']
            == inline_query_result_cached_video.reply_markup.to_dict()
        )

    def test_equality(self):
        a = InlineQueryResultCachedVideo(self.id_, self.video_file_id, self.title)
        b = InlineQueryResultCachedVideo(self.id_, self.video_file_id, self.title)
        c = InlineQueryResultCachedVideo(self.id_, '', self.title)
        d = InlineQueryResultCachedVideo('', self.video_file_id, self.title)
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
