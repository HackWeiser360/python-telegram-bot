#!/usr/bin/env python

import os
from pathlib import Path

import pytest
from flaky import flaky

from telegram import PhotoSize, Animation, Voice, TelegramError, MessageEntity
from telegram.error import BadRequest
from telegram.utils.helpers import escape_markdown


@pytest.fixture(scope='function')
def animation_file():
    f = open('tests/data/game.gif', 'rb')
    yield f
    f.close()


@pytest.fixture(scope='class')
def animation(bot, chat_id):
    with open('tests/data/game.gif', 'rb') as f:
        return bot.send_animation(
            chat_id, animation=f, timeout=50, thumb=open('tests/data/thumb.jpg', 'rb')
        ).animation


class TestAnimation:
    animation_file_id = 'CgADAQADngIAAuyVeEez0xRovKi9VAI'
    animation_file_unique_id = 'adc3145fd2e84d95b64d68eaa22aa33e'
    width = 320
    height = 180
    duration = 1
    # animation_file_url = 'https://python-telegram-bot.org/static/testfiles/game.gif'
    # Shortened link, the above one is cached with the wrong duration.
    animation_file_url = 'http://bit.ly/2L18jua'
    file_name = 'game.gif.mp4'
    mime_type = 'video/mp4'
    file_size = 4127
    caption = "Test *animation*"

    def test_creation(self, animation):
        assert isinstance(animation, Animation)
        assert isinstance(animation.file_id, str)
        assert isinstance(animation.file_unique_id, str)
        assert animation.file_id != ''
        assert animation.file_unique_id != ''

    def test_expected_values(self, animation):
        assert animation.file_size == self.file_size
        assert animation.mime_type == self.mime_type
        assert animation.file_name == self.file_name
        assert isinstance(animation.thumb, PhotoSize)

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_send_all_args(self, bot, chat_id, animation_file, animation, thumb_file):
        message = bot.send_animation(
            chat_id,
            animation_file,
            duration=self.duration,
            width=self.width,
            height=self.height,
            caption=self.caption,
            parse_mode='Markdown',
            disable_notification=False,
            thumb=thumb_file,
        )

        assert isinstance(message.animation, Animation)
        assert isinstance(message.animation.file_id, str)
        assert isinstance(message.animation.file_unique_id, str)
        assert message.animation.file_id != ''
        assert message.animation.file_unique_id != ''
        assert message.animation.file_name == animation.file_name
        assert message.animation.mime_type == animation.mime_type
        assert message.animation.file_size == animation.file_size
        assert message.animation.thumb.width == self.width
        assert message.animation.thumb.height == self.height

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_send_animation_custom_filename(self, bot, chat_id, animation_file, monkeypatch):
        def make_assertion(url, data, **kwargs):
            return data['animation'].filename == 'custom_filename'

        monkeypatch.setattr(bot.request, 'post', make_assertion)

        assert bot.send_animation(chat_id, animation_file, filename='custom_filename')

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_get_and_download(self, bot, animation):
        new_file = bot.get_file(animation.file_id)

        assert new_file.file_size == self.file_size
        assert new_file.file_id == animation.file_id
        assert new_file.file_path.startswith('https://')

        new_file.download('game.gif')

        assert os.path.isfile('game.gif')

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_send_animation_url_file(self, bot, chat_id, animation):
        message = bot.send_animation(
            chat_id=chat_id, animation=self.animation_file_url, caption=self.caption
        )

        assert message.caption == self.caption

        assert isinstance(message.animation, Animation)
        assert isinstance(message.animation.file_id, str)
        assert isinstance(message.animation.file_unique_id, str)
        assert message.animation.file_id != ''
        assert message.animation.file_unique_id != ''

        assert message.animation.duration == animation.duration
        assert message.animation.file_name == animation.file_name
        assert message.animation.mime_type == animation.mime_type
        assert message.animation.file_size == animation.file_size

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_send_animation_caption_entities(self, bot, chat_id, animation):
        test_string = 'Italic Bold Code'
        entities = [
            MessageEntity(MessageEntity.ITALIC, 0, 6),
            MessageEntity(MessageEntity.ITALIC, 7, 4),
            MessageEntity(MessageEntity.ITALIC, 12, 4),
        ]
        message = bot.send_animation(
            chat_id, animation, caption=test_string, caption_entities=entities
        )

        assert message.caption == test_string
        assert message.caption_entities == entities

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    @pytest.mark.parametrize('default_bot', [{'parse_mode': 'Markdown'}], indirect=True)
    def test_send_animation_default_parse_mode_1(self, default_bot, chat_id, animation_file):
        test_string = 'Italic Bold Code'
        test_markdown_string = '_Italic_ *Bold* `Code`'

        message = default_bot.send_animation(chat_id, animation_file, caption=test_markdown_string)
        assert message.caption_markdown == test_markdown_string
        assert message.caption == test_string

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    @pytest.mark.parametrize('default_bot', [{'parse_mode': 'Markdown'}], indirect=True)
    def test_send_animation_default_parse_mode_2(self, default_bot, chat_id, animation_file):
        test_markdown_string = '_Italic_ *Bold* `Code`'

        message = default_bot.send_animation(
            chat_id, animation_file, caption=test_markdown_string, parse_mode=None
        )
        assert message.caption == test_markdown_string
        assert message.caption_markdown == escape_markdown(test_markdown_string)

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    @pytest.mark.parametrize('default_bot', [{'parse_mode': 'Markdown'}], indirect=True)
    def test_send_animation_default_parse_mode_3(self, default_bot, chat_id, animation_file):
        test_markdown_string = '_Italic_ *Bold* `Code`'

        message = default_bot.send_animation(
            chat_id, animation_file, caption=test_markdown_string, parse_mode='HTML'
        )
        assert message.caption == test_markdown_string
        assert message.caption_markdown == escape_markdown(test_markdown_string)

    def test_send_animation_local_files(self, monkeypatch, bot, chat_id):
        # For just test that the correct paths are passed as we have no local bot API set up
        test_flag = False
        expected = (Path.cwd() / 'tests/data/telegram.jpg/').as_uri()
        file = 'tests/data/telegram.jpg'

        def make_assertion(_, data, *args, **kwargs):
            nonlocal test_flag
            print(data.get('animation'), expected)
            test_flag = data.get('animation') == expected and data.get('thumb') == expected

        monkeypatch.setattr(bot, '_post', make_assertion)
        bot.send_animation(chat_id, file, thumb=file)
        assert test_flag

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
    def test_send_animation_default_allow_sending_without_reply(
        self, default_bot, chat_id, animation, custom
    ):
        reply_to_message = default_bot.send_message(chat_id, 'test')
        reply_to_message.delete()
        if custom is not None:
            message = default_bot.send_animation(
                chat_id,
                animation,
                allow_sending_without_reply=custom,
                reply_to_message_id=reply_to_message.message_id,
            )
            assert message.reply_to_message is None
        elif default_bot.defaults.allow_sending_without_reply:
            message = default_bot.send_animation(
                chat_id, animation, reply_to_message_id=reply_to_message.message_id
            )
            assert message.reply_to_message is None
        else:
            with pytest.raises(BadRequest, match='message not found'):
                default_bot.send_animation(
                    chat_id, animation, reply_to_message_id=reply_to_message.message_id
                )

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_resend(self, bot, chat_id, animation):
        message = bot.send_animation(chat_id, animation.file_id)

        assert message.animation == animation

    def test_send_with_animation(self, monkeypatch, bot, chat_id, animation):
        def test(url, data, **kwargs):
            return data['animation'] == animation.file_id

        monkeypatch.setattr(bot.request, 'post', test)
        message = bot.send_animation(animation=animation, chat_id=chat_id)
        assert message

    def test_de_json(self, bot, animation):
        json_dict = {
            'file_id': self.animation_file_id,
            'file_unique_id': self.animation_file_unique_id,
            'width': self.width,
            'height': self.height,
            'duration': self.duration,
            'thumb': animation.thumb.to_dict(),
            'file_name': self.file_name,
            'mime_type': self.mime_type,
            'file_size': self.file_size,
        }
        animation = Animation.de_json(json_dict, bot)
        assert animation.file_id == self.animation_file_id
        assert animation.file_unique_id == self.animation_file_unique_id
        assert animation.thumb == animation.thumb
        assert animation.file_name == self.file_name
        assert animation.mime_type == self.mime_type
        assert animation.file_size == self.file_size

    def test_to_dict(self, animation):
        animation_dict = animation.to_dict()

        assert isinstance(animation_dict, dict)
        assert animation_dict['file_id'] == animation.file_id
        assert animation_dict['file_unique_id'] == animation.file_unique_id
        assert animation_dict['width'] == animation.width
        assert animation_dict['height'] == animation.height
        assert animation_dict['duration'] == animation.duration
        assert animation_dict['thumb'] == animation.thumb.to_dict()
        assert animation_dict['file_name'] == animation.file_name
        assert animation_dict['mime_type'] == animation.mime_type
        assert animation_dict['file_size'] == animation.file_size

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_error_send_empty_file(self, bot, chat_id):
        animation_file = open(os.devnull, 'rb')

        with pytest.raises(TelegramError):
            bot.send_animation(chat_id=chat_id, animation=animation_file)

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_error_send_empty_file_id(self, bot, chat_id):
        with pytest.raises(TelegramError):
            bot.send_animation(chat_id=chat_id, animation='')

    def test_error_send_without_required_args(self, bot, chat_id):
        with pytest.raises(TypeError):
            bot.send_animation(chat_id=chat_id)

    def test_get_file_instance_method(self, monkeypatch, animation):
        def test(*args, **kwargs):
            return args[1] == animation.file_id

        monkeypatch.setattr('telegram.Bot.get_file', test)
        assert animation.get_file()

    def test_equality(self):
        a = Animation(
            self.animation_file_id,
            self.animation_file_unique_id,
            self.height,
            self.width,
            self.duration,
        )
        b = Animation('', self.animation_file_unique_id, self.height, self.width, self.duration)
        d = Animation('', '', 0, 0, 0)
        e = Voice(self.animation_file_id, self.animation_file_unique_id, 0)

        assert a == b
        assert hash(a) == hash(b)
        assert a is not b

        assert a != d
        assert hash(a) != hash(d)

        assert a != e
        assert hash(a) != hash(e)
