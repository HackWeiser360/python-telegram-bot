#!/usr/bin/env python


import os
import pytest
from flaky import flaky

from telegram import ChatPhoto, Voice, TelegramError
from tests.conftest import expect_bad_request


@pytest.fixture(scope='function')
def chatphoto_file():
    f = open('tests/data/telegram.jpg', 'rb')
    yield f
    f.close()


@pytest.fixture(scope='function')
def chat_photo(bot, super_group_id):
    def func():
        return bot.get_chat(super_group_id, timeout=50).photo

    return expect_bad_request(func, 'Type of file mismatch', 'Telegram did not accept the file.')


class TestChatPhoto:
    chatphoto_small_file_id = 'smallCgADAQADngIAAuyVeEez0xRovKi9VAI'
    chatphoto_big_file_id = 'bigCgADAQADngIAAuyVeEez0xRovKi9VAI'
    chatphoto_small_file_unique_id = 'smalladc3145fd2e84d95b64d68eaa22aa33e'
    chatphoto_big_file_unique_id = 'bigadc3145fd2e84d95b64d68eaa22aa33e'
    chatphoto_file_url = 'https://python-telegram-bot.org/static/testfiles/telegram.jpg'

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_send_all_args(self, bot, super_group_id, chatphoto_file, chat_photo, thumb_file):
        def func():
            assert bot.set_chat_photo(super_group_id, chatphoto_file)

        expect_bad_request(func, 'Type of file mismatch', 'Telegram did not accept the file.')

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_get_and_download(self, bot, chat_photo):
        new_file = bot.get_file(chat_photo.small_file_id)

        assert new_file.file_id == chat_photo.small_file_id
        assert new_file.file_path.startswith('https://')

        new_file.download('telegram.jpg')

        assert os.path.isfile('telegram.jpg')

        new_file = bot.get_file(chat_photo.big_file_id)

        assert new_file.file_id == chat_photo.big_file_id
        assert new_file.file_path.startswith('https://')

        new_file.download('telegram.jpg')

        assert os.path.isfile('telegram.jpg')

    def test_send_with_chat_photo(self, monkeypatch, bot, super_group_id, chat_photo):
        def test(url, data, **kwargs):
            return data['photo'] == chat_photo

        monkeypatch.setattr(bot.request, 'post', test)
        message = bot.set_chat_photo(photo=chat_photo, chat_id=super_group_id)
        assert message

    def test_de_json(self, bot, chat_photo):
        json_dict = {
            'small_file_id': self.chatphoto_small_file_id,
            'big_file_id': self.chatphoto_big_file_id,
            'small_file_unique_id': self.chatphoto_small_file_unique_id,
            'big_file_unique_id': self.chatphoto_big_file_unique_id,
        }
        chat_photo = ChatPhoto.de_json(json_dict, bot)
        assert chat_photo.small_file_id == self.chatphoto_small_file_id
        assert chat_photo.big_file_id == self.chatphoto_big_file_id
        assert chat_photo.small_file_unique_id == self.chatphoto_small_file_unique_id
        assert chat_photo.big_file_unique_id == self.chatphoto_big_file_unique_id

    def test_to_dict(self, chat_photo):
        chat_photo_dict = chat_photo.to_dict()

        assert isinstance(chat_photo_dict, dict)
        assert chat_photo_dict['small_file_id'] == chat_photo.small_file_id
        assert chat_photo_dict['big_file_id'] == chat_photo.big_file_id
        assert chat_photo_dict['small_file_unique_id'] == chat_photo.small_file_unique_id
        assert chat_photo_dict['big_file_unique_id'] == chat_photo.big_file_unique_id

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_error_send_empty_file(self, bot, super_group_id):
        chatphoto_file = open(os.devnull, 'rb')

        with pytest.raises(TelegramError):
            bot.set_chat_photo(chat_id=super_group_id, photo=chatphoto_file)

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_error_send_empty_file_id(self, bot, super_group_id):
        with pytest.raises(TelegramError):
            bot.set_chat_photo(chat_id=super_group_id, photo='')

    def test_error_send_without_required_args(self, bot, super_group_id):
        with pytest.raises(TypeError):
            bot.set_chat_photo(chat_id=super_group_id)

    def test_get_small_file_instance_method(self, monkeypatch, chat_photo):
        def test(*args, **kwargs):
            return args[1] == chat_photo.small_file_id

        monkeypatch.setattr('telegram.Bot.get_file', test)
        assert chat_photo.get_small_file()

    def test_get_big_file_instance_method(self, monkeypatch, chat_photo):
        def test(*args, **kwargs):
            return args[1] == chat_photo.big_file_id

        monkeypatch.setattr('telegram.Bot.get_file', test)
        assert chat_photo.get_big_file()

    def test_equality(self):
        a = ChatPhoto(
            self.chatphoto_small_file_id,
            self.chatphoto_big_file_id,
            self.chatphoto_small_file_unique_id,
            self.chatphoto_big_file_unique_id,
        )
        b = ChatPhoto(
            self.chatphoto_small_file_id,
            self.chatphoto_big_file_id,
            self.chatphoto_small_file_unique_id,
            self.chatphoto_big_file_unique_id,
        )
        c = ChatPhoto(
            '', '', self.chatphoto_small_file_unique_id, self.chatphoto_big_file_unique_id
        )
        d = ChatPhoto('', '', 0, 0)
        e = Voice(self.chatphoto_small_file_id, self.chatphoto_small_file_unique_id, 0)

        assert a == b
        assert hash(a) == hash(b)
        assert a is not b

        assert a != c
        assert hash(a) != hash(c)

        assert a != d
        assert hash(a) != hash(d)

        assert a != e
        assert hash(a) != hash(e)
