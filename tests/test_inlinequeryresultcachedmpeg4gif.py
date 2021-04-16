#!/usr/bin/env python


import pytest

from telegram import (
    InlineQueryResultCachedMpeg4Gif,
    InlineKeyboardButton,
    InputTextMessageContent,
    InlineKeyboardMarkup,
    InlineQueryResultCachedVoice,
    MessageEntity,
)


@pytest.fixture(scope='class')
def inline_query_result_cached_mpeg4_gif():
    return InlineQueryResultCachedMpeg4Gif(
        TestInlineQueryResultCachedMpeg4Gif.id_,
        TestInlineQueryResultCachedMpeg4Gif.mpeg4_file_id,
        title=TestInlineQueryResultCachedMpeg4Gif.title,
        caption=TestInlineQueryResultCachedMpeg4Gif.caption,
        parse_mode=TestInlineQueryResultCachedMpeg4Gif.parse_mode,
        caption_entities=TestInlineQueryResultCachedMpeg4Gif.caption_entities,
        input_message_content=TestInlineQueryResultCachedMpeg4Gif.input_message_content,
        reply_markup=TestInlineQueryResultCachedMpeg4Gif.reply_markup,
    )


class TestInlineQueryResultCachedMpeg4Gif:
    id_ = 'id'
    type_ = 'mpeg4_gif'
    mpeg4_file_id = 'mpeg4 file id'
    title = 'title'
    caption = 'caption'
    parse_mode = 'Markdown'
    caption_entities = [MessageEntity(MessageEntity.ITALIC, 0, 7)]
    input_message_content = InputTextMessageContent('input_message_content')
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('reply_markup')]])

    def test_expected_values(self, inline_query_result_cached_mpeg4_gif):
        assert inline_query_result_cached_mpeg4_gif.type == self.type_
        assert inline_query_result_cached_mpeg4_gif.id == self.id_
        assert inline_query_result_cached_mpeg4_gif.mpeg4_file_id == self.mpeg4_file_id
        assert inline_query_result_cached_mpeg4_gif.title == self.title
        assert inline_query_result_cached_mpeg4_gif.caption == self.caption
        assert inline_query_result_cached_mpeg4_gif.parse_mode == self.parse_mode
        assert inline_query_result_cached_mpeg4_gif.caption_entities == self.caption_entities
        assert (
            inline_query_result_cached_mpeg4_gif.input_message_content.to_dict()
            == self.input_message_content.to_dict()
        )
        assert (
            inline_query_result_cached_mpeg4_gif.reply_markup.to_dict()
            == self.reply_markup.to_dict()
        )

    def test_to_dict(self, inline_query_result_cached_mpeg4_gif):
        inline_query_result_cached_mpeg4_gif_dict = inline_query_result_cached_mpeg4_gif.to_dict()

        assert isinstance(inline_query_result_cached_mpeg4_gif_dict, dict)
        assert (
            inline_query_result_cached_mpeg4_gif_dict['type']
            == inline_query_result_cached_mpeg4_gif.type
        )
        assert (
            inline_query_result_cached_mpeg4_gif_dict['id']
            == inline_query_result_cached_mpeg4_gif.id
        )
        assert (
            inline_query_result_cached_mpeg4_gif_dict['mpeg4_file_id']
            == inline_query_result_cached_mpeg4_gif.mpeg4_file_id
        )
        assert (
            inline_query_result_cached_mpeg4_gif_dict['title']
            == inline_query_result_cached_mpeg4_gif.title
        )
        assert (
            inline_query_result_cached_mpeg4_gif_dict['caption']
            == inline_query_result_cached_mpeg4_gif.caption
        )
        assert (
            inline_query_result_cached_mpeg4_gif_dict['parse_mode']
            == inline_query_result_cached_mpeg4_gif.parse_mode
        )
        assert inline_query_result_cached_mpeg4_gif_dict['caption_entities'] == [
            ce.to_dict() for ce in inline_query_result_cached_mpeg4_gif.caption_entities
        ]
        assert (
            inline_query_result_cached_mpeg4_gif_dict['input_message_content']
            == inline_query_result_cached_mpeg4_gif.input_message_content.to_dict()
        )
        assert (
            inline_query_result_cached_mpeg4_gif_dict['reply_markup']
            == inline_query_result_cached_mpeg4_gif.reply_markup.to_dict()
        )

    def test_equality(self):
        a = InlineQueryResultCachedMpeg4Gif(self.id_, self.mpeg4_file_id)
        b = InlineQueryResultCachedMpeg4Gif(self.id_, self.mpeg4_file_id)
        c = InlineQueryResultCachedMpeg4Gif(self.id_, '')
        d = InlineQueryResultCachedMpeg4Gif('', self.mpeg4_file_id)
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
