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
Test chicken_turtle_util.cli
'''

from chicken_turtle_util import cli
from click.testing import CliRunner
import click
from pathlib import Path
import pytest
from textwrap import dedent

class TestNoContext(object):
    
    '''Tests without Context'''
    
    def test_options(self):
        '''
        Test our options and arguments
        '''
        @click.command()
        @cli.option('--option', default=555)
        @cli.argument('argument')
        @cli.password_option('--password')
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
    
class TestContext(object):
    
    '''Test basic workings of Context'''
    
    def test_context_argument(self):
        '''
        When using Context, `context` kwarg is supplied
        
        This also tests that other options and arguments are left unharmed
        '''
        @cli.Context.command()
        @cli.option('--option')
        @cli.argument('argument')
        def main(option, argument, context):
            assert option == '5'
            assert argument == 'arg'
            assert context
        
        params = {x.opts[0]: x for x in main.params}
        assert '--option' in params
        assert 'argument' in params
        
        result = CliRunner().invoke(main, ['--option', '5', 'arg'])
        assert not result.exception, result.output 

class TestMixins(object):
    
    '''Test context mixins separately'''
                
    def test_basics(self):
        '''Test BasicsMixin'''
        
        version = '1.0.0'
        
        class MyAppContext(cli.BasicsMixin(version), cli.Context):
            pass
        
        @MyAppContext.command()
        def main(context):
            pass
        
        params = {x.opts[0]: x for x in main.params}
        
        # Version option present
        assert '--version' in params
        result = CliRunner().invoke(main, ['--version'])
        assert not result.exception
        assert version in result.output
        
        # -h, --help option present
        result = CliRunner().invoke(main, ['--help'])
        assert not result.exception
        assert '-h, --help' in result.output, result.output
        
        # Runs
        result = CliRunner().invoke(main, [])
        assert not result.exception, result.output
        
    def test_database(self, mocker):
        '''Test DatabaseMixin'''
        Database = mocker.Mock(return_value='database')
        
        class MyAppContext(cli.DatabaseMixin(Database), cli.Context):
            pass
            
        @MyAppContext.command()
        def main(context):
            Database.assert_called_once_with(context=context, host='db_host', user='db_user', password='db_password', name='db_name')
            assert context.database == 'database'
        
        # Runs and provides database
        args = [
            '--database-host', 'db_host', '--database-user', 'db_user',
            '--database-password', 'db_password', '--database-name', 'db_name'
        ]
        result = CliRunner().invoke(main, args)
        assert not result.exception, result.output
        
    def test_configuration(self, mocker, tmpdir):
        help_message = 'Epic help message'
        create_configuration = mocker.Mock()
        tmpdir = Path(str(tmpdir))
        config_path = tmpdir / 'mah.conf'
        
        class MyAppContext(cli.ConfigurationMixin(create_configuration, help_message), cli.Context):
            pass
        
        @MyAppContext.command()
        def main(context):
            create_configuration.assert_called_once_with(context, config_path)
            assert context.configuration == 'configuration'
        
        # When missing file, raise
        result = CliRunner().invoke(main, ['--configuration', str(tmpdir / 'missing.conf')])
        assert result.exception
        assert 'missing.conf' in result.output
        assert 'does not exist' in result.output
        
        # When raise, print exception message
        create_configuration.side_effect = Exception(str(tmpdir / 'main.conf') + ' does not exist')
        result = CliRunner().invoke(main, ['--configuration', str(tmpdir)])
        assert result.exception
        assert 'main.conf does not exist' in result.output
        create_configuration.side_effect = None
        create_configuration.reset_mock()
        
        # When file present, all is well
        config_path.touch()
        create_configuration.return_value = 'configuration'
        result = CliRunner().invoke(main, ['--configuration', str(config_path)], catch_exceptions=False)
        assert not result.exception, result.output
        
        # Given help message must be part of command help message
        result = CliRunner().invoke(main, ['--help'])
        assert help_message in result.output
        
    def test_configurations(self, mocker, tmpdir):
        help_messages = {
            'main': 'Epic main help message', 
            'test': 'Epic test help message'
        }
        help_message = '''\
        Configuration files
        -------------------
        main
            Epic main help message
        test
            Epic test help message
        '''.rstrip().replace(' '*8, ' '*2)
        print(help_message)
        tmpdir = Path(str(tmpdir))
        config_path = tmpdir / 'mah.conf'
        
        class MyAppContext(cli.ConfigurationsMixin(help_messages), cli.Context):
            pass
        
        context_ = [None]
        @MyAppContext.command()
        def main(context):
            context_[0] = context
        
        # When missing file, raise
        result = CliRunner().invoke(main, ['--configuration', 'main', str(tmpdir / 'missing.conf')])
        assert result.exception
        assert 'missing.conf' in result.output
        assert 'does not exist' in result.output
        
        # When file present, all is well
        config_path.touch()
        result = CliRunner().invoke(main, ['--configuration', 'main', str(config_path)])
        assert not result.exception, result.output
        assert context_[0]._configuration_paths == {'main': config_path}
        
        # Multiple config args
        result = CliRunner().invoke(main, ['--configuration', 'main', str(config_path), '--configuration', 'test', str(config_path)])
        assert not result.exception, result.output
        assert context_[0]._configuration_paths == {'main': config_path, 'test': config_path}
        
        # When unknown configuration name, raise
        config_path.touch()
        result = CliRunner().invoke(main, ['--configuration', 'other', str(config_path)])
        assert result.exception
        assert 'other' in result.output
        assert 'Invalid value for "--configuration"' in result.output
        
        # Given help message must be part of command help message
        result = CliRunner().invoke(main, ['--help'])
        print(result.output)
        assert help_message in result.output
    
    class TestOutputDirectory(object):
        
        @pytest.fixture
        def output_dir(self):
            return Path('my_output_dir')
            
        @pytest.fixture
        def main(self, output_dir):
            class MyAppContext(cli.OutputDirectoryMixin, cli.Context):
                pass
                
            @MyAppContext.command()
            def main(context):
                assert context.output_directory.absolute() == output_dir.absolute()
                
            return main
        
        def test_missing_dir(self, temp_dir_cwd, main, output_dir):
            '''When dir is missing, error'''
            result = CliRunner().invoke(main, ['--output-directory', str(output_dir)])
            assert result.exception
            assert 'not exist' in result.output
            
        def test_not_writable_dir(self, temp_dir_cwd, main, output_dir):
            '''When dir is not writable, error'''
            output_dir = Path('my_output_dir')
            output_dir.mkdir(mode=0o555) # anything but write rights
            
            result = CliRunner().invoke(main, ['--output-directory', str(output_dir)])
            assert result.exception, result.output
            assert 'not writable' in result.output
        
        def test_happy_days(self, temp_dir_cwd, main, output_dir):
            '''When dir exists and is writable, Context.output_directory has its path'''
            output_dir = Path('my_output_dir')
            output_dir.mkdir()
            
            result = CliRunner().invoke(main, ['--output-directory', str(output_dir)])
            print(result.exception)
            assert not result.exception, result.output
    
    def test_data_directory(self, temp_dir_cwd, mocker):
        mocker.patch('xdg.BaseDirectory.xdg_data_home', str(Path.cwd().absolute()))
        
        class MyAppContext(cli.DataDirectoryMixin('my_app'), cli.Context):
            pass
                
        @MyAppContext.command()
        def main(context):
            assert context.data_directory.absolute() == Path('my_app').absolute()
            return main
        
        result = CliRunner().invoke(main)
        assert not result.exception
        
    def test_cache_directory(self, temp_dir_cwd, mocker):
        mocker.patch('xdg.BaseDirectory.xdg_cache_home', str(Path.cwd().absolute()))
        
        class MyAppContext(cli.CacheDirectoryMixin('my_app'), cli.Context):
            pass
                
        @MyAppContext.command()
        def main(context):
            assert context.cache_directory.absolute() == Path('my_app').absolute()
            return main
        
        result = CliRunner().invoke(main)
        assert not result.exception
