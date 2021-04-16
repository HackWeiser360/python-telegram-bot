#!/usr/bin/env python


import pytest

from telegram import EncryptedPassportElement, PassportFile, PassportElementError


@pytest.fixture(scope='class')
def encrypted_passport_element():
    return EncryptedPassportElement(
        TestEncryptedPassportElement.type_,
        data=TestEncryptedPassportElement.data,
        phone_number=TestEncryptedPassportElement.phone_number,
        email=TestEncryptedPassportElement.email,
        files=TestEncryptedPassportElement.files,
        front_side=TestEncryptedPassportElement.front_side,
        reverse_side=TestEncryptedPassportElement.reverse_side,
        selfie=TestEncryptedPassportElement.selfie,
    )


class TestEncryptedPassportElement:
    type_ = 'type'
    data = 'data'
    phone_number = 'phone_number'
    email = 'email'
    files = [PassportFile('file_id', 50, 0)]
    front_side = PassportFile('file_id', 50, 0)
    reverse_side = PassportFile('file_id', 50, 0)
    selfie = PassportFile('file_id', 50, 0)

    def test_expected_values(self, encrypted_passport_element):
        assert encrypted_passport_element.type == self.type_
        assert encrypted_passport_element.data == self.data
        assert encrypted_passport_element.phone_number == self.phone_number
        assert encrypted_passport_element.email == self.email
        assert encrypted_passport_element.files == self.files
        assert encrypted_passport_element.front_side == self.front_side
        assert encrypted_passport_element.reverse_side == self.reverse_side
        assert encrypted_passport_element.selfie == self.selfie

    def test_to_dict(self, encrypted_passport_element):
        encrypted_passport_element_dict = encrypted_passport_element.to_dict()

        assert isinstance(encrypted_passport_element_dict, dict)
        assert encrypted_passport_element_dict['type'] == encrypted_passport_element.type
        assert encrypted_passport_element_dict['data'] == encrypted_passport_element.data
        assert (
            encrypted_passport_element_dict['phone_number']
            == encrypted_passport_element.phone_number
        )
        assert encrypted_passport_element_dict['email'] == encrypted_passport_element.email
        assert isinstance(encrypted_passport_element_dict['files'], list)
        assert (
            encrypted_passport_element_dict['front_side']
            == encrypted_passport_element.front_side.to_dict()
        )
        assert (
            encrypted_passport_element_dict['reverse_side']
            == encrypted_passport_element.reverse_side.to_dict()
        )
        assert (
            encrypted_passport_element_dict['selfie']
            == encrypted_passport_element.selfie.to_dict()
        )

    def test_equality(self):
        a = EncryptedPassportElement(self.type_, data=self.data)
        b = EncryptedPassportElement(self.type_, data=self.data)
        c = EncryptedPassportElement(self.data, '')
        d = PassportElementError('source', 'type', 'message')

        assert a == b
        assert hash(a) == hash(b)
        assert a is not b

        assert a != c
        assert hash(a) != hash(c)

        assert a != d
        assert hash(a) != hash(d)
