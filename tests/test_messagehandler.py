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
import re
from queue import Queue

import pytest
from telegram.utils.deprecate import TelegramDeprecationWarning

from telegram import (
    Message,
    Update,
    Chat,
    Bot,
    User,
    CallbackQuery,
    InlineQuery,
    ChosenInlineResult,
    ShippingQuery,
    PreCheckoutQuery,
)
from telegram.ext import Filters, MessageHandler, CallbackContext, JobQueue, UpdateFilter

message = Message(1, None, Chat(1, ''), from_user=User(1, '', False), text='Text')

params = [
    {'callback_query': CallbackQuery(1, User(1, '', False), 'chat', message=message)},
    {'inline_query': InlineQuery(1, User(1, '', False), '', '')},
    {'chosen_inline_result': ChosenInlineResult('id', User(1, '', False), '')},
    {'shipping_query': ShippingQuery('id', User(1, '', False), '', None)},
    {'pre_checkout_query': PreCheckoutQuery('id', User(1, '', False), '', 0, '')},
    {'callback_query': CallbackQuery(1, User(1, '', False), 'chat')},
]

ids = (
    'callback_query',
    'inline_query',
    'chosen_inline_result',
    'shipping_query',
    'pre_checkout_query',
    'callback_query_without_message',
)


@pytest.fixture(scope='class', params=params, ids=ids)
def false_update(request):
    return Update(update_id=1, **request.param)


@pytest.fixture(scope='class')
def message(bot):
    return Message(1, None, Chat(1, ''), from_user=User(1, '', False), bot=bot)


class TestMessageHandler:
    test_flag = False
    SRE_TYPE = type(re.match("", ""))

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
            and isinstance(context.chat_data, dict)
            and isinstance(context.bot_data, dict)
            and (
                (
                    isinstance(context.user_data, dict)
                    and (
                        isinstance(update.message, Message)
                        or isinstance(update.edited_message, Message)
                    )
                )
                or (
                    context.user_data is None
                    and (
                        isinstance(update.channel_post, Message)
                        or isinstance(update.edited_channel_post, Message)
                    )
                )
            )
        )

    def callback_context_regex1(self, update, context):
        if context.matches:
            types = all([type(res) == self.SRE_TYPE for res in context.matches])
            num = len(context.matches) == 1
            self.test_flag = types and num

    def callback_context_regex2(self, update, context):
        if context.matches:
            types = all([type(res) == self.SRE_TYPE for res in context.matches])
            num = len(context.matches) == 2
            self.test_flag = types and num

    def test_basic(self, dp, message):
        handler = MessageHandler(None, self.callback_basic)
        dp.add_handler(handler)

        assert handler.check_update(Update(0, message))
        dp.process_update(Update(0, message))
        assert self.test_flag

    def test_deprecation_warning(self):
        with pytest.warns(TelegramDeprecationWarning, match='See https://git.io/fxJuV'):
            MessageHandler(None, self.callback_basic, edited_updates=True)
        with pytest.warns(TelegramDeprecationWarning, match='See https://git.io/fxJuV'):
            MessageHandler(None, self.callback_basic, message_updates=False)
        with pytest.warns(TelegramDeprecationWarning, match='See https://git.io/fxJuV'):
            MessageHandler(None, self.callback_basic, channel_post_updates=True)

    def test_edited_deprecated(self, message):
        handler = MessageHandler(
            None,
            self.callback_basic,
            edited_updates=True,
            message_updates=False,
            channel_post_updates=False,
        )

        assert handler.check_update(Update(0, edited_message=message))
        assert not handler.check_update(Update(0, message=message))
        assert not handler.check_update(Update(0, channel_post=message))
        assert handler.check_update(Update(0, edited_channel_post=message))

    def test_channel_post_deprecated(self, message):
        handler = MessageHandler(
            None,
            self.callback_basic,
            edited_updates=False,
            message_updates=False,
            channel_post_updates=True,
        )
        assert not handler.check_update(Update(0, edited_message=message))
        assert not handler.check_update(Update(0, message=message))
        assert handler.check_update(Update(0, channel_post=message))
        assert not handler.check_update(Update(0, edited_channel_post=message))

    def test_multiple_flags_deprecated(self, message):
        handler = MessageHandler(
            None,
            self.callback_basic,
            edited_updates=True,
            message_updates=True,
            channel_post_updates=True,
        )

        assert handler.check_update(Update(0, edited_message=message))
        assert handler.check_update(Update(0, message=message))
        assert handler.check_update(Update(0, channel_post=message))
        assert handler.check_update(Update(0, edited_channel_post=message))

    def test_none_allowed_deprecated(self):
        with pytest.raises(ValueError, match='are all False'):
            MessageHandler(
                None,
                self.callback_basic,
                message_updates=False,
                channel_post_updates=False,
                edited_updates=False,
            )

    def test_with_filter(self, message):
        handler = MessageHandler(Filters.group, self.callback_basic)

        message.chat.type = 'group'
        assert handler.check_update(Update(0, message))

        message.chat.type = 'private'
        assert not handler.check_update(Update(0, message))

    def test_callback_query_with_filter(self, message):
        class TestFilter(UpdateFilter):
            flag = False

            def filter(self, u):
                self.flag = True

        test_filter = TestFilter()
        handler = MessageHandler(test_filter, self.callback_basic)

        update = Update(1, callback_query=CallbackQuery(1, None, None, message=message))

        assert update.effective_message
        assert not handler.check_update(update)
        assert not test_filter.flag

    def test_specific_filters(self, message):
        f = (
            ~Filters.update.messages
            & ~Filters.update.channel_post
            & Filters.update.edited_channel_post
        )
        handler = MessageHandler(f, self.callback_basic)

        assert not handler.check_update(Update(0, edited_message=message))
        assert not handler.check_update(Update(0, message=message))
        assert not handler.check_update(Update(0, channel_post=message))
        assert handler.check_update(Update(0, edited_channel_post=message))

    def test_pass_user_or_chat_data(self, dp, message):
        handler = MessageHandler(None, self.callback_data_1, pass_user_data=True)
        dp.add_handler(handler)

        dp.process_update(Update(0, message=message))
        assert self.test_flag

        dp.remove_handler(handler)
        handler = MessageHandler(None, self.callback_data_1, pass_chat_data=True)
        dp.add_handler(handler)

        self.test_flag = False
        dp.process_update(Update(0, message=message))
        assert self.test_flag

        dp.remove_handler(handler)
        handler = MessageHandler(
            None, self.callback_data_2, pass_chat_data=True, pass_user_data=True
        )
        dp.add_handler(handler)

        self.test_flag = False
        dp.process_update(Update(0, message=message))
        assert self.test_flag

    def test_pass_job_or_update_queue(self, dp, message):
        handler = MessageHandler(None, self.callback_queue_1, pass_job_queue=True)
        dp.add_handler(handler)

        dp.process_update(Update(0, message=message))
        assert self.test_flag

        dp.remove_handler(handler)
        handler = MessageHandler(None, self.callback_queue_1, pass_update_queue=True)
        dp.add_handler(handler)

        self.test_flag = False
        dp.process_update(Update(0, message=message))
        assert self.test_flag

        dp.remove_handler(handler)
        handler = MessageHandler(
            None, self.callback_queue_2, pass_job_queue=True, pass_update_queue=True
        )
        dp.add_handler(handler)

        self.test_flag = False
        dp.process_update(Update(0, message=message))
        assert self.test_flag

    def test_other_update_types(self, false_update):
        handler = MessageHandler(None, self.callback_basic, edited_updates=True)
        assert not handler.check_update(false_update)

    def test_context(self, cdp, message):
        handler = MessageHandler(
            None, self.callback_context, edited_updates=True, channel_post_updates=True
        )
        cdp.add_handler(handler)

        cdp.process_update(Update(0, message=message))
        assert self.test_flag

        self.test_flag = False
        cdp.process_update(Update(0, edited_message=message))
        assert self.test_flag

        self.test_flag = False
        cdp.process_update(Update(0, channel_post=message))
        assert self.test_flag

        self.test_flag = False
        cdp.process_update(Update(0, edited_channel_post=message))
        assert self.test_flag

    def test_context_regex(self, cdp, message):
        handler = MessageHandler(Filters.regex('one two'), self.callback_context_regex1)
        cdp.add_handler(handler)

        message.text = 'not it'
        cdp.process_update(Update(0, message))
        assert not self.test_flag

        message.text += ' one two now it is'
        cdp.process_update(Update(0, message))
        assert self.test_flag

    def test_context_multiple_regex(self, cdp, message):
        handler = MessageHandler(
            Filters.regex('one') & Filters.regex('two'), self.callback_context_regex2
        )
        cdp.add_handler(handler)

        message.text = 'not it'
        cdp.process_update(Update(0, message))
        assert not self.test_flag

        message.text += ' one two now it is'
        cdp.process_update(Update(0, message))
        assert self.test_flag
