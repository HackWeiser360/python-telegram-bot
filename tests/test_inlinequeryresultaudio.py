#!/usr/bin/env python


import pytest

from telegram import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InlineQueryResultAudio,
    InputTextMessageContent,
    InlineQueryResultVoice,
    MessageEntity,
)


@pytest.fixture(scope='class')
def inline_query_result_audio():
    return InlineQueryResultAudio(
        TestInlineQueryResultAudio.id_,
        TestInlineQueryResultAudio.audio_url,
        TestInlineQueryResultAudio.title,
        performer=TestInlineQueryResultAudio.performer,
        audio_duration=TestInlineQueryResultAudio.audio_duration,
        caption=TestInlineQueryResultAudio.caption,
        parse_mode=TestInlineQueryResultAudio.parse_mode,
        caption_entities=TestInlineQueryResultAudio.caption_entities,
        input_message_content=TestInlineQueryResultAudio.input_message_content,
        reply_markup=TestInlineQueryResultAudio.reply_markup,
    )


class TestInlineQueryResultAudio:
    id_ = 'id'
    type_ = 'audio'
    audio_url = 'audio url'
    title = 'title'
    performer = 'performer'
    audio_duration = 'audio_duration'
    caption = 'caption'
    parse_mode = 'Markdown'
    caption_entities = [MessageEntity(MessageEntity.ITALIC, 0, 7)]
    input_message_content = InputTextMessageContent('input_message_content')
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('reply_markup')]])

    def test_expected_values(self, inline_query_result_audio):
        assert inline_query_result_audio.type == self.type_
        assert inline_query_result_audio.id == self.id_
        assert inline_query_result_audio.audio_url == self.audio_url
        assert inline_query_result_audio.title == self.title
        assert inline_query_result_audio.performer == self.performer
        assert inline_query_result_audio.audio_duration == self.audio_duration
        assert inline_query_result_audio.caption == self.caption
        assert inline_query_result_audio.parse_mode == self.parse_mode
        assert inline_query_result_audio.caption_entities == self.caption_entities
        assert (
            inline_query_result_audio.input_message_content.to_dict()
            == self.input_message_content.to_dict()
        )
        assert inline_query_result_audio.reply_markup.to_dict() == self.reply_markup.to_dict()

    def test_to_dict(self, inline_query_result_audio):
        inline_query_result_audio_dict = inline_query_result_audio.to_dict()

        assert isinstance(inline_query_result_audio_dict, dict)
        assert inline_query_result_audio_dict['type'] == inline_query_result_audio.type
        assert inline_query_result_audio_dict['id'] == inline_query_result_audio.id
        assert inline_query_result_audio_dict['audio_url'] == inline_query_result_audio.audio_url
        assert inline_query_result_audio_dict['title'] == inline_query_result_audio.title
        assert inline_query_result_audio_dict['performer'] == inline_query_result_audio.performer
        assert (
            inline_query_result_audio_dict['audio_duration']
            == inline_query_result_audio.audio_duration
        )
        assert inline_query_result_audio_dict['caption'] == inline_query_result_audio.caption
        assert inline_query_result_audio_dict['parse_mode'] == inline_query_result_audio.parse_mode
        assert inline_query_result_audio_dict['caption_entities'] == [
            ce.to_dict() for ce in inline_query_result_audio.caption_entities
        ]
        assert (
            inline_query_result_audio_dict['input_message_content']
            == inline_query_result_audio.input_message_content.to_dict()
        )
        assert (
            inline_query_result_audio_dict['reply_markup']
            == inline_query_result_audio.reply_markup.to_dict()
        )

    def test_equality(self):
        a = InlineQueryResultAudio(self.id_, self.audio_url, self.title)
        b = InlineQueryResultAudio(self.id_, self.title, self.title)
        c = InlineQueryResultAudio(self.id_, '', self.title)
        d = InlineQueryResultAudio('', self.audio_url, self.title)
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
