#!/usr/bin/env python


import pytest

from telegram import (
    InlineQueryResultCachedDocument,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputTextMessageContent,
    InlineQueryResultCachedVoice,
    MessageEntity,
)


@pytest.fixture(scope='class')
def inline_query_result_cached_document():
    return InlineQueryResultCachedDocument(
        TestInlineQueryResultCachedDocument.id_,
        TestInlineQueryResultCachedDocument.title,
        TestInlineQueryResultCachedDocument.document_file_id,
        caption=TestInlineQueryResultCachedDocument.caption,
        parse_mode=TestInlineQueryResultCachedDocument.parse_mode,
        caption_entities=TestInlineQueryResultCachedDocument.caption_entities,
        description=TestInlineQueryResultCachedDocument.description,
        input_message_content=TestInlineQueryResultCachedDocument.input_message_content,
        reply_markup=TestInlineQueryResultCachedDocument.reply_markup,
    )


class TestInlineQueryResultCachedDocument:
    id_ = 'id'
    type_ = 'document'
    document_file_id = 'document file id'
    title = 'title'
    caption = 'caption'
    parse_mode = 'Markdown'
    caption_entities = [MessageEntity(MessageEntity.ITALIC, 0, 7)]
    description = 'description'
    input_message_content = InputTextMessageContent('input_message_content')
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('reply_markup')]])

    def test_expected_values(self, inline_query_result_cached_document):
        assert inline_query_result_cached_document.id == self.id_
        assert inline_query_result_cached_document.type == self.type_
        assert inline_query_result_cached_document.document_file_id == self.document_file_id
        assert inline_query_result_cached_document.title == self.title
        assert inline_query_result_cached_document.caption == self.caption
        assert inline_query_result_cached_document.parse_mode == self.parse_mode
        assert inline_query_result_cached_document.caption_entities == self.caption_entities
        assert inline_query_result_cached_document.description == self.description
        assert (
            inline_query_result_cached_document.input_message_content.to_dict()
            == self.input_message_content.to_dict()
        )
        assert (
            inline_query_result_cached_document.reply_markup.to_dict()
            == self.reply_markup.to_dict()
        )

    def test_to_dict(self, inline_query_result_cached_document):
        inline_query_result_cached_document_dict = inline_query_result_cached_document.to_dict()

        assert isinstance(inline_query_result_cached_document_dict, dict)
        assert (
            inline_query_result_cached_document_dict['id']
            == inline_query_result_cached_document.id
        )
        assert (
            inline_query_result_cached_document_dict['type']
            == inline_query_result_cached_document.type
        )
        assert (
            inline_query_result_cached_document_dict['document_file_id']
            == inline_query_result_cached_document.document_file_id
        )
        assert (
            inline_query_result_cached_document_dict['title']
            == inline_query_result_cached_document.title
        )
        assert (
            inline_query_result_cached_document_dict['caption']
            == inline_query_result_cached_document.caption
        )
        assert (
            inline_query_result_cached_document_dict['parse_mode']
            == inline_query_result_cached_document.parse_mode
        )
        assert inline_query_result_cached_document_dict['caption_entities'] == [
            ce.to_dict() for ce in inline_query_result_cached_document.caption_entities
        ]
        assert (
            inline_query_result_cached_document_dict['description']
            == inline_query_result_cached_document.description
        )
        assert (
            inline_query_result_cached_document_dict['input_message_content']
            == inline_query_result_cached_document.input_message_content.to_dict()
        )
        assert (
            inline_query_result_cached_document_dict['reply_markup']
            == inline_query_result_cached_document.reply_markup.to_dict()
        )

    def test_equality(self):
        a = InlineQueryResultCachedDocument(self.id_, self.title, self.document_file_id)
        b = InlineQueryResultCachedDocument(self.id_, self.title, self.document_file_id)
        c = InlineQueryResultCachedDocument(self.id_, self.title, '')
        d = InlineQueryResultCachedDocument('', self.title, self.document_file_id)
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
