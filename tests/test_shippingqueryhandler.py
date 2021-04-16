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
    Update,
    Chat,
    Bot,
    ChosenInlineResult,
    User,
    Message,
    CallbackQuery,
    InlineQuery,
    ShippingQuery,
    PreCheckoutQuery,
    ShippingAddress,
)
from telegram.ext import ShippingQueryHandler, CallbackContext, JobQueue

message = Message(1, None, Chat(1, ''), from_user=User(1, '', False), text='Text')

params = [
    {'message': message},
    {'edited_message': message},
    {'callback_query': CallbackQuery(1, User(1, '', False), 'chat', message=message)},
    {'channel_post': message},
    {'edited_channel_post': message},
    {'inline_query': InlineQuery(1, User(1, '', False), '', '')},
    {'chosen_inline_result': ChosenInlineResult('id', User(1, '', False), '')},
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
    'pre_checkout_query',
    'callback_query_without_message',
)


@pytest.fixture(scope='class', params=params, ids=ids)
def false_update(request):
    return Update(update_id=1, **request.param)


@pytest.fixture(scope='class')
def shiping_query():
    return Update(
        1,
        shipping_query=ShippingQuery(
            42,
            User(1, 'test user', False),
            'invoice_payload',
            ShippingAddress('EN', 'my_state', 'my_city', 'steer_1', '', 'post_code'),
        ),
    )


class TestShippingQueryHandler:
    test_flag = False

    @pytest.fixture(autouse=True)
    def reset(self):
        self.test_flag = False

    def callback_basic(self, bot, update):
        test_bot = isinstance(bot, Bot)
        test_update = isinstance(update, Update)
        self.test_flag = test_bot and test_update

    def callback_data_1(self, bot, update, user_data=None, chat_data=None):
        self.test_flag = (user_data is not None) or (chat_data is not None)

    def callback_data_2(self, bot, update, user_data=None, chat_data=None):
        self.test_flag = (user_data is not None) and (chat_data is not None)

    def callback_queue_1(self, bot, update, job_queue=None, update_queue=None):
        self.test_flag = (job_queue is not None) or (update_queue is not None)

    def callback_queue_2(self, bot, update, job_queue=None, update_queue=None):
        self.test_flag = (job_queue is not None) and (update_queue is not None)

    def callback_context(self, update, context):
        self.test_flag = (
            isinstance(context, CallbackContext)
            and isinstance(context.bot, Bot)
            and isinstance(update, Update)
            and isinstance(context.update_queue, Queue)
            and isinstance(context.job_queue, JobQueue)
            and isinstance(context.user_data, dict)
            and context.chat_data is None
            and isinstance(context.bot_data, dict)
            and isinstance(update.shipping_query, ShippingQuery)
        )

    def test_basic(self, dp, shiping_query):
        handler = ShippingQueryHandler(self.callback_basic)
        dp.add_handler(handler)

        assert handler.check_update(shiping_query)
        dp.process_update(shiping_query)
        assert self.test_flag

    def test_pass_user_or_chat_data(self, dp, shiping_query):
        handler = ShippingQueryHandler(self.callback_data_1, pass_user_data=True)
        dp.add_handler(handler)

        dp.process_update(shiping_query)
        assert self.test_flag

        dp.remove_handler(handler)
        handler = ShippingQueryHandler(self.callback_data_1, pass_chat_data=True)
        dp.add_handler(handler)

        self.test_flag = False
        dp.process_update(shiping_query)
        assert self.test_flag

        dp.remove_handler(handler)
        handler = ShippingQueryHandler(
            self.callback_data_2, pass_chat_data=True, pass_user_data=True
        )
        dp.add_handler(handler)

        self.test_flag = False
        dp.process_update(shiping_query)
        assert self.test_flag

    def test_pass_job_or_update_queue(self, dp, shiping_query):
        handler = ShippingQueryHandler(self.callback_queue_1, pass_job_queue=True)
        dp.add_handler(handler)

        dp.process_update(shiping_query)
        assert self.test_flag

        dp.remove_handler(handler)
        handler = ShippingQueryHandler(self.callback_queue_1, pass_update_queue=True)
        dp.add_handler(handler)

        self.test_flag = False
        dp.process_update(shiping_query)
        assert self.test_flag

        dp.remove_handler(handler)
        handler = ShippingQueryHandler(
            self.callback_queue_2, pass_job_queue=True, pass_update_queue=True
        )
        dp.add_handler(handler)

        self.test_flag = False
        dp.process_update(shiping_query)
        assert self.test_flag

    def test_other_update_types(self, false_update):
        handler = ShippingQueryHandler(self.callback_basic)
        assert not handler.check_update(false_update)

    def test_context(self, cdp, shiping_query):
        handler = ShippingQueryHandler(self.callback_context)
        cdp.add_handler(handler)

        cdp.process_update(shiping_query)
        assert self.test_flag
