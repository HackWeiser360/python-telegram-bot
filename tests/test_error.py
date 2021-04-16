#!/usr/bin/env python

import pickle
from collections import defaultdict

import pytest

from telegram import TelegramError, TelegramDecryptionError
from telegram.error import (
    Unauthorized,
    InvalidToken,
    NetworkError,
    BadRequest,
    TimedOut,
    ChatMigrated,
    RetryAfter,
    Conflict,
)


class TestErrors:
    def test_telegram_error(self):
        with pytest.raises(TelegramError, match="^test message$"):
            raise TelegramError("test message")
        with pytest.raises(TelegramError, match="^Test message$"):
            raise TelegramError("Error: test message")
        with pytest.raises(TelegramError, match="^Test message$"):
            raise TelegramError("[Error]: test message")
        with pytest.raises(TelegramError, match="^Test message$"):
            raise TelegramError("Bad Request: test message")

    def test_unauthorized(self):
        with pytest.raises(Unauthorized, match="test message"):
            raise Unauthorized("test message")
        with pytest.raises(Unauthorized, match="^Test message$"):
            raise Unauthorized("Error: test message")
        with pytest.raises(Unauthorized, match="^Test message$"):
            raise Unauthorized("[Error]: test message")
        with pytest.raises(Unauthorized, match="^Test message$"):
            raise Unauthorized("Bad Request: test message")

    def test_invalid_token(self):
        with pytest.raises(InvalidToken, match="Invalid token"):
            raise InvalidToken

    def test_network_error(self):
        with pytest.raises(NetworkError, match="test message"):
            raise NetworkError("test message")
        with pytest.raises(NetworkError, match="^Test message$"):
            raise NetworkError("Error: test message")
        with pytest.raises(NetworkError, match="^Test message$"):
            raise NetworkError("[Error]: test message")
        with pytest.raises(NetworkError, match="^Test message$"):
            raise NetworkError("Bad Request: test message")

    def test_bad_request(self):
        with pytest.raises(BadRequest, match="test message"):
            raise BadRequest("test message")
        with pytest.raises(BadRequest, match="^Test message$"):
            raise BadRequest("Error: test message")
        with pytest.raises(BadRequest, match="^Test message$"):
            raise BadRequest("[Error]: test message")
        with pytest.raises(BadRequest, match="^Test message$"):
            raise BadRequest("Bad Request: test message")

    def test_timed_out(self):
        with pytest.raises(TimedOut, match="^Timed out$"):
            raise TimedOut

    def test_chat_migrated(self):
        with pytest.raises(ChatMigrated, match="Group migrated to supergroup. New chat id: 1234"):
            raise ChatMigrated(1234)
        try:
            raise ChatMigrated(1234)
        except ChatMigrated as e:
            assert e.new_chat_id == 1234

    def test_retry_after(self):
        with pytest.raises(RetryAfter, match="Flood control exceeded. Retry in 12.0 seconds"):
            raise RetryAfter(12)

    def test_conflict(self):
        with pytest.raises(Conflict, match='Something something.'):
            raise Conflict('Something something.')

    @pytest.mark.parametrize(
        "exception, attributes",
        [
            (TelegramError("test message"), ["message"]),
            (Unauthorized("test message"), ["message"]),
            (InvalidToken(), ["message"]),
            (NetworkError("test message"), ["message"]),
            (BadRequest("test message"), ["message"]),
            (TimedOut(), ["message"]),
            (ChatMigrated(1234), ["message", "new_chat_id"]),
            (RetryAfter(12), ["message", "retry_after"]),
            (Conflict("test message"), ["message"]),
            (TelegramDecryptionError("test message"), ["message"]),
        ],
    )
    def test_errors_pickling(self, exception, attributes):
        print(exception)
        pickled = pickle.dumps(exception)
        unpickled = pickle.loads(pickled)
        assert type(unpickled) is type(exception)
        assert str(unpickled) == str(exception)

        for attribute in attributes:
            assert getattr(unpickled, attribute) == getattr(exception, attribute)

    def test_pickling_test_coverage(self):
        """
        This test is only here to make sure that new errors will override __reduce__ properly.
        Add the new error class to the below covered_subclasses dict, if it's covered in the above
        test_errors_pickling test.
        """

        def make_assertion(cls):
            assert {sc for sc in cls.__subclasses__()} == covered_subclasses[cls]
            for subcls in cls.__subclasses__():
                make_assertion(subcls)

        covered_subclasses = defaultdict(set)
        covered_subclasses.update(
            {
                TelegramError: {
                    Unauthorized,
                    InvalidToken,
                    NetworkError,
                    ChatMigrated,
                    RetryAfter,
                    Conflict,
                    TelegramDecryptionError,
                },
                NetworkError: {BadRequest, TimedOut},
            }
        )

        make_assertion(TelegramError)
