#!/usr/bin/env python


import pytest

from telegram import ChatPermissions, User


@pytest.fixture(scope="class")
def chat_permissions():
    return ChatPermissions(
        can_send_messages=True,
        can_send_media_messages=True,
        can_send_polls=True,
        can_send_other_messages=True,
        can_add_web_page_previews=True,
        can_change_info=True,
        can_invite_users=True,
        can_pin_messages=True,
    )


class TestChatPermissions:
    can_send_messages = True
    can_send_media_messages = True
    can_send_polls = True
    can_send_other_messages = False
    can_add_web_page_previews = False
    can_change_info = False
    can_invite_users = None
    can_pin_messages = None

    def test_de_json(self, bot):
        json_dict = {
            'can_send_messages': self.can_send_messages,
            'can_send_media_messages': self.can_send_media_messages,
            'can_send_polls': self.can_send_polls,
            'can_send_other_messages': self.can_send_other_messages,
            'can_add_web_page_previews': self.can_add_web_page_previews,
            'can_change_info': self.can_change_info,
            'can_invite_users': self.can_invite_users,
            'can_pin_messages': self.can_pin_messages,
        }
        permissions = ChatPermissions.de_json(json_dict, bot)

        assert permissions.can_send_messages == self.can_send_messages
        assert permissions.can_send_media_messages == self.can_send_media_messages
        assert permissions.can_send_polls == self.can_send_polls
        assert permissions.can_send_other_messages == self.can_send_other_messages
        assert permissions.can_add_web_page_previews == self.can_add_web_page_previews
        assert permissions.can_change_info == self.can_change_info
        assert permissions.can_invite_users == self.can_invite_users
        assert permissions.can_pin_messages == self.can_pin_messages

    def test_to_dict(self, chat_permissions):
        permissions_dict = chat_permissions.to_dict()

        assert isinstance(permissions_dict, dict)
        assert permissions_dict['can_send_messages'] == chat_permissions.can_send_messages
        assert (
            permissions_dict['can_send_media_messages'] == chat_permissions.can_send_media_messages
        )
        assert permissions_dict['can_send_polls'] == chat_permissions.can_send_polls
        assert (
            permissions_dict['can_send_other_messages'] == chat_permissions.can_send_other_messages
        )
        assert (
            permissions_dict['can_add_web_page_previews']
            == chat_permissions.can_add_web_page_previews
        )
        assert permissions_dict['can_change_info'] == chat_permissions.can_change_info
        assert permissions_dict['can_invite_users'] == chat_permissions.can_invite_users
        assert permissions_dict['can_pin_messages'] == chat_permissions.can_pin_messages

    def test_equality(self):
        a = ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_polls=True,
            can_send_other_messages=False,
        )
        b = ChatPermissions(
            can_send_polls=True,
            can_send_other_messages=False,
            can_send_messages=True,
            can_send_media_messages=True,
        )
        c = ChatPermissions(
            can_send_messages=False,
            can_send_media_messages=True,
            can_send_polls=True,
            can_send_other_messages=False,
        )
        d = User(123, '', False)

        assert a == b
        assert hash(a) == hash(b)
        assert a is not b

        assert a != c
        assert hash(a) != hash(c)

        assert a != d
        assert hash(a) != hash(d)
