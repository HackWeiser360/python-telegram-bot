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
    Location,
)
from telegram.ext import InlineQueryHandler, CallbackContext, JobQueue

message = Message(1, None, Chat(1, ''), from_user=User(1, '', False), text='Text')

params = [
    {'message': message},
    {'edited_message': message},
    {'callback_query': CallbackQuery(1, User(1, '', False), 'chat', message=message)},
    {'channel_post': message},
    {'edited_channel_post': message},
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
    'chosen_inline_result',
    'shipping_query',
    'pre_checkout_query',
    'callback_query_without_message',
)


@pytest.fixture(scope='class', params=params, ids=ids)
def false_update(request):
    return Update(update_id=2, **request.param)


@pytest.fixture(scope='function')
def inline_query(bot):
    return Update(
        0,
        inline_query=InlineQuery(
            'id',
            User(2, 'test user', False),
            'test query',
            offset='22',
            location=Location(latitude=-23.691288, longitude=-46.788279),
        ),
    )


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
            self.test_flag = groups == ('t', ' query')
        if groupdict is not None:
            self.test_flag = groupdict == {'begin': 't', 'end': ' query'}

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
            and isinstance(update.inline_query, InlineQuery)
        )

    def callback_context_pattern(self, update, context):
        if context.matches[0].groups():
            self.test_flag = context.matches[0].groups() == ('t', ' query')
        if context.matches[0].groupdict():
            self.test_flag = context.matches[0].groupdict() == {'begin': 't', 'end': ' query'}

    def test_basic(self, dp, inline_query):
        handler = InlineQueryHandler(self.callback_basic)
        dp.add_handler(handler)

        assert handler.check_update(inline_query)

        dp.process_update(inline_query)
        assert self.test_flag

    def test_with_pattern(self, inline_query):
        handler = InlineQueryHandler(self.callback_basic, pattern='(?P<begin>.*)est(?P<end>.*)')

        assert handler.check_update(inline_query)

        inline_query.inline_query.query = 'nothing here'
        assert not handler.check_update(inline_query)

    def test_with_passing_group_dict(self, dp, inline_query):
        handler = InlineQueryHandler(
            self.callback_group, pattern='(?P<begin>.*)est(?P<end>.*)', pass_groups=True
        )
        dp.add_handler(handler)

        dp.process_update(inline_query)
        assert self.test_flag

        dp.remove_handler(handler)
        handler = InlineQueryHandler(
            self.callback_group, pattern='(?P<begin>.*)est(?P<end>.*)', pass_groupdict=True
        )
        dp.add_handler(handler)

        self.test_flag = False
        dp.process_update(inline_query)
        assert self.test_flag

    def test_pass_user_or_chat_data(self, dp, inline_query):
        handler = InlineQueryHandler(self.callback_data_1, pass_user_data=True)
        dp.add_handler(handler)

        dp.process_update(inline_query)
        assert self.test_flag

        dp.remove_handler(handler)
        handler = InlineQueryHandler(self.callback_data_1, pass_chat_data=True)
        dp.add_handler(handler)

        self.test_flag = False
        dp.process_update(inline_query)
        assert self.test_flag

        dp.remove_handler(handler)
        handler = InlineQueryHandler(
            self.callback_data_2, pass_chat_data=True, pass_user_data=True
        )
        dp.add_handler(handler)

        self.test_flag = False
        dp.process_update(inline_query)
        assert self.test_flag

    def test_pass_job_or_update_queue(self, dp, inline_query):
        handler = InlineQueryHandler(self.callback_queue_1, pass_job_queue=True)
        dp.add_handler(handler)

        dp.process_update(inline_query)
        assert self.test_flag

        dp.remove_handler(handler)
        handler = InlineQueryHandler(self.callback_queue_1, pass_update_queue=True)
        dp.add_handler(handler)

        self.test_flag = False
        dp.process_update(inline_query)
        assert self.test_flag

        dp.remove_handler(handler)
        handler = InlineQueryHandler(
            self.callback_queue_2, pass_job_queue=True, pass_update_queue=True
        )
        dp.add_handler(handler)

        self.test_flag = False
        dp.process_update(inline_query)
        assert self.test_flag

    def test_other_update_types(self, false_update):
        handler = InlineQueryHandler(self.callback_basic)
        assert not handler.check_update(false_update)

    def test_context(self, cdp, inline_query):
        handler = InlineQueryHandler(self.callback_context)
        cdp.add_handler(handler)

        cdp.process_update(inline_query)
        assert self.test_flag

    def test_context_pattern(self, cdp, inline_query):
        handler = InlineQueryHandler(
            self.callback_context_pattern, pattern=r'(?P<begin>.*)est(?P<end>.*)'
        )
        cdp.add_handler(handler)

        cdp.process_update(inline_query)
        assert self.test_flag

        cdp.remove_handler(handler)
        handler = InlineQueryHandler(self.callback_context_pattern, pattern=r'(t)est(.*)')
        cdp.add_handler(handler)

        cdp.process_update(inline_query)
        assert self.test_flag
