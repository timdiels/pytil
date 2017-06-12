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
Test pytil.configuration
'''

from xdg.BaseDirectory import xdg_config_dirs
from pytil.configuration import ConfigurationLoader
from pathlib import Path
from pytil import path as path_
import pytest
from textwrap import dedent

class TestConfigurationLoader(object):

    @pytest.yield_fixture(autouse=True)
    def use_temp_dir(self, temp_dir_cwd):
        original = path_._root
        path_._root = Path.cwd()
        yield
        path_._root = original

    @pytest.fixture()
    def directory_name(self):
        return 'my_app'

    @pytest.fixture()
    def configuration_stem(self):
        return 'main' 

    @pytest.fixture()
    def loader(self, directory_name, configuration_stem):
        return ConfigurationLoader(Path(__name__).stem, directory_name, configuration_stem)

    def test_inheritance(self, directory_name):
        '''
        Test config file inheritance and use of defaults
        '''
        configuration_stem = 'inheritance'

        # First defaults should be read
        # from: data/main.defaults.conf given we used __name__.parent as package_name

        # Then /etc/{directory_name}/{configuration_name}.conf should override the defaults 
        path_.write(Path('etc/{}/{}.conf'.format(directory_name, configuration_stem)), contents=dedent('''\
        [section]
        a=10
        b=20
        c=30
        e=50
        space-word = f2
        '''))

        # Then each xdg conf file should override the previous (testing with just 1 file here)
        xdg_conf_dir = Path('home/mittens/much_conf_dir')
        xdg_conf_file = xdg_conf_dir / directory_name / (configuration_stem + '.conf')
        path_.write(xdg_conf_file, contents=dedent('''\
        [section]
        a=100
        b=200
        f=600
        space_word = expected
        '''))

        # Finally the path arg should override the previous
        path = Path('local.conf')
        path_.write(path, contents='''\
        [section]
        a=1000
        g=7000
        ''')

        # Test
        original = xdg_config_dirs[:]
        try:
            xdg_config_dirs[:] = ['/' + str(xdg_conf_dir)]
            configuration = self.loader(directory_name, configuration_stem).load(path)
        finally:
            xdg_config_dirs[:] = original

        # Assert
        assert configuration['section'] == dict(a='1000', b='200', c='30', d='4', e='50', f='600', g='7000', space_word='expected')

    def test_parsing(self, loader):
        '''
        Test config parsing rules

        - Configuration values are treated as strings.
        - Empty strings are allowed.
        - Inline comments can be started with '#' and ';'.
        - The 'default' section provides defaults for other sections.
        - ExtendedInterpolation is used (https://docs.python.org/3/library/configparser.html#configparser.ExtendedInterpolation).
        - Option names have '-' and ' ' replaced with '_'.
        '''
        path = Path('conf')
        path_.write(path, contents=dedent('''\
        [default]
        a=1
        b=2
        
        # comment
        ; comment
        [section leader]
        space thing = spaaace  # comment
        under_score = 1  ; comment
        dash-ing = yes
        empty = 
        colon : yep
        
        [override-some]
        a=5
        
        [interpolation]
        regular = 5
        magic = ${regular}
        very_magic = ${section leader:space thing}
        '''))

        configuration = loader.load(path)
        assert configuration == {
            'section leader': {
                'space_thing': 'spaaace',
                'under_score': '1',
                'dash_ing': 'yes',
                'empty': '',
                'colon': 'yep',
                'a': '1',
                'b': '2',
            },
            'override-some': {
                'a': '5',
                'b': '2',
            },
            'interpolation': {
                'regular': '5',
                'magic': '5',
                'very_magic': 'spaaace',
                'a': '1',
                'b': '2',
            }
        }

    class TestLoadPathArg(object):

        def test_file_path(self, loader):
            '''
            When file path, use it as a config path
            '''
            path = Path('conf')
            path_.write(path, contents=dedent('''\
            [section]
            option = value
            '''))

            configuration = loader.load(path)
            assert configuration == {'section': {'option': 'value'}}  # found it

        def test_dir_path(self, loader, configuration_stem):
            '''
            When directory path, use {dir}/{configuration_name}.conf as config path
            '''
            dir_path = Path('dir') 
            path = dir_path / (configuration_stem + '.conf')
            path_.write(path, contents=dedent('''\
            [section]
            option = value
            '''))

            configuration = loader.load(dir_path)
            assert configuration == {'section': {'option': 'value'}}  # found it

        def test_none(self, loader):
            '''
            When None, no config path is added
            '''
            configuration = loader.load(None)
            assert configuration == {}  # did not raise and empty result
            configuration = loader.load()
            assert configuration == {}  # did not raise and empty result

        def test_missing(self, loader):
            '''
            When path to missing file/dir, ValueError
            '''
            with pytest.raises(ValueError) as ex:
                loader.load(Path('missing'))
            assert 'file' in str(ex.value)

        def test_dir_path_missing_conf(self, loader):
            '''
            When directory path whose {dir}/{configuration_name}.conf is missing, but {dir} exists, then ValueError
            '''
            dir_ = Path('dir')
            dir_.mkdir()
            with pytest.raises(ValueError) as ex:
                loader.load(dir_)
            assert 'file' in str(ex.value)

    def test_help_message(self, loader, directory_name, configuration_stem):
        '''Correct help message'''
        description = 'Is amazing conf file'
        message = loader.cli_help_message(description)
        assert description in message
        assert (directory_name + '/' + configuration_stem + '.conf') in message
