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

from telegram import InputContactMessageContent, User


@pytest.fixture(scope='class')
def input_contact_message_content():
    return InputContactMessageContent(
        TestInputContactMessageContent.phone_number,
        TestInputContactMessageContent.first_name,
        last_name=TestInputContactMessageContent.last_name,
    )


class TestInputContactMessageContent:
    phone_number = 'phone number'
    first_name = 'first name'
    last_name = 'last name'

    def test_expected_values(self, input_contact_message_content):
        assert input_contact_message_content.first_name == self.first_name
        assert input_contact_message_content.phone_number == self.phone_number
        assert input_contact_message_content.last_name == self.last_name

    def test_to_dict(self, input_contact_message_content):
        input_contact_message_content_dict = input_contact_message_content.to_dict()

        assert isinstance(input_contact_message_content_dict, dict)
        assert (
            input_contact_message_content_dict['phone_number']
            == input_contact_message_content.phone_number
        )
        assert (
            input_contact_message_content_dict['first_name']
            == input_contact_message_content.first_name
        )
        assert (
            input_contact_message_content_dict['last_name']
            == input_contact_message_content.last_name
        )

    def test_equality(self):
        a = InputContactMessageContent('phone', 'first', last_name='last')
        b = InputContactMessageContent('phone', 'first_name', vcard='vcard')
        c = InputContactMessageContent('phone_number', 'first', vcard='vcard')
        d = User(123, 'first', False)

        assert a == b
        assert hash(a) == hash(b)

        assert a != c
        assert hash(a) != hash(c)

        assert a != d
        assert hash(a) != hash(d)
