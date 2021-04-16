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

from telegram import ShippingAddress, OrderInfo


@pytest.fixture(scope='class')
def order_info():
    return OrderInfo(
        TestOrderInfo.name,
        TestOrderInfo.phone_number,
        TestOrderInfo.email,
        TestOrderInfo.shipping_address,
    )


class TestOrderInfo:
    name = 'name'
    phone_number = 'phone_number'
    email = 'email'
    shipping_address = ShippingAddress('GB', '', 'London', '12 Grimmauld Place', '', 'WC1')

    def test_de_json(self, bot):
        json_dict = {
            'name': TestOrderInfo.name,
            'phone_number': TestOrderInfo.phone_number,
            'email': TestOrderInfo.email,
            'shipping_address': TestOrderInfo.shipping_address.to_dict(),
        }
        order_info = OrderInfo.de_json(json_dict, bot)

        assert order_info.name == self.name
        assert order_info.phone_number == self.phone_number
        assert order_info.email == self.email
        assert order_info.shipping_address == self.shipping_address

    def test_to_dict(self, order_info):
        order_info_dict = order_info.to_dict()

        assert isinstance(order_info_dict, dict)
        assert order_info_dict['name'] == order_info.name
        assert order_info_dict['phone_number'] == order_info.phone_number
        assert order_info_dict['email'] == order_info.email
        assert order_info_dict['shipping_address'] == order_info.shipping_address.to_dict()

    def test_equality(self):
        a = OrderInfo(
            'name',
            'number',
            'mail',
            ShippingAddress('GB', '', 'London', '12 Grimmauld Place', '', 'WC1'),
        )
        b = OrderInfo(
            'name',
            'number',
            'mail',
            ShippingAddress('GB', '', 'London', '12 Grimmauld Place', '', 'WC1'),
        )
        c = OrderInfo(
            'name',
            'number',
            'mail',
            ShippingAddress('GB', '', 'London', '13 Grimmauld Place', '', 'WC1'),
        )
        d = OrderInfo(
            'name',
            'number',
            'e-mail',
            ShippingAddress('GB', '', 'London', '12 Grimmauld Place', '', 'WC1'),
        )
        e = ShippingAddress('GB', '', 'London', '12 Grimmauld Place', '', 'WC1')

        assert a == b
        assert hash(a) == hash(b)

        assert a != c
        assert hash(a) != hash(c)

        assert a != d
        assert hash(a) != hash(d)

        assert a != e
        assert hash(a) != hash(e)
