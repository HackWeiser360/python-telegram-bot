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
from queue import Queue

import pytest

from telegram import (
    Bot,
    Update,
    Message,
    User,
    Chat,
    CallbackQuery,
    InlineQuery,
    ChosenInlineResult,
    ShippingQuery,
    PreCheckoutQuery,
)
from telegram.ext import StringCommandHandler, CallbackContext, JobQueue

message = Message(1, None, Chat(1, ''), from_user=User(1, '', False), text='Text')

params = [
    {'message': message},
    {'edited_message': message},
    {'callback_query': CallbackQuery(1, User(1, '', False), 'chat', message=message)},
    {'channel_post': message},
    {'edited_channel_post': message},
    {'inline_query': InlineQuery(1, User(1, '', False), '', '')},
    {'chosen_inline_result': ChosenInlineResult('id', User(1, '', False), '')},
    {'shipping_query': ShippingQuery('id', User(1, '', False), '', None)},
    {'pre_checkout_query': PreCheckoutQuery('id', User(1, '', False), '', 0, '')},
    {'callback_query': CallbackQuery(1, User(1, '', False), 'chat')},
]

ids = (
    'message',
    'edited_message',
    'callback_query',
    'channel_post',
    'edited_channel_post',
    'inline_query',
    'chosen_inline_result',
    'shipping_query',
    'pre_checkout_query',
    'callback_query_without_message',
)


@pytest.fixture(scope='class', params=params, ids=ids)
def false_update(request):
    return Update(update_id=1, **request.param)


class TestStringCommandHandler:
    test_flag = False

    @pytest.fixture(autouse=True)
    def reset(self):
        self.test_flag = False

    def callback_basic(self, bot, update):
        test_bot = isinstance(bot, Bot)
        test_update = isinstance(update, str)
        self.test_flag = test_bot and test_update

    def callback_queue_1(self, bot, update, job_queue=None, update_queue=None):
        self.test_flag = (job_queue is not None) or (update_queue is not None)

    def callback_queue_2(self, bot, update, job_queue=None, update_queue=None):
        self.test_flag = (job_queue is not None) and (update_queue is not None)

    def sch_callback_args(self, bot, update, args):
        if update == '/test':
            self.test_flag = len(args) == 0
        else:
            self.test_flag = args == ['one', 'two']

    def callback_context(self, update, context):
        self.test_flag = (
            isinstance(context, CallbackContext)
            and isinstance(context.bot, Bot)
            and isinstance(update, str)
            and isinstance(context.update_queue, Queue)
            and isinstance(context.job_queue, JobQueue)
            and context.user_data is None
            and context.chat_data is None
            and isinstance(context.bot_data, dict)
        )

    def callback_context_args(self, update, context):
        self.test_flag = context.args == ['one', 'two']

    def test_basic(self, dp):
        handler = StringCommandHandler('test', self.callback_basic)
        dp.add_handler(handler)

        check = handler.check_update('/test')
        assert check is not None and check is not False
        dp.process_update('/test')
        assert self.test_flag

        check = handler.check_update('/nottest')
        assert check is None or check is False
        check = handler.check_update('not /test in front')
        assert check is None or check is False
        check = handler.check_update('/test followed by text')
        assert check is not None and check is not False

    def test_pass_args(self, dp):
        handler = StringCommandHandler('test', self.sch_callback_args, pass_args=True)
        dp.add_handler(handler)

        dp.process_update('/test')
        assert self.test_flag

        self.test_flag = False
        dp.process_update('/test one two')
        assert self.test_flag

    def test_pass_job_or_update_queue(self, dp):
        handler = StringCommandHandler('test', self.callback_queue_1, pass_job_queue=True)
        dp.add_handler(handler)

        dp.process_update('/test')
        assert self.test_flag

        dp.remove_handler(handler)
        handler = StringCommandHandler('test', self.callback_queue_1, pass_update_queue=True)
        dp.add_handler(handler)

        self.test_flag = False
        dp.process_update('/test')
        assert self.test_flag

        dp.remove_handler(handler)
        handler = StringCommandHandler(
            'test', self.callback_queue_2, pass_job_queue=True, pass_update_queue=True
        )
        dp.add_handler(handler)

        self.test_flag = False
        dp.process_update('/test')
        assert self.test_flag

    def test_other_update_types(self, false_update):
        handler = StringCommandHandler('test', self.callback_basic)
        assert not handler.check_update(false_update)

    def test_context(self, cdp):
        handler = StringCommandHandler('test', self.callback_context)
        cdp.add_handler(handler)

        cdp.process_update('/test')
        assert self.test_flag

    def test_context_args(self, cdp):
        handler = StringCommandHandler('test', self.callback_context_args)
        cdp.add_handler(handler)

        cdp.process_update('/test')
        assert not self.test_flag

        cdp.process_update('/test one two')
        assert self.test_flag
