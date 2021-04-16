#!/usr/bin/env python

import time
import datetime as dtm
from pathlib import Path
from platform import python_implementation

import pytest
from flaky import flaky

from telegram import (
    Bot,
    Update,
    ChatAction,
    TelegramError,
    User,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InlineQueryResultArticle,
    InputTextMessageContent,
    ShippingOption,
    LabeledPrice,
    ChatPermissions,
    Poll,
    BotCommand,
    InlineQueryResultDocument,
    Dice,
    MessageEntity,
    ParseMode,
)
from telegram.constants import MAX_INLINE_QUERY_RESULTS
from telegram.error import BadRequest, InvalidToken, NetworkError, RetryAfter
from telegram.utils.helpers import from_timestamp, escape_markdown, to_timestamp
from tests.conftest import expect_bad_request

BASE_TIME = time.time()
HIGHSCORE_DELTA = 1450000000


@pytest.fixture(scope='class')
def message(bot, chat_id):
    to_reply_to = bot.send_message(
        chat_id, 'Text', disable_web_page_preview=True, disable_notification=True
    )
    return bot.send_message(
        chat_id,
        'Text',
        reply_to_message_id=to_reply_to.message_id,
        disable_web_page_preview=True,
        disable_notification=True,
    )


@pytest.fixture(scope='class')
def media_message(bot, chat_id):
    with open('tests/data/telegram.ogg', 'rb') as f:
        return bot.send_voice(chat_id, voice=f, caption='my caption', timeout=10)


@pytest.fixture(scope='class')
def chat_permissions():
    return ChatPermissions(can_send_messages=False, can_change_info=False, can_invite_users=False)


def inline_results_callback(page=None):
    if not page:
        return [InlineQueryResultArticle(i, str(i), None) for i in range(1, 254)]
    elif page <= 5:
        return [
            InlineQueryResultArticle(i, str(i), None)
            for i in range(page * 5 + 1, (page + 1) * 5 + 1)
        ]
    return None


@pytest.fixture(scope='class')
def inline_results():
    return inline_results_callback()


class TestBot:
    @pytest.mark.parametrize(
        'token',
        argvalues=[
            '123',
            '12a:abcd1234',
            '12:abcd1234',
            '1234:abcd1234\n',
            ' 1234:abcd1234',
            ' 1234:abcd1234\r',
            '1234:abcd 1234',
        ],
    )
    def test_invalid_token(self, token):
        with pytest.raises(InvalidToken, match='Invalid token'):
            Bot(token)

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_invalid_token_server_response(self, monkeypatch):
        monkeypatch.setattr('telegram.Bot._validate_token', lambda x, y: True)
        bot = Bot('12')
        with pytest.raises(InvalidToken):
            bot.get_me()

    def test_unknown_kwargs(self, bot, monkeypatch):
        def post(url, data, timeout):
            assert data['unknown_kwarg_1'] == 7
            assert data['unknown_kwarg_2'] == 5

        monkeypatch.setattr(bot.request, 'post', post)
        bot.send_message(123, 'text', api_kwargs={'unknown_kwarg_1': 7, 'unknown_kwarg_2': 5})

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_get_me_and_properties(self, bot):
        get_me_bot = bot.get_me()
        commands = bot.get_my_commands()

        assert isinstance(get_me_bot, User)
        assert get_me_bot.id == bot.id
        assert get_me_bot.username == bot.username
        assert get_me_bot.first_name == bot.first_name
        assert get_me_bot.last_name == bot.last_name
        assert get_me_bot.name == bot.name
        assert get_me_bot.can_join_groups == bot.can_join_groups
        assert get_me_bot.can_read_all_group_messages == bot.can_read_all_group_messages
        assert get_me_bot.supports_inline_queries == bot.supports_inline_queries
        assert f'https://t.me/{get_me_bot.username}' == bot.link
        assert commands == bot.commands

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_to_dict(self, bot):
        to_dict_bot = bot.to_dict()

        assert isinstance(to_dict_bot, dict)
        assert to_dict_bot["id"] == bot.id
        assert to_dict_bot["username"] == bot.username
        assert to_dict_bot["first_name"] == bot.first_name
        if bot.last_name:
            assert to_dict_bot["last_name"] == bot.last_name

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_forward_message(self, bot, chat_id, message):
        message = bot.forward_message(chat_id, from_chat_id=chat_id, message_id=message.message_id)

        assert message.text == message.text
        assert message.forward_from.username == message.from_user.username
        assert isinstance(message.forward_date, dtm.datetime)

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_delete_message(self, bot, chat_id):
        message = bot.send_message(chat_id, text='will be deleted')
        time.sleep(2)

        assert bot.delete_message(chat_id=chat_id, message_id=message.message_id) is True

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_delete_message_old_message(self, bot, chat_id):
        with pytest.raises(BadRequest):
            # Considering that the first message is old enough
            bot.delete_message(chat_id=chat_id, message_id=1)

    # send_photo, send_audio, send_document, send_sticker, send_video, send_voice, send_video_note,
    # send_media_group and send_animation are tested in their respective test modules. No need to
    # duplicate here.

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_send_venue(self, bot, chat_id):
        longitude = -46.788279
        latitude = -23.691288
        title = 'title'
        address = 'address'
        foursquare_id = 'foursquare id'
        foursquare_type = 'foursquare type'
        google_place_id = 'google_place id'
        google_place_type = 'google_place type'

        message = bot.send_venue(
            chat_id=chat_id,
            title=title,
            address=address,
            latitude=latitude,
            longitude=longitude,
            foursquare_id=foursquare_id,
            foursquare_type=foursquare_type,
        )

        assert message.venue
        assert message.venue.title == title
        assert message.venue.address == address
        assert message.venue.location.latitude == latitude
        assert message.venue.location.longitude == longitude
        assert message.venue.foursquare_id == foursquare_id
        assert message.venue.foursquare_type == foursquare_type
        assert message.venue.google_place_id is None
        assert message.venue.google_place_type is None

        message = bot.send_venue(
            chat_id=chat_id,
            title=title,
            address=address,
            latitude=latitude,
            longitude=longitude,
            google_place_id=google_place_id,
            google_place_type=google_place_type,
        )

        assert message.venue
        assert message.venue.title == title
        assert message.venue.address == address
        assert message.venue.location.latitude == latitude
        assert message.venue.location.longitude == longitude
        assert message.venue.google_place_id == google_place_id
        assert message.venue.google_place_type == google_place_type
        assert message.venue.foursquare_id is None
        assert message.venue.foursquare_type is None

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    @pytest.mark.xfail(raises=RetryAfter)
    @pytest.mark.skipif(
        python_implementation() == 'PyPy', reason='Unstable on pypy for some reason'
    )
    def test_send_contact(self, bot, chat_id):
        phone_number = '+11234567890'
        first_name = 'Leandro'
        last_name = 'Toledo'
        message = bot.send_contact(
            chat_id=chat_id, phone_number=phone_number, first_name=first_name, last_name=last_name
        )

        assert message.contact
        assert message.contact.phone_number == phone_number
        assert message.contact.first_name == first_name
        assert message.contact.last_name == last_name

    # TODO: Add bot to group to test polls too

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    @pytest.mark.parametrize(
        'reply_markup',
        [
            None,
            InlineKeyboardMarkup.from_button(
                InlineKeyboardButton(text='text', callback_data='data')
            ),
            InlineKeyboardMarkup.from_button(
                InlineKeyboardButton(text='text', callback_data='data')
            ).to_dict(),
        ],
    )
    def test_send_and_stop_poll(self, bot, super_group_id, reply_markup):
        question = 'Is this a test?'
        answers = ['Yes', 'No', 'Maybe']
        message = bot.send_poll(
            chat_id=super_group_id,
            question=question,
            options=answers,
            is_anonymous=False,
            allows_multiple_answers=True,
            timeout=60,
        )

        assert message.poll
        assert message.poll.question == question
        assert message.poll.options[0].text == answers[0]
        assert message.poll.options[1].text == answers[1]
        assert message.poll.options[2].text == answers[2]
        assert not message.poll.is_anonymous
        assert message.poll.allows_multiple_answers
        assert not message.poll.is_closed
        assert message.poll.type == Poll.REGULAR

        # Since only the poll and not the complete message is returned, we can't check that the
        # reply_markup is correct. So we just test that sending doesn't give an error.
        poll = bot.stop_poll(
            chat_id=super_group_id,
            message_id=message.message_id,
            reply_markup=reply_markup,
            timeout=60,
        )
        assert isinstance(poll, Poll)
        assert poll.is_closed
        assert poll.options[0].text == answers[0]
        assert poll.options[0].voter_count == 0
        assert poll.options[1].text == answers[1]
        assert poll.options[1].voter_count == 0
        assert poll.options[2].text == answers[2]
        assert poll.options[2].voter_count == 0
        assert poll.question == question
        assert poll.total_voter_count == 0

        explanation = '[Here is a link](https://google.com)'
        explanation_entities = [
            MessageEntity(MessageEntity.TEXT_LINK, 0, 14, url='https://google.com')
        ]
        message_quiz = bot.send_poll(
            chat_id=super_group_id,
            question=question,
            options=answers,
            type=Poll.QUIZ,
            correct_option_id=2,
            is_closed=True,
            explanation=explanation,
            explanation_parse_mode=ParseMode.MARKDOWN_V2,
        )
        assert message_quiz.poll.correct_option_id == 2
        assert message_quiz.poll.type == Poll.QUIZ
        assert message_quiz.poll.is_closed
        assert message_quiz.poll.explanation == 'Here is a link'
        assert message_quiz.poll.explanation_entities == explanation_entities

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    @pytest.mark.parametrize(['open_period', 'close_date'], [(5, None), (None, True)])
    def test_send_open_period(self, bot, super_group_id, open_period, close_date):
        question = 'Is this a test?'
        answers = ['Yes', 'No', 'Maybe']
        reply_markup = InlineKeyboardMarkup.from_button(
            InlineKeyboardButton(text='text', callback_data='data')
        )

        if close_date:
            close_date = dtm.datetime.utcnow() + dtm.timedelta(seconds=5)

        message = bot.send_poll(
            chat_id=super_group_id,
            question=question,
            options=answers,
            is_anonymous=False,
            allows_multiple_answers=True,
            timeout=60,
            open_period=open_period,
            close_date=close_date,
        )
        time.sleep(5.1)
        new_message = bot.edit_message_reply_markup(
            chat_id=super_group_id,
            message_id=message.message_id,
            reply_markup=reply_markup,
            timeout=60,
        )
        assert new_message.poll.id == message.poll.id
        assert new_message.poll.is_closed

    @flaky(5, 1)
    @pytest.mark.timeout(10)
    def test_send_close_date_default_tz(self, tz_bot, super_group_id):
        question = 'Is this a test?'
        answers = ['Yes', 'No', 'Maybe']
        reply_markup = InlineKeyboardMarkup.from_button(
            InlineKeyboardButton(text='text', callback_data='data')
        )

        aware_close_date = dtm.datetime.now(tz=tz_bot.defaults.tzinfo) + dtm.timedelta(seconds=5)
        close_date = aware_close_date.replace(tzinfo=None)

        message = tz_bot.send_poll(
            chat_id=super_group_id,
            question=question,
            options=answers,
            close_date=close_date,
            timeout=60,
        )
        assert message.poll.close_date == aware_close_date.replace(microsecond=0)

        time.sleep(5.1)

        new_message = tz_bot.edit_message_reply_markup(
            chat_id=super_group_id,
            message_id=message.message_id,
            reply_markup=reply_markup,
            timeout=60,
        )
        assert new_message.poll.id == message.poll.id
        assert new_message.poll.is_closed

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_send_poll_explanation_entities(self, bot, chat_id):
        test_string = 'Italic Bold Code'
        entities = [
            MessageEntity(MessageEntity.ITALIC, 0, 6),
            MessageEntity(MessageEntity.ITALIC, 7, 4),
            MessageEntity(MessageEntity.ITALIC, 12, 4),
        ]
        message = bot.send_poll(
            chat_id,
            'question',
            options=['a', 'b'],
            correct_option_id=0,
            type=Poll.QUIZ,
            explanation=test_string,
            explanation_entities=entities,
        )

        assert message.poll.explanation == test_string
        assert message.poll.explanation_entities == entities

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    @pytest.mark.parametrize('default_bot', [{'parse_mode': 'Markdown'}], indirect=True)
    def test_send_poll_default_parse_mode(self, default_bot, super_group_id):
        explanation = 'Italic Bold Code'
        explanation_markdown = '_Italic_ *Bold* `Code`'
        question = 'Is this a test?'
        answers = ['Yes', 'No', 'Maybe']

        message = default_bot.send_poll(
            chat_id=super_group_id,
            question=question,
            options=answers,
            type=Poll.QUIZ,
            correct_option_id=2,
            is_closed=True,
            explanation=explanation_markdown,
        )
        assert message.poll.explanation == explanation
        assert message.poll.explanation_entities == [
            MessageEntity(MessageEntity.ITALIC, 0, 6),
            MessageEntity(MessageEntity.BOLD, 7, 4),
            MessageEntity(MessageEntity.CODE, 12, 4),
        ]

        message = default_bot.send_poll(
            chat_id=super_group_id,
            question=question,
            options=answers,
            type=Poll.QUIZ,
            correct_option_id=2,
            is_closed=True,
            explanation=explanation_markdown,
            explanation_parse_mode=None,
        )
        assert message.poll.explanation == explanation_markdown
        assert message.poll.explanation_entities == []

        message = default_bot.send_poll(
            chat_id=super_group_id,
            question=question,
            options=answers,
            type=Poll.QUIZ,
            correct_option_id=2,
            is_closed=True,
            explanation=explanation_markdown,
            explanation_parse_mode='HTML',
        )
        assert message.poll.explanation == explanation_markdown
        assert message.poll.explanation_entities == []

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
    def test_send_poll_default_allow_sending_without_reply(self, default_bot, chat_id, custom):
        question = 'Is this a test?'
        answers = ['Yes', 'No', 'Maybe']
        reply_to_message = default_bot.send_message(chat_id, 'test')
        reply_to_message.delete()
        if custom is not None:
            message = default_bot.send_poll(
                chat_id,
                question=question,
                options=answers,
                allow_sending_without_reply=custom,
                reply_to_message_id=reply_to_message.message_id,
            )
            assert message.reply_to_message is None
        elif default_bot.defaults.allow_sending_without_reply:
            message = default_bot.send_poll(
                chat_id,
                question=question,
                options=answers,
                reply_to_message_id=reply_to_message.message_id,
            )
            assert message.reply_to_message is None
        else:
            with pytest.raises(BadRequest, match='message not found'):
                default_bot.send_poll(
                    chat_id,
                    question=question,
                    options=answers,
                    reply_to_message_id=reply_to_message.message_id,
                )

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    @pytest.mark.parametrize('emoji', Dice.ALL_EMOJI + [None])
    def test_send_dice(self, bot, chat_id, emoji):
        message = bot.send_dice(chat_id, emoji=emoji)

        assert message.dice
        if emoji is None:
            assert message.dice.emoji == Dice.DICE
        else:
            assert message.dice.emoji == emoji

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
    def test_send_dice_default_allow_sending_without_reply(self, default_bot, chat_id, custom):
        reply_to_message = default_bot.send_message(chat_id, 'test')
        reply_to_message.delete()
        if custom is not None:
            message = default_bot.send_dice(
                chat_id,
                allow_sending_without_reply=custom,
                reply_to_message_id=reply_to_message.message_id,
            )
            assert message.reply_to_message is None
        elif default_bot.defaults.allow_sending_without_reply:
            message = default_bot.send_dice(
                chat_id,
                reply_to_message_id=reply_to_message.message_id,
            )
            assert message.reply_to_message is None
        else:
            with pytest.raises(BadRequest, match='message not found'):
                default_bot.send_dice(chat_id, reply_to_message_id=reply_to_message.message_id)

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_send_chat_action(self, bot, chat_id):
        assert bot.send_chat_action(chat_id, ChatAction.TYPING)

    # TODO: Needs improvement. We need incoming inline query to test answer.
    def test_answer_inline_query(self, monkeypatch, bot):
        # For now just test that our internals pass the correct data
        def test(url, data, *args, **kwargs):
            return data == {
                'cache_time': 300,
                'results': [
                    {
                        'title': 'first',
                        'id': '11',
                        'type': 'article',
                        'input_message_content': {'message_text': 'first'},
                    },
                    {
                        'title': 'second',
                        'id': '12',
                        'type': 'article',
                        'input_message_content': {'message_text': 'second'},
                    },
                ],
                'next_offset': '42',
                'switch_pm_parameter': 'start_pm',
                'inline_query_id': 1234,
                'is_personal': True,
                'switch_pm_text': 'switch pm',
            }

        monkeypatch.setattr(bot.request, 'post', test)
        results = [
            InlineQueryResultArticle('11', 'first', InputTextMessageContent('first')),
            InlineQueryResultArticle('12', 'second', InputTextMessageContent('second')),
        ]

        assert bot.answer_inline_query(
            1234,
            results=results,
            cache_time=300,
            is_personal=True,
            next_offset='42',
            switch_pm_text='switch pm',
            switch_pm_parameter='start_pm',
        )

    def test_answer_inline_query_no_default_parse_mode(self, monkeypatch, bot):
        def test(url, data, *args, **kwargs):
            return data == {
                'cache_time': 300,
                'results': [
                    {
                        'title': 'test_result',
                        'id': '123',
                        'type': 'document',
                        'document_url': 'https://raw.githubusercontent.com/'
                        'python-telegram-bot/logos/master/logo/png/'
                        'ptb-logo_240.png',
                        'mime_type': 'image/png',
                        'caption': 'ptb_logo',
                    }
                ],
                'next_offset': '42',
                'switch_pm_parameter': 'start_pm',
                'inline_query_id': 1234,
                'is_personal': True,
                'switch_pm_text': 'switch pm',
            }

        monkeypatch.setattr(bot.request, 'post', test)
        results = [
            InlineQueryResultDocument(
                id='123',
                document_url='https://raw.githubusercontent.com/python-telegram-bot/logos/master/'
                'logo/png/ptb-logo_240.png',
                title='test_result',
                mime_type='image/png',
                caption='ptb_logo',
            )
        ]

        assert bot.answer_inline_query(
            1234,
            results=results,
            cache_time=300,
            is_personal=True,
            next_offset='42',
            switch_pm_text='switch pm',
            switch_pm_parameter='start_pm',
        )

    @pytest.mark.parametrize('default_bot', [{'parse_mode': 'Markdown'}], indirect=True)
    def test_answer_inline_query_default_parse_mode(self, monkeypatch, default_bot):
        def test(url, data, *args, **kwargs):
            return data == {
                'cache_time': 300,
                'results': [
                    {
                        'title': 'test_result',
                        'id': '123',
                        'type': 'document',
                        'document_url': 'https://raw.githubusercontent.com/'
                        'python-telegram-bot/logos/master/logo/png/'
                        'ptb-logo_240.png',
                        'mime_type': 'image/png',
                        'caption': 'ptb_logo',
                        'parse_mode': 'Markdown',
                    }
                ],
                'next_offset': '42',
                'switch_pm_parameter': 'start_pm',
                'inline_query_id': 1234,
                'is_personal': True,
                'switch_pm_text': 'switch pm',
            }

        monkeypatch.setattr(default_bot.request, 'post', test)
        results = [
            InlineQueryResultDocument(
                id='123',
                document_url='https://raw.githubusercontent.com/python-telegram-bot/logos/master/'
                'logo/png/ptb-logo_240.png',
                title='test_result',
                mime_type='image/png',
                caption='ptb_logo',
            )
        ]

        assert default_bot.answer_inline_query(
            1234,
            results=results,
            cache_time=300,
            is_personal=True,
            next_offset='42',
            switch_pm_text='switch pm',
            switch_pm_parameter='start_pm',
        )

    def test_answer_inline_query_current_offset_error(self, bot, inline_results):
        with pytest.raises(ValueError, match=('`current_offset` and `next_offset`')):
            bot.answer_inline_query(
                1234, results=inline_results, next_offset=42, current_offset=51
            )

    @pytest.mark.parametrize(
        'current_offset,num_results,id_offset,expected_next_offset',
        [
            ('', MAX_INLINE_QUERY_RESULTS, 1, 1),
            (1, MAX_INLINE_QUERY_RESULTS, 51, 2),
            (5, 3, 251, ''),
        ],
    )
    def test_answer_inline_query_current_offset_1(
        self,
        monkeypatch,
        bot,
        inline_results,
        current_offset,
        num_results,
        id_offset,
        expected_next_offset,
    ):
        # For now just test that our internals pass the correct data
        def make_assertion(url, data, *args, **kwargs):
            results = data['results']
            length_matches = len(results) == num_results
            ids_match = all([int(res['id']) == id_offset + i for i, res in enumerate(results)])
            next_offset_matches = data['next_offset'] == str(expected_next_offset)
            return length_matches and ids_match and next_offset_matches

        monkeypatch.setattr(bot.request, 'post', make_assertion)

        assert bot.answer_inline_query(1234, results=inline_results, current_offset=current_offset)

    def test_answer_inline_query_current_offset_2(self, monkeypatch, bot, inline_results):
        # For now just test that our internals pass the correct data
        def make_assertion(url, data, *args, **kwargs):
            results = data['results']
            length_matches = len(results) == MAX_INLINE_QUERY_RESULTS
            ids_match = all([int(res['id']) == 1 + i for i, res in enumerate(results)])
            next_offset_matches = data['next_offset'] == '1'
            return length_matches and ids_match and next_offset_matches

        monkeypatch.setattr(bot.request, 'post', make_assertion)

        assert bot.answer_inline_query(1234, results=inline_results, current_offset=0)

        inline_results = inline_results[:30]

        def make_assertion(url, data, *args, **kwargs):
            results = data['results']
            length_matches = len(results) == 30
            ids_match = all([int(res['id']) == 1 + i for i, res in enumerate(results)])
            next_offset_matches = data['next_offset'] == ''
            return length_matches and ids_match and next_offset_matches

        monkeypatch.setattr(bot.request, 'post', make_assertion)

        assert bot.answer_inline_query(1234, results=inline_results, current_offset=0)

    def test_answer_inline_query_current_offset_callback(self, monkeypatch, bot, caplog):
        # For now just test that our internals pass the correct data
        def make_assertion(url, data, *args, **kwargs):
            results = data['results']
            length = len(results) == 5
            ids = all([int(res['id']) == 6 + i for i, res in enumerate(results)])
            next_offset = data['next_offset'] == '2'
            return length and ids and next_offset

        monkeypatch.setattr(bot.request, 'post', make_assertion)

        assert bot.answer_inline_query(1234, results=inline_results_callback, current_offset=1)

        def make_assertion(url, data, *args, **kwargs):
            results = data['results']
            length = results == []
            next_offset = data['next_offset'] == ''
            return length and next_offset

        monkeypatch.setattr(bot.request, 'post', make_assertion)

        assert bot.answer_inline_query(1234, results=inline_results_callback, current_offset=6)

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_get_user_profile_photos(self, bot, chat_id):
        user_profile_photos = bot.get_user_profile_photos(chat_id)

        assert user_profile_photos.photos[0][0].file_size == 5403

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_get_one_user_profile_photo(self, bot, chat_id):
        user_profile_photos = bot.get_user_profile_photos(chat_id, offset=0, limit=1)
        assert user_profile_photos.photos[0][0].file_size == 5403

    # get_file is tested multiple times in the test_*media* modules.
    # Here we only test the behaviour for bot apis in local mode
    def test_get_file_local_mode(self, bot, monkeypatch):
        path = str(Path.cwd() / 'tests' / 'data' / 'game.gif')

        def _post(*args, **kwargs):
            return {
                'file_id': None,
                'file_unique_id': None,
                'file_size': None,
                'file_path': path,
            }

        monkeypatch.setattr(bot, '_post', _post)

        resulting_path = bot.get_file('file_id').file_path
        assert bot.token not in resulting_path
        assert resulting_path == path

    # TODO: Needs improvement. No feasable way to test until bots can add members.
    def test_kick_chat_member(self, monkeypatch, bot):
        def test(url, data, *args, **kwargs):
            chat_id = data['chat_id'] == 2
            user_id = data['user_id'] == 32
            until_date = data.get('until_date', 1577887200) == 1577887200
            return chat_id and user_id and until_date

        monkeypatch.setattr(bot.request, 'post', test)
        until = from_timestamp(1577887200)

        assert bot.kick_chat_member(2, 32)
        assert bot.kick_chat_member(2, 32, until_date=until)
        assert bot.kick_chat_member(2, 32, until_date=1577887200)

    def test_kick_chat_member_default_tz(self, monkeypatch, tz_bot):
        until = dtm.datetime(2020, 1, 11, 16, 13)
        until_timestamp = to_timestamp(until, tzinfo=tz_bot.defaults.tzinfo)

        def test(url, data, *args, **kwargs):
            chat_id = data['chat_id'] == 2
            user_id = data['user_id'] == 32
            until_date = data.get('until_date', until_timestamp) == until_timestamp
            return chat_id and user_id and until_date

        monkeypatch.setattr(tz_bot.request, 'post', test)

        assert tz_bot.kick_chat_member(2, 32)
        assert tz_bot.kick_chat_member(2, 32, until_date=until)
        assert tz_bot.kick_chat_member(2, 32, until_date=until_timestamp)

    # TODO: Needs improvement.
    @pytest.mark.parametrize('only_if_banned', [True, False, None])
    def test_unban_chat_member(self, monkeypatch, bot, only_if_banned):
        def make_assertion(url, data, *args, **kwargs):
            chat_id = data['chat_id'] == 2
            user_id = data['user_id'] == 32
            o_i_b = data.get('only_if_banned', None) == only_if_banned
            return chat_id and user_id and o_i_b

        monkeypatch.setattr(bot.request, 'post', make_assertion)

        assert bot.unban_chat_member(2, 32, only_if_banned=only_if_banned)

    def test_set_chat_permissions(self, monkeypatch, bot, chat_permissions):
        def test(url, data, *args, **kwargs):
            chat_id = data['chat_id'] == 2
            permissions = data['permissions'] == chat_permissions.to_dict()
            return chat_id and permissions

        monkeypatch.setattr(bot.request, 'post', test)

        assert bot.set_chat_permissions(2, chat_permissions)

    def test_set_chat_administrator_custom_title(self, monkeypatch, bot):
        def test(url, data, *args, **kwargs):
            chat_id = data['chat_id'] == 2
            user_id = data['user_id'] == 32
            custom_title = data['custom_title'] == 'custom_title'
            return chat_id and user_id and custom_title

        monkeypatch.setattr(bot.request, 'post', test)
        assert bot.set_chat_administrator_custom_title(2, 32, 'custom_title')

    # TODO: Needs improvement. Need an incoming callbackquery to test
    def test_answer_callback_query(self, monkeypatch, bot):
        # For now just test that our internals pass the correct data
        def test(url, data, *args, **kwargs):
            return data == {
                'callback_query_id': 23,
                'show_alert': True,
                'url': 'no_url',
                'cache_time': 1,
                'text': 'answer',
            }

        monkeypatch.setattr(bot.request, 'post', test)

        assert bot.answer_callback_query(
            23, text='answer', show_alert=True, url='no_url', cache_time=1
        )

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_edit_message_text(self, bot, message):
        message = bot.edit_message_text(
            text='new_text',
            chat_id=message.chat_id,
            message_id=message.message_id,
            parse_mode='HTML',
            disable_web_page_preview=True,
        )

        assert message.text == 'new_text'

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_edit_message_text_entities(self, bot, message):
        test_string = 'Italic Bold Code'
        entities = [
            MessageEntity(MessageEntity.ITALIC, 0, 6),
            MessageEntity(MessageEntity.ITALIC, 7, 4),
            MessageEntity(MessageEntity.ITALIC, 12, 4),
        ]
        message = bot.edit_message_text(
            text=test_string,
            chat_id=message.chat_id,
            message_id=message.message_id,
            entities=entities,
        )

        assert message.text == test_string
        assert message.entities == entities

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    @pytest.mark.parametrize('default_bot', [{'parse_mode': 'Markdown'}], indirect=True)
    def test_edit_message_text_default_parse_mode(self, default_bot, message):
        test_string = 'Italic Bold Code'
        test_markdown_string = '_Italic_ *Bold* `Code`'

        message = default_bot.edit_message_text(
            text=test_markdown_string,
            chat_id=message.chat_id,
            message_id=message.message_id,
            disable_web_page_preview=True,
        )
        assert message.text_markdown == test_markdown_string
        assert message.text == test_string

        message = default_bot.edit_message_text(
            text=test_markdown_string,
            chat_id=message.chat_id,
            message_id=message.message_id,
            parse_mode=None,
            disable_web_page_preview=True,
        )
        assert message.text == test_markdown_string
        assert message.text_markdown == escape_markdown(test_markdown_string)

        message = default_bot.edit_message_text(
            text=test_markdown_string,
            chat_id=message.chat_id,
            message_id=message.message_id,
            disable_web_page_preview=True,
        )
        message = default_bot.edit_message_text(
            text=test_markdown_string,
            chat_id=message.chat_id,
            message_id=message.message_id,
            parse_mode='HTML',
            disable_web_page_preview=True,
        )
        assert message.text == test_markdown_string
        assert message.text_markdown == escape_markdown(test_markdown_string)

    @pytest.mark.skip(reason='need reference to an inline message')
    def test_edit_message_text_inline(self):
        pass

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_edit_message_caption(self, bot, media_message):
        message = bot.edit_message_caption(
            caption='new_caption',
            chat_id=media_message.chat_id,
            message_id=media_message.message_id,
        )

        assert message.caption == 'new_caption'

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_edit_message_caption_entities(self, bot, media_message):
        test_string = 'Italic Bold Code'
        entities = [
            MessageEntity(MessageEntity.ITALIC, 0, 6),
            MessageEntity(MessageEntity.ITALIC, 7, 4),
            MessageEntity(MessageEntity.ITALIC, 12, 4),
        ]
        message = bot.edit_message_caption(
            caption=test_string,
            chat_id=media_message.chat_id,
            message_id=media_message.message_id,
            caption_entities=entities,
        )

        assert message.caption == test_string
        assert message.caption_entities == entities

    # edit_message_media is tested in test_inputmedia

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    @pytest.mark.parametrize('default_bot', [{'parse_mode': 'Markdown'}], indirect=True)
    def test_edit_message_caption_default_parse_mode(self, default_bot, media_message):
        test_string = 'Italic Bold Code'
        test_markdown_string = '_Italic_ *Bold* `Code`'

        message = default_bot.edit_message_caption(
            caption=test_markdown_string,
            chat_id=media_message.chat_id,
            message_id=media_message.message_id,
        )
        assert message.caption_markdown == test_markdown_string
        assert message.caption == test_string

        message = default_bot.edit_message_caption(
            caption=test_markdown_string,
            chat_id=media_message.chat_id,
            message_id=media_message.message_id,
            parse_mode=None,
        )
        assert message.caption == test_markdown_string
        assert message.caption_markdown == escape_markdown(test_markdown_string)

        message = default_bot.edit_message_caption(
            caption=test_markdown_string,
            chat_id=media_message.chat_id,
            message_id=media_message.message_id,
        )
        message = default_bot.edit_message_caption(
            caption=test_markdown_string,
            chat_id=media_message.chat_id,
            message_id=media_message.message_id,
            parse_mode='HTML',
        )
        assert message.caption == test_markdown_string
        assert message.caption_markdown == escape_markdown(test_markdown_string)

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_edit_message_caption_with_parse_mode(self, bot, media_message):
        message = bot.edit_message_caption(
            caption='new *caption*',
            parse_mode='Markdown',
            chat_id=media_message.chat_id,
            message_id=media_message.message_id,
        )

        assert message.caption == 'new caption'

    def test_edit_message_caption_without_required(self, bot):
        with pytest.raises(ValueError, match='Both chat_id and message_id are required when'):
            bot.edit_message_caption(caption='new_caption')

    @pytest.mark.skip(reason='need reference to an inline message')
    def test_edit_message_caption_inline(self):
        pass

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_edit_reply_markup(self, bot, message):
        new_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text='test', callback_data='1')]])
        message = bot.edit_message_reply_markup(
            chat_id=message.chat_id, message_id=message.message_id, reply_markup=new_markup
        )

        assert message is not True

    def test_edit_message_reply_markup_without_required(self, bot):
        new_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text='test', callback_data='1')]])
        with pytest.raises(ValueError, match='Both chat_id and message_id are required when'):
            bot.edit_message_reply_markup(reply_markup=new_markup)

    @pytest.mark.skip(reason='need reference to an inline message')
    def test_edit_reply_markup_inline(self):
        pass

    # TODO: Actually send updates to the test bot so this can be tested properly
    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_get_updates(self, bot):
        bot.delete_webhook()  # make sure there is no webhook set if webhook tests failed
        updates = bot.get_updates(timeout=1)

        assert isinstance(updates, list)
        if updates:
            assert isinstance(updates[0], Update)

    @flaky(3, 1)
    @pytest.mark.timeout(15)
    @pytest.mark.xfail
    def test_set_webhook_get_webhook_info_and_delete_webhook(self, bot):
        url = 'https://python-telegram-bot.org/test/webhook'
        max_connections = 7
        allowed_updates = ['message']
        bot.set_webhook(
            url,
            max_connections=max_connections,
            allowed_updates=allowed_updates,
            ip_address='127.0.0.1',
        )
        time.sleep(2)
        live_info = bot.get_webhook_info()
        time.sleep(6)
        bot.delete_webhook()
        time.sleep(2)
        info = bot.get_webhook_info()
        assert info.url == ''
        assert live_info.url == url
        assert live_info.max_connections == max_connections
        assert live_info.allowed_updates == allowed_updates
        assert live_info.ip_address == '127.0.0.1'

    @pytest.mark.parametrize('drop_pending_updates', [True, False])
    def test_set_webhook_delete_webhook_drop_pending_updates(
        self, bot, drop_pending_updates, monkeypatch
    ):
        def assertion(url, data, *args, **kwargs):
            return bool(data.get('drop_pending_updates')) == drop_pending_updates

        monkeypatch.setattr(bot.request, 'post', assertion)

        assert bot.set_webhook(drop_pending_updates=drop_pending_updates)
        assert bot.delete_webhook(drop_pending_updates=drop_pending_updates)

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_leave_chat(self, bot):
        with pytest.raises(BadRequest, match='Chat not found'):
            bot.leave_chat(-123456)

        with pytest.raises(NetworkError, match='Chat not found'):
            bot.leave_chat(-123456)

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_get_chat(self, bot, super_group_id):
        chat = bot.get_chat(super_group_id)

        assert chat.type == 'supergroup'
        assert chat.title == f'>>> telegram.Bot(test) @{bot.username}'
        assert chat.id == int(super_group_id)

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_get_chat_administrators(self, bot, channel_id):
        admins = bot.get_chat_administrators(channel_id)
        assert isinstance(admins, list)

        for a in admins:
            assert a.status in ('administrator', 'creator')

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_get_chat_members_count(self, bot, channel_id):
        count = bot.get_chat_members_count(channel_id)
        assert isinstance(count, int)
        assert count > 3

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_get_chat_member(self, bot, channel_id, chat_id):
        chat_member = bot.get_chat_member(channel_id, chat_id)

        assert chat_member.status == 'administrator'
        assert chat_member.user.first_name == 'PTB'
        assert chat_member.user.last_name == 'Test user'

    @pytest.mark.skip(reason="Not implemented yet.")
    def test_set_chat_sticker_set(self):
        pass

    @pytest.mark.skip(reason="Not implemented yet.")
    def test_delete_chat_sticker_set(self):
        pass

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_send_game(self, bot, chat_id):
        game_short_name = 'test_game'
        message = bot.send_game(chat_id, game_short_name)

        assert message.game
        assert message.game.description == (
            'A no-op test game, for python-telegram-bot ' 'bot framework testing.'
        )
        assert message.game.animation.file_id != ''
        assert message.game.photo[0].file_size == 851

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
    def test_send_game_default_allow_sending_without_reply(self, default_bot, chat_id, custom):
        game_short_name = 'test_game'
        reply_to_message = default_bot.send_message(chat_id, 'test')
        reply_to_message.delete()
        if custom is not None:
            message = default_bot.send_game(
                chat_id,
                game_short_name,
                allow_sending_without_reply=custom,
                reply_to_message_id=reply_to_message.message_id,
            )
            assert message.reply_to_message is None
        elif default_bot.defaults.allow_sending_without_reply:
            message = default_bot.send_game(
                chat_id,
                game_short_name,
                reply_to_message_id=reply_to_message.message_id,
            )
            assert message.reply_to_message is None
        else:
            with pytest.raises(BadRequest, match='message not found'):
                default_bot.send_game(
                    chat_id, game_short_name, reply_to_message_id=reply_to_message.message_id
                )

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_set_game_score_1(self, bot, chat_id):
        # NOTE: numbering of methods assures proper order between test_set_game_scoreX methods

        def func():
            game_short_name = 'test_game'
            game = bot.send_game(chat_id, game_short_name)

            message = bot.set_game_score(
                user_id=chat_id,
                score=int(BASE_TIME) - HIGHSCORE_DELTA,
                chat_id=game.chat_id,
                message_id=game.message_id,
            )

            assert message.game.description == game.game.description
            assert message.game.animation.file_id == game.game.animation.file_id
            assert message.game.photo[0].file_size == game.game.photo[0].file_size
            assert message.game.text != game.game.text

        expect_bad_request(func, 'Bot_score_not_modified', 'This test is a diva for some reason.')

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_set_game_score_2(self, bot, chat_id):
        # NOTE: numbering of methods assures proper order between test_set_game_scoreX methods
        game_short_name = 'test_game'
        game = bot.send_game(chat_id, game_short_name)

        score = int(BASE_TIME) - HIGHSCORE_DELTA + 1

        message = bot.set_game_score(
            user_id=chat_id,
            score=score,
            chat_id=game.chat_id,
            message_id=game.message_id,
            disable_edit_message=True,
        )

        assert message.game.description == game.game.description
        assert message.game.animation.file_id == game.game.animation.file_id
        assert message.game.photo[0].file_size == game.game.photo[0].file_size
        assert message.game.text == game.game.text

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_set_game_score_3(self, bot, chat_id):
        # NOTE: numbering of methods assures proper order between test_set_game_scoreX methods
        game_short_name = 'test_game'
        game = bot.send_game(chat_id, game_short_name)

        score = int(BASE_TIME) - HIGHSCORE_DELTA - 1

        with pytest.raises(BadRequest, match='Bot_score_not_modified'):
            bot.set_game_score(
                user_id=chat_id, score=score, chat_id=game.chat_id, message_id=game.message_id
            )

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_set_game_score_4(self, bot, chat_id):
        # NOTE: numbering of methods assures proper order between test_set_game_scoreX methods
        game_short_name = 'test_game'
        game = bot.send_game(chat_id, game_short_name)

        score = int(BASE_TIME) - HIGHSCORE_DELTA - 2

        message = bot.set_game_score(
            user_id=chat_id,
            score=score,
            chat_id=game.chat_id,
            message_id=game.message_id,
            force=True,
        )

        assert message.game.description == game.game.description
        assert message.game.animation.file_id == game.game.animation.file_id
        assert message.game.photo[0].file_size == game.game.photo[0].file_size

        # For some reason the returned message does not contain the updated score. need to fetch
        # the game again...
        game2 = bot.send_game(chat_id, game_short_name)
        assert str(score) in game2.game.text

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_set_game_score_too_low_score(self, bot, chat_id):
        # We need a game to set the score for
        game_short_name = 'test_game'
        game = bot.send_game(chat_id, game_short_name)

        with pytest.raises(BadRequest):
            bot.set_game_score(
                user_id=chat_id, score=100, chat_id=game.chat_id, message_id=game.message_id
            )

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_get_game_high_scores(self, bot, chat_id):
        # We need a game to get the scores for
        game_short_name = 'test_game'
        game = bot.send_game(chat_id, game_short_name)
        high_scores = bot.get_game_high_scores(chat_id, game.chat_id, game.message_id)
        # We assume that the other game score tests ran within 20 sec
        assert pytest.approx(high_scores[0].score, abs=20) == int(BASE_TIME) - HIGHSCORE_DELTA

    # send_invoice is tested in test_invoice

    # TODO: Needs improvement. Need incoming shippping queries to test
    def test_answer_shipping_query_ok(self, monkeypatch, bot):
        # For now just test that our internals pass the correct data
        def test(url, data, *args, **kwargs):
            return data == {
                'shipping_query_id': 1,
                'ok': True,
                'shipping_options': [
                    {'title': 'option1', 'prices': [{'label': 'price', 'amount': 100}], 'id': 1}
                ],
            }

        monkeypatch.setattr(bot.request, 'post', test)
        shipping_options = ShippingOption(1, 'option1', [LabeledPrice('price', 100)])
        assert bot.answer_shipping_query(1, True, shipping_options=[shipping_options])

    def test_answer_shipping_query_error_message(self, monkeypatch, bot):
        # For now just test that our internals pass the correct data
        def test(url, data, *args, **kwargs):
            return data == {
                'shipping_query_id': 1,
                'error_message': 'Not enough fish',
                'ok': False,
            }

        monkeypatch.setattr(bot.request, 'post', test)
        assert bot.answer_shipping_query(1, False, error_message='Not enough fish')

    def test_answer_shipping_query_errors(self, monkeypatch, bot):
        shipping_options = ShippingOption(1, 'option1', [LabeledPrice('price', 100)])

        with pytest.raises(TelegramError, match='should not be empty and there should not be'):
            bot.answer_shipping_query(1, True, error_message='Not enough fish')

        with pytest.raises(TelegramError, match='should not be empty and there should not be'):
            bot.answer_shipping_query(1, False)

        with pytest.raises(TelegramError, match='should not be empty and there should not be'):
            bot.answer_shipping_query(1, False, shipping_options=shipping_options)

        with pytest.raises(TelegramError, match='should not be empty and there should not be'):
            bot.answer_shipping_query(1, True)

    # TODO: Needs improvement. Need incoming pre checkout queries to test
    def test_answer_pre_checkout_query_ok(self, monkeypatch, bot):
        # For now just test that our internals pass the correct data
        def test(url, data, *args, **kwargs):
            return data == {'pre_checkout_query_id': 1, 'ok': True}

        monkeypatch.setattr(bot.request, 'post', test)
        assert bot.answer_pre_checkout_query(1, True)

    def test_answer_pre_checkout_query_error_message(self, monkeypatch, bot):
        # For now just test that our internals pass the correct data
        def test(url, data, *args, **kwargs):
            return data == {
                'pre_checkout_query_id': 1,
                'error_message': 'Not enough fish',
                'ok': False,
            }

        monkeypatch.setattr(bot.request, 'post', test)
        assert bot.answer_pre_checkout_query(1, False, error_message='Not enough fish')

    def test_answer_pre_checkout_query_errors(self, monkeypatch, bot):
        with pytest.raises(TelegramError, match='should not be'):
            bot.answer_pre_checkout_query(1, True, error_message='Not enough fish')

        with pytest.raises(TelegramError, match='should not be empty'):
            bot.answer_pre_checkout_query(1, False)

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_restrict_chat_member(self, bot, channel_id, chat_permissions):
        # TODO: Add bot to supergroup so this can be tested properly
        with pytest.raises(BadRequest, match='Method is available only for supergroups'):
            assert bot.restrict_chat_member(
                channel_id, 95205500, chat_permissions, until_date=dtm.datetime.utcnow()
            )

    def test_restrict_chat_member_default_tz(
        self, monkeypatch, tz_bot, channel_id, chat_permissions
    ):
        until = dtm.datetime(2020, 1, 11, 16, 13)
        until_timestamp = to_timestamp(until, tzinfo=tz_bot.defaults.tzinfo)

        def test(url, data, *args, **kwargs):
            return data.get('until_date', until_timestamp) == until_timestamp

        monkeypatch.setattr(tz_bot.request, 'post', test)

        assert tz_bot.restrict_chat_member(channel_id, 95205500, chat_permissions)
        assert tz_bot.restrict_chat_member(
            channel_id, 95205500, chat_permissions, until_date=until
        )
        assert tz_bot.restrict_chat_member(
            channel_id, 95205500, chat_permissions, until_date=until_timestamp
        )

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_promote_chat_member(self, bot, channel_id):
        # TODO: Add bot to supergroup so this can be tested properly / give bot perms
        with pytest.raises(BadRequest, match='Not enough rights'):
            assert bot.promote_chat_member(
                channel_id,
                95205500,
                is_anonymous=True,
                can_change_info=True,
                can_post_messages=True,
                can_edit_messages=True,
                can_delete_messages=True,
                can_invite_users=True,
                can_restrict_members=True,
                can_pin_messages=True,
                can_promote_members=True,
            )

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_export_chat_invite_link(self, bot, channel_id):
        # Each link is unique apparently
        invite_link = bot.export_chat_invite_link(channel_id)
        assert isinstance(invite_link, str)
        assert invite_link != ''

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_set_chat_photo(self, bot, channel_id):
        def func():
            assert bot.set_chat_photo(channel_id, f)

        with open('tests/data/telegram_test_channel.jpg', 'rb') as f:
            expect_bad_request(func, 'Type of file mismatch', 'Telegram did not accept the file.')

    def test_set_chat_photo_local_files(self, monkeypatch, bot, chat_id):
        # For just test that the correct paths are passed as we have no local bot API set up
        test_flag = False
        expected = (Path.cwd() / 'tests/data/telegram.jpg/').as_uri()
        file = 'tests/data/telegram.jpg'

        def make_assertion(_, data, *args, **kwargs):
            nonlocal test_flag
            test_flag = data.get('photo') == expected

        monkeypatch.setattr(bot, '_post', make_assertion)
        bot.set_chat_photo(chat_id, file)
        assert test_flag

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_delete_chat_photo(self, bot, channel_id):
        def func():
            assert bot.delete_chat_photo(channel_id)

        expect_bad_request(func, 'Chat_not_modified', 'Chat photo was not set.')

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_set_chat_title(self, bot, channel_id):
        assert bot.set_chat_title(channel_id, '>>> telegram.Bot() - Tests')

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_set_chat_description(self, bot, channel_id):
        assert bot.set_chat_description(channel_id, 'Time: ' + str(time.time()))

    # TODO: Add bot to group to test there too
    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_pin_and_unpin_message(self, bot, super_group_id):
        message1 = bot.send_message(super_group_id, text="test_pin_message_1")
        message2 = bot.send_message(super_group_id, text="test_pin_message_2")
        message3 = bot.send_message(super_group_id, text="test_pin_message_3")

        assert bot.pin_chat_message(
            chat_id=super_group_id, message_id=message1.message_id, disable_notification=True
        )

        bot.pin_chat_message(
            chat_id=super_group_id, message_id=message2.message_id, disable_notification=True
        )
        bot.pin_chat_message(
            chat_id=super_group_id, message_id=message3.message_id, disable_notification=True
        )

        chat = bot.get_chat(super_group_id)
        assert chat.pinned_message == message3

        assert bot.unpin_chat_message(super_group_id, message_id=message2.message_id)
        assert bot.unpin_chat_message(super_group_id)

        assert bot.unpin_all_chat_messages(super_group_id)

    # get_sticker_set, upload_sticker_file, create_new_sticker_set, add_sticker_to_set,
    # set_sticker_position_in_set and delete_sticker_from_set are tested in the
    # test_sticker module.

    def test_timeout_propagation_explicit(self, monkeypatch, bot, chat_id):

        from telegram.vendor.ptb_urllib3.urllib3.util.timeout import Timeout

        class OkException(Exception):
            pass

        TIMEOUT = 500

        def request_wrapper(*args, **kwargs):
            obj = kwargs.get('timeout')
            if isinstance(obj, Timeout) and obj._read == TIMEOUT:
                raise OkException

            return b'{"ok": true, "result": []}'

        monkeypatch.setattr('telegram.utils.request.Request._request_wrapper', request_wrapper)

        # Test file uploading
        with pytest.raises(OkException):
            bot.send_photo(chat_id, open('tests/data/telegram.jpg', 'rb'), timeout=TIMEOUT)

        # Test JSON submition
        with pytest.raises(OkException):
            bot.get_chat_administrators(chat_id, timeout=TIMEOUT)

    def test_timeout_propagation_implicit(self, monkeypatch, bot, chat_id):

        from telegram.vendor.ptb_urllib3.urllib3.util.timeout import Timeout

        class OkException(Exception):
            pass

        def request_wrapper(*args, **kwargs):
            obj = kwargs.get('timeout')
            if isinstance(obj, Timeout) and obj._read == 20:
                raise OkException

            return b'{"ok": true, "result": []}'

        monkeypatch.setattr('telegram.utils.request.Request._request_wrapper', request_wrapper)

        # Test file uploading
        with pytest.raises(OkException):
            bot.send_photo(chat_id, open('tests/data/telegram.jpg', 'rb'))

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_send_message_entities(self, bot, chat_id):
        test_string = 'Italic Bold Code'
        entities = [
            MessageEntity(MessageEntity.ITALIC, 0, 6),
            MessageEntity(MessageEntity.ITALIC, 7, 4),
            MessageEntity(MessageEntity.ITALIC, 12, 4),
        ]
        message = bot.send_message(chat_id=chat_id, text=test_string, entities=entities)
        assert message.text == test_string
        assert message.entities == entities

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    @pytest.mark.parametrize('default_bot', [{'parse_mode': 'Markdown'}], indirect=True)
    def test_send_message_default_parse_mode(self, default_bot, chat_id):
        test_string = 'Italic Bold Code'
        test_markdown_string = '_Italic_ *Bold* `Code`'

        message = default_bot.send_message(chat_id, test_markdown_string)
        assert message.text_markdown == test_markdown_string
        assert message.text == test_string

        message = default_bot.send_message(chat_id, test_markdown_string, parse_mode=None)
        assert message.text == test_markdown_string
        assert message.text_markdown == escape_markdown(test_markdown_string)

        message = default_bot.send_message(chat_id, test_markdown_string, parse_mode='HTML')
        assert message.text == test_markdown_string
        assert message.text_markdown == escape_markdown(test_markdown_string)

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
    def test_send_message_default_allow_sending_without_reply(self, default_bot, chat_id, custom):
        reply_to_message = default_bot.send_message(chat_id, 'test')
        reply_to_message.delete()
        if custom is not None:
            message = default_bot.send_message(
                chat_id,
                'test',
                allow_sending_without_reply=custom,
                reply_to_message_id=reply_to_message.message_id,
            )
            assert message.reply_to_message is None
        elif default_bot.defaults.allow_sending_without_reply:
            message = default_bot.send_message(
                chat_id, 'test', reply_to_message_id=reply_to_message.message_id
            )
            assert message.reply_to_message is None
        else:
            with pytest.raises(BadRequest, match='message not found'):
                default_bot.send_message(
                    chat_id, 'test', reply_to_message_id=reply_to_message.message_id
                )

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_set_and_get_my_commands(self, bot):
        commands = [
            BotCommand('cmd1', 'descr1'),
            BotCommand('cmd2', 'descr2'),
        ]
        bot.set_my_commands([])
        assert bot.get_my_commands() == []
        assert bot.commands == []
        assert bot.set_my_commands(commands)

        for bc in [bot.get_my_commands(), bot.commands]:
            assert len(bc) == 2
            assert bc[0].command == 'cmd1'
            assert bc[0].description == 'descr1'
            assert bc[1].command == 'cmd2'
            assert bc[1].description == 'descr2'

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_set_and_get_my_commands_strings(self, bot):
        commands = [
            ['cmd1', 'descr1'],
            ['cmd2', 'descr2'],
        ]
        bot.set_my_commands([])
        assert bot.get_my_commands() == []
        assert bot.commands == []
        assert bot.set_my_commands(commands)

        for bc in [bot.get_my_commands(), bot.commands]:
            assert len(bc) == 2
            assert bc[0].command == 'cmd1'
            assert bc[0].description == 'descr1'
            assert bc[1].command == 'cmd2'
            assert bc[1].description == 'descr2'

    def test_log_out(self, monkeypatch, bot):
        # We don't actually make a request as to not break the test setup
        def assertion(url, data, *args, **kwargs):
            return data == {} and url.split('/')[-1] == 'logOut'

        monkeypatch.setattr(bot.request, 'post', assertion)

        assert bot.log_out()

    def test_close(self, monkeypatch, bot):
        # We don't actually make a request as to not break the test setup
        def assertion(url, data, *args, **kwargs):
            return data == {} and url.split('/')[-1] == 'close'

        monkeypatch.setattr(bot.request, 'post', assertion)

        assert bot.close()

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    @pytest.mark.parametrize('json_keyboard', [True, False])
    def test_copy_message(self, monkeypatch, bot, chat_id, media_message, json_keyboard):
        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="test", callback_data="test2")]]
        )

        def post(url, data, timeout):
            assert data["chat_id"] == chat_id
            assert data["from_chat_id"] == chat_id
            assert data["message_id"] == media_message.message_id
            assert data["caption"] == "<b>Test</b>"
            assert data["parse_mode"] == ParseMode.HTML
            assert data["reply_to_message_id"] == media_message.message_id
            assert data["reply_markup"] == keyboard.to_json()
            assert data["disable_notification"] is True
            assert data["caption_entities"] == [MessageEntity(MessageEntity.BOLD, 0, 4)]
            return data

        monkeypatch.setattr(bot.request, 'post', post)
        bot.copy_message(
            chat_id,
            from_chat_id=chat_id,
            message_id=media_message.message_id,
            caption="<b>Test</b>",
            caption_entities=[MessageEntity(MessageEntity.BOLD, 0, 4)],
            parse_mode=ParseMode.HTML,
            reply_to_message_id=media_message.message_id,
            reply_markup=keyboard.to_json() if json_keyboard else keyboard,
            disable_notification=True,
        )

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    def test_copy_message_without_reply(self, bot, chat_id, media_message):
        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="test", callback_data="test2")]]
        )

        returned = bot.copy_message(
            chat_id,
            from_chat_id=chat_id,
            message_id=media_message.message_id,
            caption="<b>Test</b>",
            parse_mode=ParseMode.HTML,
            reply_to_message_id=media_message.message_id,
            reply_markup=keyboard,
        )
        # we send a temp message which replies to the returned message id in order to get a
        # message object
        temp_message = bot.send_message(chat_id, "test", reply_to_message_id=returned.message_id)
        message = temp_message.reply_to_message
        assert message.chat_id == int(chat_id)
        assert message.caption == "Test"
        assert len(message.caption_entities) == 1
        assert message.reply_markup == keyboard

    @flaky(3, 1)
    @pytest.mark.timeout(10)
    @pytest.mark.parametrize(
        'default_bot',
        [
            ({'parse_mode': ParseMode.HTML, 'allow_sending_without_reply': True}),
            ({'parse_mode': False, 'allow_sending_without_reply': True}),
            ({'parse_mode': False, 'allow_sending_without_reply': False}),
        ],
        indirect=['default_bot'],
    )
    def test_copy_message_with_default(self, default_bot, chat_id, media_message):
        reply_to_message = default_bot.send_message(chat_id, 'test')
        reply_to_message.delete()
        if not default_bot.defaults.allow_sending_without_reply:
            with pytest.raises(BadRequest, match='Reply message not found'):
                default_bot.copy_message(
                    chat_id,
                    from_chat_id=chat_id,
                    message_id=media_message.message_id,
                    caption="<b>Test</b>",
                    reply_to_message_id=reply_to_message.message_id,
                )
            return
        else:
            returned = default_bot.copy_message(
                chat_id,
                from_chat_id=chat_id,
                message_id=media_message.message_id,
                caption="<b>Test</b>",
                reply_to_message_id=reply_to_message.message_id,
            )
        # we send a temp message which replies to the returned message id in order to get a
        # message object
        temp_message = default_bot.send_message(
            chat_id, "test", reply_to_message_id=returned.message_id
        )
        message = temp_message.reply_to_message
        if default_bot.defaults.parse_mode:
            assert len(message.caption_entities) == 1
        else:
            assert len(message.caption_entities) == 0
