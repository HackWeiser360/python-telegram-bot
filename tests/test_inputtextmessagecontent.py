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

from telegram import InputTextMessageContent, ParseMode, MessageEntity


@pytest.fixture(scope='class')
def input_text_message_content():
    return InputTextMessageContent(
        TestInputTextMessageContent.message_text,
        parse_mode=TestInputTextMessageContent.parse_mode,
        entities=TestInputTextMessageContent.entities,
        disable_web_page_preview=TestInputTextMessageContent.disable_web_page_preview,
    )


class TestInputTextMessageContent:
    message_text = '*message text*'
    parse_mode = ParseMode.MARKDOWN
    entities = [MessageEntity(MessageEntity.ITALIC, 0, 7)]
    disable_web_page_preview = True

    def test_expected_values(self, input_text_message_content):
        assert input_text_message_content.parse_mode == self.parse_mode
        assert input_text_message_content.message_text == self.message_text
        assert input_text_message_content.disable_web_page_preview == self.disable_web_page_preview
        assert input_text_message_content.entities == self.entities

    def test_to_dict(self, input_text_message_content):
        input_text_message_content_dict = input_text_message_content.to_dict()

        assert isinstance(input_text_message_content_dict, dict)
        assert (
            input_text_message_content_dict['message_text']
            == input_text_message_content.message_text
        )
        assert (
            input_text_message_content_dict['parse_mode'] == input_text_message_content.parse_mode
        )
        assert input_text_message_content_dict['entities'] == [
            ce.to_dict() for ce in input_text_message_content.entities
        ]
        assert (
            input_text_message_content_dict['disable_web_page_preview']
            == input_text_message_content.disable_web_page_preview
        )

    def test_equality(self):
        a = InputTextMessageContent('text')
        b = InputTextMessageContent('text', parse_mode=ParseMode.HTML)
        c = InputTextMessageContent('label')
        d = ParseMode.HTML

        assert a == b
        assert hash(a) == hash(b)

        assert a != c
        assert hash(a) != hash(c)

        assert a != d
        assert hash(a) != hash(d)
