# Copyright (C) 2015, 2016 VIB/BEG/UGent - Tim Diels <timdiels.m@gmail.com>
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

# TODO there's also a config.py file, merge or remove it. Whut?

'''
Configuration loaders, currently only from configuration files
'''

from xdg.BaseDirectory import xdg_config_dirs
from configparser import ConfigParser, ExtendedInterpolation
from pkg_resources import resource_string
from textwrap import dedent
from pathlib import Path
from chicken_turtle_util import path as path_
from contextlib import suppress

class ConfigurationLoader(object):

    '''
    Loads a single configuration from one or more files 

    Reads configuration files in this order:

    1. ``/etc/{directory_name}/{configuration_name}.conf``
    2. for each `XDG <https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html>`_
       config dir, try ``{xdg_config_dir}/{directory_name}/{configuration_name}.conf``

    If none are found, the defaults are used. The first configuration file can
    be said to inherit the defaults. Any next configuration files inherit the
    configuration of their predecessors. Defaults are specified in the package
    data of `package_name` with path ``data/{configuration_name}.defaults.conf``.

    Configuration values are treated as strings. Empty strings are allowed.
    Inline comments can be started with '#' and ';'. The 'default' section
    provides defaults for other sections. `ExtendedInterpolation 
    <https://docs.python.org/3/library/configparser.html#configparser.ExtendedInterpolation>`_
    is used. Option names have '-' and ' ' replaced with '_'; section names do
    not, but as that may change in the future, we recommend using all underscore
    section names only.

    Parameters
    ----------
    package_name : str
        Fully qualified name of the package whose package data contains the defaults file
    directory_name : str
        Name of directory in which configuration files should reside.
    configuration_name : str
        Name of configuration file (without suffix; a '.conf' suffix is added)

    Notes
    -----
    The interface also aims to enforce consistency and good practice across
    applications, so it's kept intentionally rigid in some regards.
    '''  

    def __init__(self, package_name, directory_name, configuration_name):
        self._package_name = package_name
        self._directory_name = directory_name
        self._configuration_name = configuration_name

        # Determine paths to search for config files
        dirs = [Path('/etc')] + [Path(x) for x in reversed(xdg_config_dirs)]
        self._paths = [x / directory_name / '{}.conf'.format(configuration_name) for x in dirs]

    # Note: this docstring is also used to describe ConfigurationMixin's API (doc coupling)
    def load(self, path=None):
        '''
        Load configuration (from configuration files)

        Parameters
        ----------
        path : pathlib.Path or None
            Path to configuration file, which must exist; or path to directory
            containing a configuration file; or None.

        Returns
        -------
        {section :: str => { option :: str => value :: str}}
            The configuration. The 'default' section is not included. However,
            all options from the 'default' section are included in each other
            returned section.

        Raises
        ------
        ValueError
            if `path` is a missing file; or if it is a directory which does not
            contain the configuration file.
        '''
        # Add path
        paths = self._paths.copy()
        if path:
            if path.is_dir():
                path /= '{}.conf'.format(self._configuration_name)
            paths.append(path)

        # Prepend file sys root to abs paths
        paths = [(path_._root / str(x)[1:] if x.is_absolute() else x) for x in paths]
        if path:
            path = paths[-1]

            # Passed path must exist
            if not path.exists():
                raise ValueError('Expected configuration file at {}'.format(path))

        # Configure parser
        config_parser = ConfigParser(
            inline_comment_prefixes=('#', ';'), 
            empty_lines_in_values=False, 
            default_section='default', 
            interpolation=ExtendedInterpolation()
        )

        def option_transform(name):
            return name.replace('-', '_').replace(' ', '_').lower()

        config_parser.optionxform = option_transform

        # Parse defaults and configs
        with suppress(FileNotFoundError):
            defaults_contents = resource_string(self._package_name, 'data/{}.defaults.conf'.format(self._configuration_name))
            config_parser.read_string(defaults_contents.decode('UTF-8')) #TODO fails
        config_parser.read([str(x) for x in paths])  # reads in given order

        config = {k : dict(v) for k,v in config_parser.items()}
        del config['default']
        return config

    def cli_help_message(self, description):
        '''
        Get a user friendly help message that can be dropped in a
        `click.Command`'s epilog

        Parameters
        ----------
        description : str
            Description of the configuration file to include in the message.

        Returns
        -------
        str
            A help message that uses `click`'s help formatting constructs (e.g. ``\b``)
        '''
        config_files_listing = '\n'.join('    {}. {!s}'.format(i, path) for i, path in enumerate(self._paths, 1))
        text = dedent('''\
        {config_file}:
        
            {description}
            
            {config_file} files are read from the following locations:
            
            \b
            {config_files_listing}
            
            Any configuration file can override options set by previous configuration files. Some 
            configuration file locations can be changed using the XDG standard (http://standards.freedesktop.org/basedir-spec/basedir-spec-0.6.html).
        ''').format(  # XXX explain more fully
            config_file='{}.conf'.format(self._configuration_name),
            description=description,
            config_files_listing=config_files_listing
        )
        return text
