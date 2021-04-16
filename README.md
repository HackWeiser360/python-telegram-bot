# Python-Telegram-Bot
[Bot](Python-Telegram-Bot.png)

<p align="center">
  <img src="https://img.shields.io/badge/Version-1.0-green?style=for-the-badge">
  <img src="https://img.shields.io/github/license/HackWeiser360/python-telegram-bot?style=for-the-badge">
  <img src="https://img.shields.io/github/stars/HackWeiser360/python-telegram-bot?style=for-the-badge">
  <img src="https://img.shields.io/github/issues/HackWeiser360/python-telegram-bot?color=red&style=for-the-badge">
  <img src="https://img.shields.io/github/forks/HackWeiser360/python-telegram-bot?color=teal&style=for-the-badge">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Author-HackWeiser360-cyan?style=flat-square">
  <img src="https://img.shields.io/badge/Open%20Source-Yes-cyan?style=flat-square">
  <img src="https://img.shields.io/badge/MADE%20IN-Kenya✌-green?colorA=%23ff0000&colorB=%23017e40&style=flat-square">
  <img src="https://img.shields.io/badge/Written%20In-Python-cyan?style=flat-square">
</p>

Python-Telegram-Bot is a bot made from python obviously as the name suggests. The bot can be used in Telegram groups. The bot comes with new and added features from the normal Telegram bots. Let's get started.

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

Visit `this page <https://github.com/HackWeiser360/python-telegram-bot/blob/master/examples/README.md>`_ to discover the official examples or look at the examples on the `wiki <https://github.com/HackWeiser360/python-telegram-bot/wiki/Examples>`_ to see other bots the community has built. The Wiki is under construction and should be ready in 2-3 weeks.

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
<div align="center">
<a href="https://github.com/HackWeiser360" target="_blank">
<img src=https://img.shields.io/badge/github-%2324292e.svg?&style=for-the-badge&logo=github&logoColor=white alt=github style="margin-bottom: 5px;" />
</a>
<a href="https://twitter.com/503_madmax" target="_blank">
<img src=https://img.shields.io/badge/twitter-%2300acee.svg?&style=for-the-badge&logo=twitter&logoColor=white alt=twitter style="margin-bottom: 5px;" />
</a>
<a href="https://www.instagram.com/madmax4708/" target="_blank">
<img src=https://img.shields.io/badge/instagram-%23000000.svg?&style=for-the-badge&logo=instagram&logoColor=white alt=instagram style="margin-bottom: 5px;" />
### Stargazers
[![Stargazers repo roster for @HackWeiser360/python-telegram-bot](https://reporoster.com/stars/HackWeiser360/python-telegram-bot)](https://github.com/HackWeiser360/python-telegram-bot)
