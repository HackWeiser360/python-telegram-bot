#!/usr/bin/env python


import pytest

from telegram import (
    InlineKeyboardMarkup,
    InlineQueryResultAudio,
    InlineQueryResultArticle,
    InlineKeyboardButton,
    InputTextMessageContent,
)


@pytest.fixture(scope='class')
def inline_query_result_article():
    return InlineQueryResultArticle(
        TestInlineQueryResultArticle.id_,
        TestInlineQueryResultArticle.title,
        input_message_content=TestInlineQueryResultArticle.input_message_content,
        reply_markup=TestInlineQueryResultArticle.reply_markup,
        url=TestInlineQueryResultArticle.url,
        hide_url=TestInlineQueryResultArticle.hide_url,
        description=TestInlineQueryResultArticle.description,
        thumb_url=TestInlineQueryResultArticle.thumb_url,
        thumb_height=TestInlineQueryResultArticle.thumb_height,
        thumb_width=TestInlineQueryResultArticle.thumb_width,
    )


class TestInlineQueryResultArticle:
    id_ = 'id'
    type_ = 'article'
    title = 'title'
    input_message_content = InputTextMessageContent('input_message_content')
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('reply_markup')]])
    url = 'url'
    hide_url = True
    description = 'description'
    thumb_url = 'thumb url'
    thumb_height = 10
    thumb_width = 15

    def test_expected_values(self, inline_query_result_article):
        assert inline_query_result_article.type == self.type_
        assert inline_query_result_article.id == self.id_
        assert inline_query_result_article.title == self.title
        assert (
            inline_query_result_article.input_message_content.to_dict()
            == self.input_message_content.to_dict()
        )
        assert inline_query_result_article.reply_markup.to_dict() == self.reply_markup.to_dict()
        assert inline_query_result_article.url == self.url
        assert inline_query_result_article.hide_url == self.hide_url
        assert inline_query_result_article.description == self.description
        assert inline_query_result_article.thumb_url == self.thumb_url
        assert inline_query_result_article.thumb_height == self.thumb_height
        assert inline_query_result_article.thumb_width == self.thumb_width

    def test_to_dict(self, inline_query_result_article):
        inline_query_result_article_dict = inline_query_result_article.to_dict()

        assert isinstance(inline_query_result_article_dict, dict)
        assert inline_query_result_article_dict['type'] == inline_query_result_article.type
        assert inline_query_result_article_dict['id'] == inline_query_result_article.id
        assert inline_query_result_article_dict['title'] == inline_query_result_article.title
        assert (
            inline_query_result_article_dict['input_message_content']
            == inline_query_result_article.input_message_content.to_dict()
        )
        assert (
            inline_query_result_article_dict['reply_markup']
            == inline_query_result_article.reply_markup.to_dict()
        )
        assert inline_query_result_article_dict['url'] == inline_query_result_article.url
        assert inline_query_result_article_dict['hide_url'] == inline_query_result_article.hide_url
        assert (
            inline_query_result_article_dict['description']
            == inline_query_result_article.description
        )
        assert (
            inline_query_result_article_dict['thumb_url'] == inline_query_result_article.thumb_url
        )
        assert (
            inline_query_result_article_dict['thumb_height']
            == inline_query_result_article.thumb_height
        )
        assert (
            inline_query_result_article_dict['thumb_width']
            == inline_query_result_article.thumb_width
        )

    def test_equality(self):
        a = InlineQueryResultArticle(self.id_, self.title, self.input_message_content)
        b = InlineQueryResultArticle(self.id_, self.title, self.input_message_content)
        c = InlineQueryResultArticle(self.id_, '', self.input_message_content)
        d = InlineQueryResultArticle('', self.title, self.input_message_content)
        e = InlineQueryResultAudio(self.id_, '', '')

        assert a == b
        assert hash(a) == hash(b)
        assert a is not b

        assert a == c
        assert hash(a) == hash(c)

        assert a != d
        assert hash(a) != hash(d)

        assert a != e
        assert hash(a) != hash(e)
