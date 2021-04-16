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

from telegram import TelegramError
from telegram.utils.request import Request


def test_replaced_unprintable_char():
    """
    Clients can send arbitrary bytes in callback data.
    Make sure the correct error is raised in this case.
    """
    server_response = b'{"invalid utf-8": "\x80", "result": "KUKU"}'

    assert Request._parse(server_response) == 'KUKU'


def test_parse_illegal_json():
    """
    Clients can send arbitrary bytes in callback data.
    Make sure the correct error is raised in this case.
    """
    server_response = b'{"invalid utf-8": "\x80", result: "KUKU"}'

    with pytest.raises(TelegramError, match='Invalid server response'):
        Request._parse(server_response)
