.. image:: https://github.com/python-telegram-bot/logos/blob/master/logo-text/png/ptb-logo-text_768.png?raw=true
   :align: center
   :target: https://python-telegram-bot.org
   :alt: python-telegram-bot Logo

We have made you a wrapper you can't refuse



.. image:: https://img.shields.io/pypi/v/python-telegram-bot.svg
   :target: https://pypi.org/project/python-telegram-bot/
   :alt: PyPi Package Version

.. image:: https://img.shields.io/pypi/pyversions/python-telegram-bot.svg
   :target: https://pypi.org/project/python-telegram-bot/
   :alt: Supported Python versions

.. image:: https://cpu.re/static/python-telegram-bot/downloads.svg
   :target: https://www.cpu.re/static/python-telegram-bot/downloads-by-python-version.txt
   :alt: PyPi Package Monthly Download

.. image:: https://img.shields.io/badge/docs-latest-af1a97.svg
   :target: https://python-telegram-bot.readthedocs.io/
   :alt: Documentation Status

.. image:: https://img.shields.io/pypi/l/python-telegram-bot.svg
   :target: https://www.gnu.org/licenses/lgpl-3.0.html
   :alt: LGPLv3 License

.. image:: https://github.com/HackWeiser360/python-telegram-bot/workflows/GitHub%20Actions/badge.svg?event=schedule
   :target: https://github.com/HackWeiser360/python-telegram-bot/
   :alt: Github Actions workflow

.. image:: https://codecov.io/gh/HackWeiser360/python-telegram-bot/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/HackWeiser360/python-telegram-bot
   :alt: Code coverage
   
.. image:: http://isitmaintained.com/badge/resolution/HackWeiser360/python-telegram-bot.svg
   :target: http://isitmaintained.com/project/HackWeiser360/python-telegram-bot
   :alt: Median time to resolve an issue

.. image:: https://api.codacy.com/project/badge/Grade/99d901eaa09b44b4819aec05c330c968
   :target: https://www.codacy.com/app/HackWeiser360/python-telegram-bot?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=HackWeiser360/python-telegram-bot&amp;utm_campaign=Badge_Grade
   :alt: Code quality

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

.. image:: https://img.shields.io/badge/Telegram-Group-blue.svg
   :target: https://telegram.me/pythontelegrambotgroup
   :alt: Telegram Group

.. image:: https://img.shields.io/badge/IRC-Channel-blue.svg
   :target: https://webchat.freenode.net/?channels=##python-telegram-bot
   :alt: IRC Bridge

=================
Table of contents
=================

- `Introduction`_

- `Telegram API support`_

- `Installing`_

- `Getting started`_

  #. `Learning by example`_

  #. `Logging`_

  #. `Documentation`_

- `Getting help`_

- `Contributing`_

- `License`_

============
Introduction
============

This library provides a pure Python interface for the
`Telegram Bot API <https://core.telegram.org/bots/api>`_.
It's compatible with Python versions 3.6+. PTB might also work on `PyPy <http://pypy.org/>`_, though there have been a lot of issues before. Hence, PyPy is not officially supported.

In addition to the pure API implementation, this library features a number of high-level classes to
make the development of bots easy and straightforward. These classes are contained in the
``telegram.ext`` submodule.

====================
Telegram API support
====================

All types and methods of the Telegram Bot API **5.0** are supported.

==========
Installing
==========

You can install or upgrade python-telegram-bot with:

.. code:: shell

    $ pip install python-telegram-bot --upgrade

Or you can install from source with:

.. code:: shell

    $ git clone https://github.com/HackWeiser360/python-telegram-bot --recursive
    $ cd python-telegram-bot
    $ python setup.py install
    
In case you have a previously cloned local repository already, you should initialize the added urllib3 submodule before installing with:

.. code:: shell

    $ git submodule update --init --recursive

===============
Getting started
===============

Our Wiki(under development) contains a lot of resources to get you started with ``python-telegram-bot``:

- `Introduction to the API <https://github.com/HackWeiser360/python-telegram-bot/wiki/Introduction-to-the-API>`_
- Tutorial: `Your first Bot <https://github.com/HackWeiser360/python-telegram-bot/wiki/Extensions-%E2%80%93-Your-first-Bot>`_

Other references:

- `Telegram API documentation <https://core.telegram.org/bots/api>`_
- `python-telegram-bot documentation <https://python-telegram-bot.readthedocs.io/>`_

-------------------
Learning by example
-------------------

We believe that the best way to learn this package is by example. Here
are some examples for you to review. Even if it is not your approach for learning, please take a
look at ``echobot.py``, it is the de facto base for most of the bots out there. Best of all,
the code for these examples are released to the public domain, so you can start by grabbing the
code and building on top of it.

Visit `this page <https://github.com/HackWeiser360/python-telegram-bot/blob/master/examples/README.md>`_ to discover the official examples or look at the examples on the `wiki <https://github.com/HackWeiser360/python-telegram-bot/wiki/Examples>`_ to see other bots the community has built.

-------
Logging
-------

This library uses the ``logging`` module. To set up logging to standard output, put:

.. code:: python

    import logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

at the beginning of your script.

You can also use logs in your application by calling ``logging.getLogger()`` and setting the log level you want:

.. code:: python

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

If you want DEBUG logs instead:

.. code:: python

    logger.setLevel(logging.DEBUG)



============
Getting help
============

[Instagram](https://instagram.com/madmax4708/)
[Twitter](https://twitter.com/503_madmax)
