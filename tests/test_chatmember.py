#!/usr/bin/env python

import datetime

import pytest

from telegram import User, ChatMember
from telegram.utils.helpers import to_timestamp


@pytest.fixture(scope='class')
def user():
    return User(1, 'First name', False)


@pytest.fixture(scope='class')
def chat_member(user):
    return ChatMember(user, TestChatMember.status)


class TestChatMember:
    status = ChatMember.CREATOR

    def test_de_json_required_args(self, bot, user):
        json_dict = {'user': user.to_dict(), 'status': self.status}

        chat_member = ChatMember.de_json(json_dict, bot)

        assert chat_member.user == user
        assert chat_member.status == self.status

    def test_de_json_all_args(self, bot, user):
        time = datetime.datetime.utcnow()
        custom_title = 'custom_title'

        json_dict = {
            'user': user.to_dict(),
            'status': self.status,
            'custom_title': custom_title,
            'is_anonymous': True,
            'until_date': to_timestamp(time),
            'can_be_edited': False,
            'can_change_info': True,
            'can_post_messages': False,
            'can_edit_messages': True,
            'can_delete_messages': True,
            'can_invite_users': False,
            'can_restrict_members': True,
            'can_pin_messages': False,
            'can_promote_members': True,
            'can_send_messages': False,
            'can_send_media_messages': True,
            'can_send_polls': False,
            'can_send_other_messages': True,
            'can_add_web_page_previews': False,
        }

        chat_member = ChatMember.de_json(json_dict, bot)

        assert chat_member.user == user
        assert chat_member.status == self.status
        assert chat_member.custom_title == custom_title
        assert chat_member.is_anonymous is True
        assert chat_member.can_be_edited is False
        assert chat_member.can_change_info is True
        assert chat_member.can_post_messages is False
        assert chat_member.can_edit_messages is True
        assert chat_member.can_delete_messages is True
        assert chat_member.can_invite_users is False
        assert chat_member.can_restrict_members is True
        assert chat_member.can_pin_messages is False
        assert chat_member.can_promote_members is True
        assert chat_member.can_send_messages is False
        assert chat_member.can_send_media_messages is True
        assert chat_member.can_send_polls is False
        assert chat_member.can_send_other_messages is True
        assert chat_member.can_add_web_page_previews is False

    def test_to_dict(self, chat_member):
        chat_member_dict = chat_member.to_dict()
        assert isinstance(chat_member_dict, dict)
        assert chat_member_dict['user'] == chat_member.user.to_dict()
        assert chat_member['status'] == chat_member.status

    def test_equality(self):
        a = ChatMember(User(1, '', False), ChatMember.ADMINISTRATOR)
        b = ChatMember(User(1, '', False), ChatMember.ADMINISTRATOR)
        d = ChatMember(User(2, '', False), ChatMember.ADMINISTRATOR)
        d2 = ChatMember(User(1, '', False), ChatMember.CREATOR)

        assert a == b
        assert hash(a) == hash(b)
        assert a is not b

        assert a != d
        assert hash(a) != hash(d)

        assert a != d2
        assert hash(a) != hash(d2)
