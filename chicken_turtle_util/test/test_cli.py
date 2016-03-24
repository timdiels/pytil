# Copyright (C) 2016 VIB/BEG/UGent - Tim Diels <timdiels.m@gmail.com>
# 
# This file is part of Chicken Turtle Util.
# 
# Chicken Turtle Util is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Chicken Turtle Util is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with Chicken Turtle Util.  If not, see <http://www.gnu.org/licenses/>.

'''
Test chicken_turtle_util.algorithms
'''

import pytest
from chicken_turtle_util import cli, iterable
from click.testing import CliRunner

def test_cli(mocker):
    '''
    Check all cli for trivial bugs
    
    The implementation itself doesn't leave much room for complex bugs
    '''

    db_args = dict(
        database_host='db_host',
        database_user='db_user',
        database_password='db_password',
        database_name='db_name'
    )
    
    Database = mocker.Mock(return_value='database')
    
    class MyAppContext(cli.DatabaseMixin(Database), cli.Context):
        pass
        
    @cli.command()
    @cli.option('--option', default=555)
    @cli.argument('argument')
    @cli.password_option('--password')
    @MyAppContext.cli_options()
    def main(option, argument, password, **kwargs):
        assert option == 5
        assert password == 'pass'
        assert argument == 'arg'
        
        context = MyAppContext(**kwargs)
        Database.assert_called_once_with(context=context, host='db_host', user='db_user', password='db_password', name='db_name')
        assert context.database == 'database'
    
    # Assert our option, argument, password_option overrides
    params = {x.opts[0]: x for x in main.params}
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
    
    # Assert -h, --help exist
    result = CliRunner().invoke(main, ['--help'])
    assert not result.exception
    assert '-h, --help' in result.output
    
    # Assert context works
    args = [
        '--option', '5', '--password', 'pass', 'arg',
        '--database-host', 'db_host', '--database-user', 'db_user',
        '--database-password', 'db_password', '--database-name', 'db_name'
    ]
    result = CliRunner().invoke(main, args, catch_exceptions=False)
    assert not result.exception, result.output
    