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

import pytest
from flaky import flaky

from telegram import LabeledPrice, Invoice
from telegram.error import BadRequest


@pytest.fixture(scope='class')
def invoice():
    return Invoice(
        TestInvoice.title,
        TestInvoice.description,
        TestInvoice.start_parameter,
        TestInvoice.currency,
        TestInvoice.total_amount,
    )


class TestInvoice:
    payload = 'payload'
    prices = [LabeledPrice('Fish', 100), LabeledPrice('Fish Tax', 1000)]
    provider_data = """{"test":"test"}"""
    title = 'title'
    description = 'description'
    start_parameter = 'start_parameter'
    currency = 'EUR'
    total_amount = sum([p.amount for p in prices])

    def test_de_json(self, bot):
        invoice_json = Invoice.de_json(
            {
                'title': TestInvoice.title,
                'description': TestInvoice.description,
                'start_parameter': TestInvoice.start_parameter,
                'currency': TestInvoice.currency,
                'total_amount': TestInvoice.total_amount,
            },
            bot,
        )

        assert invoice_json.title == self.title
        assert invoice_json.description == self.description
        assert invoice_json.start_parameter == self.start_parameter
        assert invoice_json.currency == self.currency
        assert invoice_json.total_amount == self.total_amount

    def test_to_dict(self, invoice):
        invoice_dict = invoice.to_dict()

        assert isinstance(invoice_dict, dict)
        assert invoice_dict['title'] == invoice.title
        assert invoice_dict['description'] == invoice.description
        assert invoice_dict['start_parameter'] == invoice.start_parameter
        assert invoice_dict['currency'] == invoice.currency
        assert invoice_dict['total_amount'] == invoice.total_amount

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_send_required_args_only(self, bot, chat_id, provider_token):
        message = bot.send_invoice(
            chat_id,
            self.title,
            self.description,
            self.payload,
            provider_token,
            self.start_parameter,
            self.currency,
            self.prices,
        )

        assert message.invoice.currency == self.currency
        assert message.invoice.start_parameter == self.start_parameter
        assert message.invoice.description == self.description
        assert message.invoice.title == self.title
        assert message.invoice.total_amount == self.total_amount

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_send_all_args(self, bot, chat_id, provider_token):
        message = bot.send_invoice(
            chat_id,
            self.title,
            self.description,
            self.payload,
            provider_token,
            self.start_parameter,
            self.currency,
            self.prices,
            provider_data=self.provider_data,
            photo_url='https://raw.githubusercontent.com/'
            'python-telegram-bot/logos/master/'
            'logo/png/ptb-logo_240.png',
            photo_size=240,
            photo_width=240,
            photo_height=240,
            need_name=True,
            need_phone_number=True,
            need_email=True,
            need_shipping_address=True,
            send_phone_number_to_provider=True,
            send_email_to_provider=True,
            is_flexible=True,
        )

        assert message.invoice.currency == self.currency
        assert message.invoice.start_parameter == self.start_parameter
        assert message.invoice.description == self.description
        assert message.invoice.title == self.title
        assert message.invoice.total_amount == self.total_amount

    def test_send_object_as_provider_data(self, monkeypatch, bot, chat_id, provider_token):
        def test(url, data, **kwargs):
            return (
                data['provider_data'] == '{"test_data": 123456789}'  # Depends if using
                or data['provider_data'] == '{"test_data":123456789}'
            )  # ujson or not

        monkeypatch.setattr(bot.request, 'post', test)

        assert bot.send_invoice(
            chat_id,
            self.title,
            self.description,
            self.payload,
            provider_token,
            self.start_parameter,
            self.currency,
            self.prices,
            provider_data={'test_data': 123456789},
        )

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    @pytest.mark.parametrize(
        'default_bot,custom',
        [
            ({'allow_sending_without_reply': True}, None),
            ({'allow_sending_without_reply': False}, None),
            ({'allow_sending_without_reply': False}, True),
        ],
        indirect=['default_bot'],
    )
    def test_send_invoice_default_allow_sending_without_reply(
        self, default_bot, chat_id, custom, provider_token
    ):
        reply_to_message = default_bot.send_message(chat_id, 'test')
        reply_to_message.delete()
        if custom is not None:
            message = default_bot.send_invoice(
                chat_id,
                self.title,
                self.description,
                self.payload,
                provider_token,
                self.start_parameter,
                self.currency,
                self.prices,
                allow_sending_without_reply=custom,
                reply_to_message_id=reply_to_message.message_id,
            )
            assert message.reply_to_message is None
        elif default_bot.defaults.allow_sending_without_reply:
            message = default_bot.send_invoice(
                chat_id,
                self.title,
                self.description,
                self.payload,
                provider_token,
                self.start_parameter,
                self.currency,
                self.prices,
                reply_to_message_id=reply_to_message.message_id,
            )
            assert message.reply_to_message is None
        else:
            with pytest.raises(BadRequest, match='message not found'):
                default_bot.send_invoice(
                    chat_id,
                    self.title,
                    self.description,
                    self.payload,
                    provider_token,
                    self.start_parameter,
                    self.currency,
                    self.prices,
                    reply_to_message_id=reply_to_message.message_id,
                )

    def test_equality(self):
        a = Invoice('invoice', 'desc', 'start', 'EUR', 7)
        b = Invoice('invoice', 'desc', 'start', 'EUR', 7)
        c = Invoice('invoices', 'description', 'stop', 'USD', 8)
        d = LabeledPrice('label', 5)

        assert a == b
        assert hash(a) == hash(b)

        assert a != c
        assert hash(a) != hash(c)

        assert a != d
        assert hash(a) != hash(d)
