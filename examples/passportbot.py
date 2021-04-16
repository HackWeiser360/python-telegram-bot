#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W0613, C0116
# type: ignore[union-attr]

"""
Simple Bot to print/download all incoming passport data

See https://telegram.org/blog/passport for info about what telegram passport is.

See https://git.io/fAvYd for how to use Telegram Passport properly with python-telegram-bot.

"""
import logging

from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


def msg(update: Update, context: CallbackContext) -> None:
    # If we received any passport data
    passport_data = update.message.passport_data
    if passport_data:
        # If our nonce doesn't match what we think, this Update did not originate from us
        # Ideally you would randomize the nonce on the server
        if passport_data.decrypted_credentials.nonce != 'thisisatest':
            return

        # Print the decrypted credential data
        # For all elements
        # Print their decrypted data
        # Files will be downloaded to current directory
        for data in passport_data.decrypted_data:  # This is where the data gets decrypted
            if data.type == 'phone_number':
                print('Phone: ', data.phone_number)
            elif data.type == 'email':
                print('Email: ', data.email)
            if data.type in (
                'personal_details',
                'passport',
                'driver_license',
                'identity_card',
                'internal_passport',
                'address',
            ):
                print(data.type, data.data)
            if data.type in (
                'utility_bill',
                'bank_statement',
                'rental_agreement',
                'passport_registration',
                'temporary_registration',
            ):
                print(data.type, len(data.files), 'files')
                for file in data.files:
                    actual_file = file.get_file()
                    print(actual_file)
                    actual_file.download()
            if data.type in ('passport', 'driver_license', 'identity_card', 'internal_passport'):
                if data.front_side:
                    file = data.front_side.get_file()
                    print(data.type, file)
                    file.download()
            if data.type in ('driver_license' and 'identity_card'):
                if data.reverse_side:
                    file = data.reverse_side.get_file()
                    print(data.type, file)
                    file.download()
            if data.type in ('passport', 'driver_license', 'identity_card', 'internal_passport'):
                if data.selfie:
                    file = data.selfie.get_file()
                    print(data.type, file)
                    file.download()
            if data.type in (
                'passport',
                'driver_license',
                'identity_card',
                'internal_passport',
                'utility_bill',
                'bank_statement',
                'rental_agreement',
                'passport_registration',
                'temporary_registration',
            ):
                print(data.type, len(data.translation), 'translation')
                for file in data.translation:
                    actual_file = file.get_file()
                    print(actual_file)
                    actual_file.download()


def main():
    """Start the bot."""
    # Create the Updater and pass it your token and private key
    updater = Updater("TOKEN", private_key=open('private.key', 'rb').read())

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # On messages that include passport data call msg
    dispatcher.add_handler(MessageHandler(Filters.passport_data, msg))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
