#!/usr/bin/env python

import pytest

from telegram import Update, Message, Chat, User, TelegramError
from telegram.ext import CallbackContext


class TestCallbackContext:
    def test_non_context_dp(self, dp):
        with pytest.raises(ValueError):
            CallbackContext(dp)

    def test_from_job(self, cdp):
        job = cdp.job_queue.run_once(lambda x: x, 10)

        callback_context = CallbackContext.from_job(job, cdp)

        assert callback_context.job is job
        assert callback_context.chat_data is None
        assert callback_context.user_data is None
        assert callback_context.bot_data is cdp.bot_data
        assert callback_context.bot is cdp.bot
        assert callback_context.job_queue is cdp.job_queue
        assert callback_context.update_queue is cdp.update_queue

    def test_from_update(self, cdp):
        update = Update(
            0, message=Message(0, None, Chat(1, 'chat'), from_user=User(1, 'user', False))
        )

        callback_context = CallbackContext.from_update(update, cdp)

        assert callback_context.chat_data == {}
        assert callback_context.user_data == {}
        assert callback_context.bot_data is cdp.bot_data
        assert callback_context.bot is cdp.bot
        assert callback_context.job_queue is cdp.job_queue
        assert callback_context.update_queue is cdp.update_queue

        callback_context_same_user_chat = CallbackContext.from_update(update, cdp)

        callback_context.bot_data['test'] = 'bot'
        callback_context.chat_data['test'] = 'chat'
        callback_context.user_data['test'] = 'user'

        assert callback_context_same_user_chat.bot_data is callback_context.bot_data
        assert callback_context_same_user_chat.chat_data is callback_context.chat_data
        assert callback_context_same_user_chat.user_data is callback_context.user_data

        update_other_user_chat = Update(
            0, message=Message(0, None, Chat(2, 'chat'), from_user=User(2, 'user', False))
        )

        callback_context_other_user_chat = CallbackContext.from_update(update_other_user_chat, cdp)

        assert callback_context_other_user_chat.bot_data is callback_context.bot_data
        assert callback_context_other_user_chat.chat_data is not callback_context.chat_data
        assert callback_context_other_user_chat.user_data is not callback_context.user_data

    def test_from_update_not_update(self, cdp):
        callback_context = CallbackContext.from_update(None, cdp)

        assert callback_context.chat_data is None
        assert callback_context.user_data is None
        assert callback_context.bot_data is cdp.bot_data
        assert callback_context.bot is cdp.bot
        assert callback_context.job_queue is cdp.job_queue
        assert callback_context.update_queue is cdp.update_queue

        callback_context = CallbackContext.from_update('', cdp)

        assert callback_context.chat_data is None
        assert callback_context.user_data is None
        assert callback_context.bot_data is cdp.bot_data
        assert callback_context.bot is cdp.bot
        assert callback_context.job_queue is cdp.job_queue
        assert callback_context.update_queue is cdp.update_queue

    def test_from_error(self, cdp):
        error = TelegramError('test')

        update = Update(
            0, message=Message(0, None, Chat(1, 'chat'), from_user=User(1, 'user', False))
        )

        callback_context = CallbackContext.from_error(update, error, cdp)

        assert callback_context.error is error
        assert callback_context.chat_data == {}
        assert callback_context.user_data == {}
        assert callback_context.bot_data is cdp.bot_data
        assert callback_context.bot is cdp.bot
        assert callback_context.job_queue is cdp.job_queue
        assert callback_context.update_queue is cdp.update_queue
        assert callback_context.async_args is None
        assert callback_context.async_kwargs is None

    def test_from_error_async_params(self, cdp):
        error = TelegramError('test')

        args = [1, '2']
        kwargs = {'one': 1, 2: 'two'}

        callback_context = CallbackContext.from_error(
            None, error, cdp, async_args=args, async_kwargs=kwargs
        )

        assert callback_context.error is error
        assert callback_context.async_args is args
        assert callback_context.async_kwargs is kwargs

    def test_match(self, cdp):
        callback_context = CallbackContext(cdp)

        assert callback_context.match is None

        callback_context.matches = ['test', 'blah']

        assert callback_context.match == 'test'

    def test_data_assignment(self, cdp):
        update = Update(
            0, message=Message(0, None, Chat(1, 'chat'), from_user=User(1, 'user', False))
        )

        callback_context = CallbackContext.from_update(update, cdp)

        with pytest.raises(AttributeError):
            callback_context.chat_data = {"test": 123}
        with pytest.raises(AttributeError):
            callback_context.user_data = {}
        with pytest.raises(AttributeError):
            callback_context.chat_data = "test"

    def test_dispatcher_attribute(self, cdp):
        callback_context = CallbackContext(cdp)
        assert callback_context.dispatcher == cdp
