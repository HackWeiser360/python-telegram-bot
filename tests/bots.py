#!/usr/bin/env python

"""Provide a bot to tests"""
import json
import base64
import os
import random
import pytest
from telegram.utils.request import Request
from telegram.error import RetryAfter

# Provide some public fallbacks so it's easy for contributors to run tests on their local machine
# These bots are only able to talk in our test chats, so they are quite useless for other
# purposes than testing.
FALLBACKS = [
    {
        'token': '579694714:AAHRLL5zBVy4Blx2jRFKe1HlfnXCg08WuLY',
        'payment_provider_token': '284685063:TEST:NjQ0NjZlNzI5YjJi',
        'chat_id': '675666224',
        'super_group_id': '-1001310911135',
        'channel_id': '@pythontelegrambottests',
        'bot_name': 'PTB tests fallback 1',
        'bot_username': '@ptb_fallback_1_bot',
    },
    {
        'token': '558194066:AAEEylntuKSLXj9odiv3TnX7Z5KY2J3zY3M',
        'payment_provider_token': '284685063:TEST:YjEwODQwMTFmNDcy',
        'chat_id': '675666224',
        'super_group_id': '-1001221216830',
        'channel_id': '@pythontelegrambottests',
        'bot_name': 'PTB tests fallback 2',
        'bot_username': '@ptb_fallback_2_bot',
    },
]

GITHUB_ACTION = os.getenv('GITHUB_ACTION', None)
BOTS = os.getenv('BOTS', None)
JOB_INDEX = os.getenv('JOB_INDEX', None)
if GITHUB_ACTION is not None and BOTS is not None and JOB_INDEX is not None:
    BOTS = json.loads(base64.b64decode(BOTS).decode('utf-8'))
    JOB_INDEX = int(JOB_INDEX)


def get(name, fallback):
    # If we have TOKEN, PAYMENT_PROVIDER_TOKEN, CHAT_ID, SUPER_GROUP_ID,
    # CHANNEL_ID, BOT_NAME, or BOT_USERNAME in the environment, then use that
    val = os.getenv(name.upper())
    if val:
        return val

    # If we're running as a github action then fetch bots from the repo secrets
    if GITHUB_ACTION is not None and BOTS is not None and JOB_INDEX is not None:
        try:
            return BOTS[JOB_INDEX][name]
        except KeyError:
            pass

    # Otherwise go with the fallback
    return fallback


def get_bot():
    return {k: get(k, v) for k, v in random.choice(FALLBACKS).items()}


# Patch request to xfail on flood control errors
original_request_wrapper = Request._request_wrapper


def patient_request_wrapper(*args, **kwargs):
    try:
        return original_request_wrapper(*args, **kwargs)
    except RetryAfter as e:
        pytest.xfail(f'Not waiting for flood control: {e}')


Request._request_wrapper = patient_request_wrapper
