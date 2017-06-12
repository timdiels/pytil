# Copyright (C) 2016 VIB/BEG/UGent - Tim Diels <timdiels.m@gmail.com>
#
# This file is part of pytil.
#
# pytil is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pytil is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with pytil.  If not, see <http://www.gnu.org/licenses/>.

'''
Test pytil.cli
'''

from pytil import click as click_
from click.testing import CliRunner
import click
import sys
import pytest

def test_options():
    '''
    Test our options and arguments
    '''
    @click.command()
    @click_.option('--option', default=555)
    @click_.argument('argument')
    @click_.password_option('--password')
    def main(option, argument, password):
        assert option == 5
        assert password == 'pass'
        assert argument == 'arg'

    params = {x.opts[0]: x for x in main.params}
    print(main)
    print(main.params)
    assert '--option' in params
    assert params['--option'].show_default
    assert params['--option'].required
    assert 'argument' in params
    assert params['argument'].required
    assert '--password' in params
    assert params['--password'].prompt
    assert params['--password'].hide_input
    assert not params['--password'].show_default
    assert params['--password'].required

    result = CliRunner().invoke(main, ['--option', '5', '--password', 'pass', 'arg'])
    assert not result.exception, result.output

def test_assert_runs():
    '''
    Test args are passed and when exit non-zero, raise
    '''
    @click.command()
    @click.option('--arg')
    def main(arg):
        if arg == 'fail':
            sys.exit(1)
    click_.assert_runs(main, ['--arg', 'nofail'])
    with pytest.raises(AssertionError):
        click_.assert_runs(main, ['--arg', 'fail'])
