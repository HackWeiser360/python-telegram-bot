#!/usr/bin/env python


import pytest

from telegram import (
    InputTextMessageContent,
    InlineQueryResultCachedPhoto,
    InlineKeyboardButton,
    InlineQueryResultCachedVoice,
    InlineKeyboardMarkup,
    MessageEntity,
)


@pytest.fixture(scope='class')
def inline_query_result_cached_photo():
    return InlineQueryResultCachedPhoto(
        TestInlineQueryResultCachedPhoto.id_,
        TestInlineQueryResultCachedPhoto.photo_file_id,
        title=TestInlineQueryResultCachedPhoto.title,
        description=TestInlineQueryResultCachedPhoto.description,
        caption=TestInlineQueryResultCachedPhoto.caption,
        parse_mode=TestInlineQueryResultCachedPhoto.parse_mode,
        caption_entities=TestInlineQueryResultCachedPhoto.caption_entities,
        input_message_content=TestInlineQueryResultCachedPhoto.input_message_content,
        reply_markup=TestInlineQueryResultCachedPhoto.reply_markup,
    )


class TestInlineQueryResultCachedPhoto:
    id_ = 'id'
    type_ = 'photo'
    photo_file_id = 'photo file id'
    title = 'title'
    description = 'description'
    caption = 'caption'
    parse_mode = 'HTML'
    caption_entities = [MessageEntity(MessageEntity.ITALIC, 0, 7)]
    input_message_content = InputTextMessageContent('input_message_content')
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('reply_markup')]])

    def test_expected_values(self, inline_query_result_cached_photo):
        assert inline_query_result_cached_photo.type == self.type_
        assert inline_query_result_cached_photo.id == self.id_
        assert inline_query_result_cached_photo.photo_file_id == self.photo_file_id
        assert inline_query_result_cached_photo.title == self.title
        assert inline_query_result_cached_photo.description == self.description
        assert inline_query_result_cached_photo.caption == self.caption
        assert inline_query_result_cached_photo.parse_mode == self.parse_mode
        assert inline_query_result_cached_photo.caption_entities == self.caption_entities
        assert (
            inline_query_result_cached_photo.input_message_content.to_dict()
            == self.input_message_content.to_dict()
        )
        assert (
            inline_query_result_cached_photo.reply_markup.to_dict() == self.reply_markup.to_dict()
        )

    def test_to_dict(self, inline_query_result_cached_photo):
        inline_query_result_cached_photo_dict = inline_query_result_cached_photo.to_dict()

        assert isinstance(inline_query_result_cached_photo_dict, dict)
        assert (
            inline_query_result_cached_photo_dict['type'] == inline_query_result_cached_photo.type
        )
        assert inline_query_result_cached_photo_dict['id'] == inline_query_result_cached_photo.id
        assert (
            inline_query_result_cached_photo_dict['photo_file_id']
            == inline_query_result_cached_photo.photo_file_id
        )
        assert (
            inline_query_result_cached_photo_dict['title']
            == inline_query_result_cached_photo.title
        )
        assert (
            inline_query_result_cached_photo_dict['description']
            == inline_query_result_cached_photo.description
        )
        assert (
            inline_query_result_cached_photo_dict['caption']
            == inline_query_result_cached_photo.caption
        )
        assert (
            inline_query_result_cached_photo_dict['parse_mode']
            == inline_query_result_cached_photo.parse_mode
        )
        assert inline_query_result_cached_photo_dict['caption_entities'] == [
            ce.to_dict() for ce in inline_query_result_cached_photo.caption_entities
        ]
        assert (
            inline_query_result_cached_photo_dict['input_message_content']
            == inline_query_result_cached_photo.input_message_content.to_dict()
        )
        assert (
            inline_query_result_cached_photo_dict['reply_markup']
            == inline_query_result_cached_photo.reply_markup.to_dict()
        )

    def test_equality(self):
        a = InlineQueryResultCachedPhoto(self.id_, self.photo_file_id)
        b = InlineQueryResultCachedPhoto(self.id_, self.photo_file_id)
        c = InlineQueryResultCachedPhoto(self.id_, '')
        d = InlineQueryResultCachedPhoto('', self.photo_file_id)
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
