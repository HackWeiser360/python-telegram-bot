#!/usr/bin/env python


import pytest

from telegram import (
    InlineKeyboardButton,
    InputTextMessageContent,
    InlineQueryResultCachedVoice,
    InlineKeyboardMarkup,
    InlineQueryResultCachedGif,
    MessageEntity,
)


@pytest.fixture(scope='class')
def inline_query_result_cached_gif():
    return InlineQueryResultCachedGif(
        TestInlineQueryResultCachedGif.id_,
        TestInlineQueryResultCachedGif.gif_file_id,
        title=TestInlineQueryResultCachedGif.title,
        caption=TestInlineQueryResultCachedGif.caption,
        parse_mode=TestInlineQueryResultCachedGif.parse_mode,
        caption_entities=TestInlineQueryResultCachedGif.caption_entities,
        input_message_content=TestInlineQueryResultCachedGif.input_message_content,
        reply_markup=TestInlineQueryResultCachedGif.reply_markup,
    )


class TestInlineQueryResultCachedGif:
    id_ = 'id'
    type_ = 'gif'
    gif_file_id = 'gif file id'
    title = 'title'
    caption = 'caption'
    parse_mode = 'HTML'
    caption_entities = [MessageEntity(MessageEntity.ITALIC, 0, 7)]
    input_message_content = InputTextMessageContent('input_message_content')
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('reply_markup')]])

    def test_expected_values(self, inline_query_result_cached_gif):
        assert inline_query_result_cached_gif.type == self.type_
        assert inline_query_result_cached_gif.id == self.id_
        assert inline_query_result_cached_gif.gif_file_id == self.gif_file_id
        assert inline_query_result_cached_gif.title == self.title
        assert inline_query_result_cached_gif.caption == self.caption
        assert inline_query_result_cached_gif.parse_mode == self.parse_mode
        assert inline_query_result_cached_gif.caption_entities == self.caption_entities
        assert (
            inline_query_result_cached_gif.input_message_content.to_dict()
            == self.input_message_content.to_dict()
        )
        assert inline_query_result_cached_gif.reply_markup.to_dict() == self.reply_markup.to_dict()

    def test_to_dict(self, inline_query_result_cached_gif):
        inline_query_result_cached_gif_dict = inline_query_result_cached_gif.to_dict()

        assert isinstance(inline_query_result_cached_gif_dict, dict)
        assert inline_query_result_cached_gif_dict['type'] == inline_query_result_cached_gif.type
        assert inline_query_result_cached_gif_dict['id'] == inline_query_result_cached_gif.id
        assert (
            inline_query_result_cached_gif_dict['gif_file_id']
            == inline_query_result_cached_gif.gif_file_id
        )
        assert inline_query_result_cached_gif_dict['title'] == inline_query_result_cached_gif.title
        assert (
            inline_query_result_cached_gif_dict['caption']
            == inline_query_result_cached_gif.caption
        )
        assert (
            inline_query_result_cached_gif_dict['parse_mode']
            == inline_query_result_cached_gif.parse_mode
        )
        assert inline_query_result_cached_gif_dict['caption_entities'] == [
            ce.to_dict() for ce in inline_query_result_cached_gif.caption_entities
        ]
        assert (
            inline_query_result_cached_gif_dict['input_message_content']
            == inline_query_result_cached_gif.input_message_content.to_dict()
        )
        assert (
            inline_query_result_cached_gif_dict['reply_markup']
            == inline_query_result_cached_gif.reply_markup.to_dict()
        )

    def test_equality(self):
        a = InlineQueryResultCachedGif(self.id_, self.gif_file_id)
        b = InlineQueryResultCachedGif(self.id_, self.gif_file_id)
        c = InlineQueryResultCachedGif(self.id_, '')
        d = InlineQueryResultCachedGif('', self.gif_file_id)
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
