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

from telegram import LabeledPrice, Location


@pytest.fixture(scope='class')
def labeled_price():
    return LabeledPrice(TestLabeledPrice.label, TestLabeledPrice.amount)


class TestLabeledPrice:
    label = 'label'
    amount = 100

    def test_expected_values(self, labeled_price):
        assert labeled_price.label == self.label
        assert labeled_price.amount == self.amount

    def test_to_dict(self, labeled_price):
        labeled_price_dict = labeled_price.to_dict()

        assert isinstance(labeled_price_dict, dict)
        assert labeled_price_dict['label'] == labeled_price.label
        assert labeled_price_dict['amount'] == labeled_price.amount

    def test_equality(self):
        a = LabeledPrice('label', 100)
        b = LabeledPrice('label', 100)
        c = LabeledPrice('Label', 101)
        d = Location(123, 456)

        assert a == b
        assert hash(a) == hash(b)

        assert a != c
        assert hash(a) != hash(c)

        assert a != d
        assert hash(a) != hash(d)
