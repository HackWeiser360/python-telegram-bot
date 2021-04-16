#!/usr/bin/env python

import _pytest.config
import pytest

fold_plugins = {'_cov': 'Coverage report', 'flaky': 'Flaky report'}


def terminal_summary_wrapper(original, plugin_name):
    text = fold_plugins[plugin_name]

    def pytest_terminal_summary(terminalreporter):
        terminalreporter.write(f'##[group] {text}\n')
        original(terminalreporter)
        terminalreporter.write('##[endgroup]')

    return pytest_terminal_summary


@pytest.mark.trylast
def pytest_configure(config):
    for hookimpl in config.pluginmanager.hook.pytest_terminal_summary._nonwrappers:
        if hookimpl.plugin_name in fold_plugins.keys():
            hookimpl.function = terminal_summary_wrapper(hookimpl.function, hookimpl.plugin_name)


terminal = None
previous_name = None


def _get_name(location):
    if location[0].startswith('tests/'):
        return location[0][6:]
    return location[0]


@pytest.mark.trylast
def pytest_itemcollected(item):
    item._nodeid = item._nodeid.split('::', 1)[1]


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_protocol(item, nextitem):
    # This is naughty but pytests' own plugins does something similar too, so who cares
    global terminal
    if terminal is None:
        terminal = _pytest.config.create_terminal_writer(item.config)

    global previous_name

    name = _get_name(item.location)

    if previous_name is None or previous_name != name:
        previous_name = name
        terminal.write(f'\n##[group] {name}')

    yield

    if nextitem is None or _get_name(nextitem.location) != name:
        terminal.write('\n##[endgroup]')
