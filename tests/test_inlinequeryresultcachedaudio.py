#!/usr/bin/env python


import pytest

from telegram import (
    InputTextMessageContent,
    InlineQueryResultCachedAudio,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InlineQueryResultCachedVoice,
    MessageEntity,
)


@pytest.fixture(scope='class')
def inline_query_result_cached_audio():
    return InlineQueryResultCachedAudio(
        TestInlineQueryResultCachedAudio.id_,
        TestInlineQueryResultCachedAudio.audio_file_id,
        caption=TestInlineQueryResultCachedAudio.caption,
        parse_mode=TestInlineQueryResultCachedAudio.parse_mode,
        caption_entities=TestInlineQueryResultCachedAudio.caption_entities,
        input_message_content=TestInlineQueryResultCachedAudio.input_message_content,
        reply_markup=TestInlineQueryResultCachedAudio.reply_markup,
    )


class TestInlineQueryResultCachedAudio:
    id_ = 'id'
    type_ = 'audio'
    audio_file_id = 'audio file id'
    caption = 'caption'
    parse_mode = 'HTML'
    caption_entities = [MessageEntity(MessageEntity.ITALIC, 0, 7)]
    input_message_content = InputTextMessageContent('input_message_content')
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('reply_markup')]])

    def test_expected_values(self, inline_query_result_cached_audio):
        assert inline_query_result_cached_audio.type == self.type_
        assert inline_query_result_cached_audio.id == self.id_
        assert inline_query_result_cached_audio.audio_file_id == self.audio_file_id
        assert inline_query_result_cached_audio.caption == self.caption
        assert inline_query_result_cached_audio.parse_mode == self.parse_mode
        assert inline_query_result_cached_audio.caption_entities == self.caption_entities
        assert (
            inline_query_result_cached_audio.input_message_content.to_dict()
            == self.input_message_content.to_dict()
        )
        assert (
            inline_query_result_cached_audio.reply_markup.to_dict() == self.reply_markup.to_dict()
        )

    def test_to_dict(self, inline_query_result_cached_audio):
        inline_query_result_cached_audio_dict = inline_query_result_cached_audio.to_dict()

        assert isinstance(inline_query_result_cached_audio_dict, dict)
        assert (
            inline_query_result_cached_audio_dict['type'] == inline_query_result_cached_audio.type
        )
        assert inline_query_result_cached_audio_dict['id'] == inline_query_result_cached_audio.id
        assert (
            inline_query_result_cached_audio_dict['audio_file_id']
            == inline_query_result_cached_audio.audio_file_id
        )
        assert (
            inline_query_result_cached_audio_dict['caption']
            == inline_query_result_cached_audio.caption
        )
        assert (
            inline_query_result_cached_audio_dict['parse_mode']
            == inline_query_result_cached_audio.parse_mode
        )
        assert inline_query_result_cached_audio_dict['caption_entities'] == [
            ce.to_dict() for ce in inline_query_result_cached_audio.caption_entities
        ]
        assert (
            inline_query_result_cached_audio_dict['input_message_content']
            == inline_query_result_cached_audio.input_message_content.to_dict()
        )
        assert (
            inline_query_result_cached_audio_dict['reply_markup']
            == inline_query_result_cached_audio.reply_markup.to_dict()
        )

    def test_equality(self):
        a = InlineQueryResultCachedAudio(self.id_, self.audio_file_id)
        b = InlineQueryResultCachedAudio(self.id_, self.audio_file_id)
        c = InlineQueryResultCachedAudio(self.id_, '')
        d = InlineQueryResultCachedAudio('', self.audio_file_id)
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
