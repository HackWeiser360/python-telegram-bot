#!/usr/bin/env python


import pytest
from flaky import flaky

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyMarkup, ReplyKeyboardMarkup


@pytest.fixture(scope='class')
def inline_keyboard_markup():
    return InlineKeyboardMarkup(TestInlineKeyboardMarkup.inline_keyboard)


class TestInlineKeyboardMarkup:
    inline_keyboard = [
        [
            InlineKeyboardButton(text='button1', callback_data='data1'),
            InlineKeyboardButton(text='button2', callback_data='data2'),
        ]
    ]

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_send_message_with_inline_keyboard_markup(self, bot, chat_id, inline_keyboard_markup):
        message = bot.send_message(
            chat_id, 'Testing InlineKeyboardMarkup', reply_markup=inline_keyboard_markup
        )

        assert message.text == 'Testing InlineKeyboardMarkup'

    def test_from_button(self):
        inline_keyboard_markup = InlineKeyboardMarkup.from_button(
            InlineKeyboardButton(text='button1', callback_data='data1')
        ).inline_keyboard
        assert len(inline_keyboard_markup) == 1
        assert len(inline_keyboard_markup[0]) == 1

    def test_from_row(self):
        inline_keyboard_markup = InlineKeyboardMarkup.from_row(
            [
                InlineKeyboardButton(text='button1', callback_data='data1'),
                InlineKeyboardButton(text='button1', callback_data='data1'),
            ]
        ).inline_keyboard
        assert len(inline_keyboard_markup) == 1
        assert len(inline_keyboard_markup[0]) == 2

    def test_from_column(self):
        inline_keyboard_markup = InlineKeyboardMarkup.from_column(
            [
                InlineKeyboardButton(text='button1', callback_data='data1'),
                InlineKeyboardButton(text='button1', callback_data='data1'),
            ]
        ).inline_keyboard
        assert len(inline_keyboard_markup) == 2
        assert len(inline_keyboard_markup[0]) == 1
        assert len(inline_keyboard_markup[1]) == 1

    def test_expected_values(self, inline_keyboard_markup):
        assert inline_keyboard_markup.inline_keyboard == self.inline_keyboard

    def test_expected_values_empty_switch(self, inline_keyboard_markup, bot, monkeypatch):
        def test(
            url,
            data,
            reply_to_message_id=None,
            disable_notification=None,
            reply_markup=None,
            timeout=None,
            **kwargs,
        ):
            if reply_markup is not None:
                if isinstance(reply_markup, ReplyMarkup):
                    data['reply_markup'] = reply_markup.to_json()
                else:
                    data['reply_markup'] = reply_markup

            assert bool('"switch_inline_query": ""' in data['reply_markup'])
            assert bool('"switch_inline_query_current_chat": ""' in data['reply_markup'])

        inline_keyboard_markup.inline_keyboard[0][0].callback_data = None
        inline_keyboard_markup.inline_keyboard[0][0].switch_inline_query = ''
        inline_keyboard_markup.inline_keyboard[0][1].callback_data = None
        inline_keyboard_markup.inline_keyboard[0][1].switch_inline_query_current_chat = ''

        monkeypatch.setattr(bot, '_message', test)
        bot.send_message(123, 'test', reply_markup=inline_keyboard_markup)

    def test_to_dict(self, inline_keyboard_markup):
        inline_keyboard_markup_dict = inline_keyboard_markup.to_dict()

        assert isinstance(inline_keyboard_markup_dict, dict)
        assert inline_keyboard_markup_dict['inline_keyboard'] == [
            [self.inline_keyboard[0][0].to_dict(), self.inline_keyboard[0][1].to_dict()]
        ]

    def test_de_json(self):
        json_dict = {
            'inline_keyboard': [
                [
                    {'text': 'start', 'url': 'http://google.com'},
                    {'text': 'next', 'callback_data': 'abcd'},
                ],
                [{'text': 'Cancel', 'callback_data': 'Cancel'}],
            ]
        }
        inline_keyboard_markup = InlineKeyboardMarkup.de_json(json_dict, None)

        assert isinstance(inline_keyboard_markup, InlineKeyboardMarkup)
        keyboard = inline_keyboard_markup.inline_keyboard
        assert len(keyboard) == 2
        assert len(keyboard[0]) == 2
        assert len(keyboard[1]) == 1

        assert isinstance(keyboard[0][0], InlineKeyboardButton)
        assert isinstance(keyboard[0][1], InlineKeyboardButton)
        assert isinstance(keyboard[1][0], InlineKeyboardButton)

        assert keyboard[0][0].text == 'start'
        assert keyboard[0][0].url == 'http://google.com'

    def test_equality(self):
        a = InlineKeyboardMarkup.from_column(
            [
                InlineKeyboardButton(label, callback_data='data')
                for label in ['button1', 'button2', 'button3']
            ]
        )
        b = InlineKeyboardMarkup.from_column(
            [
                InlineKeyboardButton(label, callback_data='data')
                for label in ['button1', 'button2', 'button3']
            ]
        )
        c = InlineKeyboardMarkup.from_column(
            [InlineKeyboardButton(label, callback_data='data') for label in ['button1', 'button2']]
        )
        d = InlineKeyboardMarkup.from_column(
            [
                InlineKeyboardButton(label, callback_data=label)
                for label in ['button1', 'button2', 'button3']
            ]
        )
        e = InlineKeyboardMarkup.from_column(
            [InlineKeyboardButton(label, url=label) for label in ['button1', 'button2', 'button3']]
        )
        f = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(label, callback_data='data')
                    for label in ['button1', 'button2']
                ],
                [
                    InlineKeyboardButton(label, callback_data='data')
                    for label in ['button1', 'button2']
                ],
                [
                    InlineKeyboardButton(label, callback_data='data')
                    for label in ['button1', 'button2']
                ],
            ]
        )
        g = ReplyKeyboardMarkup.from_column(['button1', 'button2', 'button3'])

        assert a == b
        assert hash(a) == hash(b)

        assert a != c
        assert hash(a) != hash(c)

        assert a != d
        assert hash(a) != hash(d)

        assert a != e
        assert hash(a) != hash(e)

        assert a != f
        assert hash(a) != hash(f)

        assert a != g
        assert hash(a) != hash(g)
