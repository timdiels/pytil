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

'''
Utilities to build a Command line interface (CLI)

- `click` options with better defaults
- mixins to build a CLI application context
'''

from functools import partial, wraps
from chicken_turtle_util.function import compose
from pathlib import Path
import click 
import xdg
from textwrap import dedent, TextWrapper

option = partial(click.option, show_default=True, required=True)
'''Like `click.option`, but by default ``show_default=True, required=True``'''

argument = partial(click.argument, required=True)
'''Like `click.argument`, but by default ``required=True``'''

password_option = partial(option, prompt=True, hide_input=True, show_default=False)
'''Like click.option, but by default ``prompt=True, hide_input=True, show_default=False, required=True``.'''

class Context(object):
    
    '''
    Application context
    
    The application context is meant to be passed around to spread application-
    global objects, e.g. a database connection pool or a file cache. (These would
    otherwise be completely global.)
    
    Usage example::
    
        from my_project import __version__, 
        from chicken_turtle_util.cli import Context
        
        # Put together an application context with mixins that fit your needs
        # Here we used a mixin providing a database and one providing good practices
        class MyAppContext(DatabaseMixin(Database), BasicsMixin(__version__), Context):
            pass
        
        @MyAppContext.command()  # The mixins add their options to the click.command, e.g. BasicsMixin adds a --version option
        def main(context): # an instance of MyAppContext is constructed using CLI option input from the user. Its context.database (provided by DatabaseMixin) is now an instance of Database
            pass
            
    Example of writing a custom mixin::
    
        import chicken_turtle_util.cli as cli
        import function
        
        class NameMixin(cli.Context):
        
            "Adds a --name cli option and provides the result as the `name` property"
            
            def __init__(self, name, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self._name = name
            
            @property
            def name(self):
                return self._name
            
            @classmethod
            def command(class_, *args, **kwargs):  # Note click.command takes a `cls` argument, so you should name your class arg `class_` instead of `cls`
                # combine our cli options with that of super (decorators are single argument functions, so we can use function.compose)
                return compose(
                    # <-- decorators that decorate a click.Command go here
                    super(NameMixin, class_).command(*args, **kwargs)
                    cli.option('--name', help='Your name.'),
                    # <-- decorators that decorate the callback function, e.g. option and argument decorators should go here
                )
    '''
    
    def __init__(self, *args, **kwargs):
        self.unused_cli_args = (args, kwargs)
    
    @classmethod
    def command(class_, *args, **kwargs):
        '''
        Like `click.command`, wraps a function and returns a Command.
        
        Refer to the mixins' doc you use for any differences in parameter
        defaults, and the returned Command.
        
        Parameters
        ----------
        *args, **kwargs
            See `click.command` and refer to your mixins' doc for any differences
        '''
        def pass_context(func):
            @wraps(func)
            def wrapped(**kwargs):
                context = class_(**kwargs)
                args, kwargs = context.unused_cli_args
                return func(*args, context=context, **kwargs)
            return wrapped
        
        return compose(
            click.command(*args, **kwargs),
            pass_context
        )

def BasicsMixin(version):        
    '''
    Application context mixin that provides good practices such as a short and
    long help options, as well as a version option
    
    Parameters
    ----------
    version : str
        Application version string, e.g. ``1.0.0``
    '''
    
    class _BasicsMixin(Context):
        
        @classmethod
        def command(class_, *args, **kwargs):
            '''
            Like `click.command`, but by default use short and long help options and
            add a version option. Subclasses may make additional modifications.
            '''
            kwargs_ = {
                'context_settings': {
                    'help_option_names': ['-h', '--help']
                }
            }
            kwargs_.update(kwargs)
            
            return compose(
                super(_BasicsMixin, class_).command(*args, **kwargs_),
                click.version_option(version=version)
            )

    return _BasicsMixin

def DatabaseMixin(create_database):
    
    '''
    Application Context mixin that provides a database
    
    Parameters
    ----------
    create_database : (context :: Context, host :: str, user :: str, password :: str, name :: str) -> (database :: any)
        function that creates a database. `context` is an instance of your
        Context class. `host` is a DNS or IP of the database server to connect
        to. `user` and `password` are the credentials to connect with. `name` is
        the name of the database to connect to.
    '''
    
    class _DatabaseMixin(Context):
        
        def __init__(self, database_host, database_user, database_password, database_name, **kwargs):
            super().__init__(**kwargs)
            self._database = create_database(context=self, host=database_host, user=database_user, password=database_password, name=database_name)
        
        @property
        def database(self):
            return self._database
        
        @classmethod
        def command(class_, *args, **kwargs):
            return compose(
                super(_DatabaseMixin, class_).command(*args, **kwargs),
                option('--database-host', help='Host running the database to connect to. Provide its DNS or IP.'),
                option('--database-user', help='User name to authenticate with.'),
                password_option('--database-password', help='Password corresponding to user to authenticate with.'),
                option('--database-name', help='Name to use for SQL database on given host.')
            )
    
    return _DatabaseMixin
    
def ConfigurationMixin(create_configuration, help_message):
    '''
    Application Context mixin for loading a configuration
    
    CLI options added:
    
    --configuration path
        Configuration file or directory.
    
    Parameters
    ----------
    create_configuration : (context :: Context, path :: Path or None) -> (configuration :: any)
        function that creates a configuration. `context` is an instance of your
        Context class. `path` is the path to a configuration file or directory
        containing the configuration file, specified on the CLI, or None if none
        was specified.
    help_message : str
        String to include in any command's help message that uses this Context
        
    See also
    --------
    configuration.ConfigurationLoader: loads and parses configurations
    '''
    
    class _ConfigurationMixin(Context):
    
        def __init__(self, configuration, **kwargs):
            super().__init__(**kwargs)
            try:
                configuration = Path(configuration) if configuration else None
                self._configuration = create_configuration(self, configuration)
            except Exception as ex:
                print('Error: ' + str(ex))  # Note: click simply exits non-zero without printing the exception message
                raise
            
        @property
        def configuration(self):
            return self._configuration
        
        @classmethod
        def command(class_, *args, **kwargs):
            def modify_command(command):
                if not command.epilog:
                    command.epilog = ''
                command.epilog += '\n' + help_message
                return command
            return compose(
                modify_command,
                super(_ConfigurationMixin, class_).command(*args, **kwargs),
                option(
                    '--configuration', 
                    type=click.Path(exists=True),
                    required=False, 
                    help='Configuration file or directory.' 
                )
            )
        
    return _ConfigurationMixin
    
def ConfigurationsMixin(help_messages):
    '''
    Application Context mixin for loading multiple configurations
    
    CLI options added:
    
    --configuration name path
        Configuration file or directory.
        
    Attributes added:
    
    _configuration_paths : {configuration_name :: str => Path}
        User provided custom location for each configuration
    
    Parameters
    ----------
    help_messages : {configuration_name :: str => help_message :: str}
        String to include in any command's help message that uses this Context
        
    See also
    --------
    configuration.ConfigurationLoader: loads and parses configurations
    
    Examples
    --------
    ::
        class MyContext(ConfigurationsMixin({'main': 'Configure ...', 'test': 'Configure testing'):
            def __init__(self, **kwargs)
                super().__init__.(**kwargs)
                self._configuration_custom_paths  # is now available, allowing you to load configuration with e.g. `ConfigurationLoader`s
    '''
    
    class _ConfigurationsMixin(Context):
        
        def __init__(self, configuration, **kwargs):
            super().__init__(**kwargs)
            self.__configuration_paths = dict((name, Path(path)) for name, path in configuration)
            
        @property
        def _configuration_paths(self):
            '''
            User provided custom location for each configuration
            '''
            return self.__configuration_paths
        
        @classmethod
        def command(class_, *args, **kwargs):
            def modify_command(command):
                if not command.epilog:
                    command.epilog = ''
                message = dedent('''\
                    \b
                    Configuration files
                    -------------------
                ''')
                wrapper = TextWrapper(initial_indent='    ', subsequent_indent='    ')
                message += '\n'.join(name + '\n' + wrapper.fill(description) for name, description in sorted(help_messages.items()))
                command.epilog += '\n' + message
                return command
            
            choice_type = click.Choice(help_messages.keys())
            choice_type.name = 'name'
            
            return compose(
                modify_command,
                super(_ConfigurationsMixin, class_).command(*args, **kwargs),
                option(
                    '--configuration',
                    nargs=2,
                    multiple=True,
                    type=(choice_type, click.Path(exists=True)),
                    required=False,
                    help='Configuration file or directory.' 
                )
            )
            
    return _ConfigurationsMixin
    
class OutputDirectoryMixin(Context):
    
    '''
    Application Context mixin, allows user to specify an output directory
    
    CLI options added:
    
    --output-directory
        Directory to write output files to.
    '''
    
    def __init__(self, output_directory, **kwargs):
        super().__init__(**kwargs)
        self._output_directory = Path(output_directory)
    
    @property
    def output_directory(self):
        '''
        Get directory to write output files to
        
        This directory exists and is writable (at time of application
        invocation).
        
        Returns
        -------
        pathlib.Path
        '''
        return self._output_directory
    
    @classmethod
    def command(class_, *args, **kwargs):
        return compose(
            super(OutputDirectoryMixin, class_).command(*args, **kwargs),
            option(
                '--output-directory',
                type=click.Path(file_okay=False, writable=True, exists=True, resolve_path=True),
                help='Directory to write output files to.'
            )
        )
    
# TODO rm
# def DefaultsConfigurationMixin(package_name, directory_name):
#     
#     '''
#     Application context mixin, read CLI defaults from `cli.conf`
#     
#     See `ConfigurationLoader` for details on the configuration format and file
#     locations. The defaults must appear as options in the ``[cli]`` section.
#     
#     Parameters
#     ----------
#     package_name
#         See `ConfigurationLoader`
#     directory_name
#         See `ConfigurationLoader`
#     '''
# 
#     class _DefaultsConfigurationMixin(Context):
#         
#         @classmethod
#         def command(class_, *args, **kwargs):
#             context_settings = kwargs.get('context_settings', {})
#             
#             config = ConfigurationLoader(package_name, directory_name, 'cli')
#             defaults = config.load()['cli']
#             assert 'default_map' not in context_settings, 'Mixin conflict: kwargs["context_settings"]["default_map"] already set'
#             context_settings['default_map'] = defaults
#             
#             epilog = 'The above defaults reflect your current configuration. These defaults can be changed in a cli.conf configuration file.\n'
#             if 'epilog' in context_settings:
#                 epilog += '\n' + context_settings['epilog']
#             epilog += '\n' + config.cli_help_message('CLI defaults, specified in a [cli] section.')
#             context_settings['epilog'] = epilog
#             
#             super(_DefaultsConfigurationMixin, class_).command(*args, **kwargs)    
#                 

def DataDirectoryMixin(directory_name):
 
    '''
    Application context mixin, provides context.data_directory
    
    Data directory is taken from XDG data home. A user can change this using the
    XDG_DATA_HOME env variable.
    
    Parameters
    ----------
    directory_name : str
        Subdirectory to use inside XDG data home. This should be your
        application name in all lowercase with spaces replaced by underscores.
    '''
    
    class _DataDirectoryMixin(Context):
        
        @property
        def data_directory(self):
            '''
            Get data root directory
            
            Only data that needs to be persistent should be stored here.
            '''
            return Path(xdg.BaseDirectory.xdg_data_home) / directory_name
        
    return _DataDirectoryMixin

def CacheDirectoryMixin(directory_name):
 
    '''
    Application context mixin, provides context.cache_directory
    
    Data directory is taken from XDG cache home. A user can change this using the
    XDG_CACHE_HOME env variable.
    
    Parameters
    ----------
    directory_name : str
        Subdirectory to use inside XDG cache home. This should be your
        application name in all lowercase with spaces replaced by underscores.
    '''
    
    class _CacheDirectoryMixin(Context):
        
        @property
        def cache_directory(self):
            '''
            Get cache root directory
            
            Only non-persistent data that is reused between runs should be stored here.
            '''
            return Path(xdg.BaseDirectory.xdg_cache_home) / directory_name
        
    return _CacheDirectoryMixin  
