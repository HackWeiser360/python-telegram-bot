#!/usr/bin/env python

from queue import Queue

import pytest

from telegram import (
    Update,
    CallbackQuery,
    Bot,
    Message,
    User,
    Chat,
    InlineQuery,
    ChosenInlineResult,
    ShippingQuery,
    PreCheckoutQuery,
)
from telegram.ext import CallbackQueryHandler, CallbackContext, JobQueue

message = Message(1, None, Chat(1, ''), from_user=User(1, '', False), text='Text')

params = [
    {'message': message},
    {'edited_message': message},
    {'channel_post': message},
    {'edited_channel_post': message},
    {'inline_query': InlineQuery(1, User(1, '', False), '', '')},
    {'chosen_inline_result': ChosenInlineResult('id', User(1, '', False), '')},
    {'shipping_query': ShippingQuery('id', User(1, '', False), '', None)},
    {'pre_checkout_query': PreCheckoutQuery('id', User(1, '', False), '', 0, '')},
]

ids = (
    'message',
    'edited_message',
    'channel_post',
    'edited_channel_post',
    'inline_query',
    'chosen_inline_result',
    'shipping_query',
    'pre_checkout_query',
)


@pytest.fixture(scope='class', params=params, ids=ids)
def false_update(request):
    return Update(update_id=2, **request.param)


@pytest.fixture(scope='function')
def callback_query(bot):
    return Update(0, callback_query=CallbackQuery(2, User(1, '', False), None, data='test data'))


class TestCallbackQueryHandler:
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

    def callback_group(self, bot, update, groups=None, groupdict=None):
        if groups is not None:
            self.test_flag = groups == ('t', ' data')
        if groupdict is not None:
            self.test_flag = groupdict == {'begin': 't', 'end': ' data'}

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
            and isinstance(update.callback_query, CallbackQuery)
        )

    def callback_context_pattern(self, update, context):
        if context.matches[0].groups():
            self.test_flag = context.matches[0].groups() == ('t', ' data')
        if context.matches[0].groupdict():
            self.test_flag = context.matches[0].groupdict() == {'begin': 't', 'end': ' data'}

    def test_basic(self, dp, callback_query):
        handler = CallbackQueryHandler(self.callback_basic)
        dp.add_handler(handler)

        assert handler.check_update(callback_query)

        dp.process_update(callback_query)
        assert self.test_flag

    def test_with_pattern(self, callback_query):
        handler = CallbackQueryHandler(self.callback_basic, pattern='.*est.*')

        assert handler.check_update(callback_query)

        callback_query.callback_query.data = 'nothing here'
        assert not handler.check_update(callback_query)

    def test_with_passing_group_dict(self, dp, callback_query):
        handler = CallbackQueryHandler(
            self.callback_group, pattern='(?P<begin>.*)est(?P<end>.*)', pass_groups=True
        )
        dp.add_handler(handler)

        dp.process_update(callback_query)
        assert self.test_flag

        dp.remove_handler(handler)
        handler = CallbackQueryHandler(
            self.callback_group, pattern='(?P<begin>.*)est(?P<end>.*)', pass_groupdict=True
        )
        dp.add_handler(handler)

        self.test_flag = False
        dp.process_update(callback_query)
        assert self.test_flag

    def test_pass_user_or_chat_data(self, dp, callback_query):
        handler = CallbackQueryHandler(self.callback_data_1, pass_user_data=True)
        dp.add_handler(handler)

        dp.process_update(callback_query)
        assert self.test_flag

        dp.remove_handler(handler)
        handler = CallbackQueryHandler(self.callback_data_1, pass_chat_data=True)
        dp.add_handler(handler)

        self.test_flag = False
        dp.process_update(callback_query)
        assert self.test_flag

        dp.remove_handler(handler)
        handler = CallbackQueryHandler(
            self.callback_data_2, pass_chat_data=True, pass_user_data=True
        )
        dp.add_handler(handler)

        self.test_flag = False
        dp.process_update(callback_query)
        assert self.test_flag

    def test_pass_job_or_update_queue(self, dp, callback_query):
        handler = CallbackQueryHandler(self.callback_queue_1, pass_job_queue=True)
        dp.add_handler(handler)

        dp.process_update(callback_query)
        assert self.test_flag

        dp.remove_handler(handler)
        handler = CallbackQueryHandler(self.callback_queue_1, pass_update_queue=True)
        dp.add_handler(handler)

        self.test_flag = False
        dp.process_update(callback_query)
        assert self.test_flag

        dp.remove_handler(handler)
        handler = CallbackQueryHandler(
            self.callback_queue_2, pass_job_queue=True, pass_update_queue=True
        )
        dp.add_handler(handler)

        self.test_flag = False
        dp.process_update(callback_query)
        assert self.test_flag

    def test_other_update_types(self, false_update):
        handler = CallbackQueryHandler(self.callback_basic)
        assert not handler.check_update(false_update)

    def test_context(self, cdp, callback_query):
        handler = CallbackQueryHandler(self.callback_context)
        cdp.add_handler(handler)

        cdp.process_update(callback_query)
        assert self.test_flag

    def test_context_pattern(self, cdp, callback_query):
        handler = CallbackQueryHandler(
            self.callback_context_pattern, pattern=r'(?P<begin>.*)est(?P<end>.*)'
        )
        cdp.add_handler(handler)

        cdp.process_update(callback_query)
        assert self.test_flag

        cdp.remove_handler(handler)
        handler = CallbackQueryHandler(self.callback_context_pattern, pattern=r'(t)est(.*)')
        cdp.add_handler(handler)

        cdp.process_update(callback_query)
        assert self.test_flag
