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
from collections import OrderedDict
from queue import Queue

import pytest

from telegram import Bot
from telegram.ext import TypeHandler, CallbackContext, JobQueue


class TestTypeHandler:
    test_flag = False

    @pytest.fixture(autouse=True)
    def reset(self):
        self.test_flag = False

    def callback_basic(self, bot, update):
        test_bot = isinstance(bot, Bot)
        test_update = isinstance(update, dict)
        self.test_flag = test_bot and test_update

    def callback_queue_1(self, bot, update, job_queue=None, update_queue=None):
        self.test_flag = (job_queue is not None) or (update_queue is not None)

    def callback_queue_2(self, bot, update, job_queue=None, update_queue=None):
        self.test_flag = (job_queue is not None) and (update_queue is not None)

    def callback_context(self, update, context):
        self.test_flag = (
            isinstance(context, CallbackContext)
            and isinstance(context.bot, Bot)
            and isinstance(update, dict)
            and isinstance(context.update_queue, Queue)
            and isinstance(context.job_queue, JobQueue)
            and context.user_data is None
            and context.chat_data is None
            and isinstance(context.bot_data, dict)
        )

    def test_basic(self, dp):
        handler = TypeHandler(dict, self.callback_basic)
        dp.add_handler(handler)

        assert handler.check_update({'a': 1, 'b': 2})
        assert not handler.check_update('not a dict')
        dp.process_update({'a': 1, 'b': 2})
        assert self.test_flag

    def test_strict(self):
        handler = TypeHandler(dict, self.callback_basic, strict=True)
        o = OrderedDict({'a': 1, 'b': 2})
        assert handler.check_update({'a': 1, 'b': 2})
        assert not handler.check_update(o)

    def test_pass_job_or_update_queue(self, dp):
        handler = TypeHandler(dict, self.callback_queue_1, pass_job_queue=True)
        dp.add_handler(handler)

        dp.process_update({'a': 1, 'b': 2})
        assert self.test_flag

        dp.remove_handler(handler)
        handler = TypeHandler(dict, self.callback_queue_1, pass_update_queue=True)
        dp.add_handler(handler)

        self.test_flag = False
        dp.process_update({'a': 1, 'b': 2})
        assert self.test_flag

        dp.remove_handler(handler)
        handler = TypeHandler(
            dict, self.callback_queue_2, pass_job_queue=True, pass_update_queue=True
        )
        dp.add_handler(handler)

        self.test_flag = False
        dp.process_update({'a': 1, 'b': 2})
        assert self.test_flag

    def test_context(self, cdp):
        handler = TypeHandler(dict, self.callback_context)
        cdp.add_handler(handler)

        cdp.process_update({'a': 1, 'b': 2})
        assert self.test_flag
