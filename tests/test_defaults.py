#!/usr/bin/env python
#


import pytest

from telegram.ext import Defaults
from telegram import User


class TestDefault:
    def test_data_assignment(self, cdp):
        defaults = Defaults()

        with pytest.raises(AttributeError):
            defaults.parse_mode = True
        with pytest.raises(AttributeError):
            defaults.disable_notification = True
        with pytest.raises(AttributeError):
            defaults.disable_web_page_preview = True
        with pytest.raises(AttributeError):
            defaults.allow_sending_without_reply = True
        with pytest.raises(AttributeError):
            defaults.timeout = True
        with pytest.raises(AttributeError):
            defaults.quote = True
        with pytest.raises(AttributeError):
            defaults.tzinfo = True
        with pytest.raises(AttributeError):
            defaults.run_async = True

    def test_equality(self):
        a = Defaults(parse_mode='HTML', quote=True)
        b = Defaults(parse_mode='HTML', quote=True)
        c = Defaults(parse_mode='HTML', quote=False)
        d = Defaults(parse_mode='HTML', timeout=50)
        e = User(123, 'test_user', False)

        assert a == b
        assert hash(a) == hash(b)
        assert a is not b

        assert a != c
        assert hash(a) != hash(c)

        assert a != d
        assert hash(a) != hash(d)

        assert a != e
        assert hash(a) != hash(e)
