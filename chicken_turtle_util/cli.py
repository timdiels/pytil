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
Command line interface (CLI) utilities:

- Click options with better defaults
- mixins to build a CLI application context
'''

from functools import partial
from chicken_turtle_util.function import compose
import click

def command(*args, **kwargs):
    #XXX don't forget to adjust in other projects when done
    kwargs_ = {
        'context_settings': {
            'help_option_names': ['-h', '--help']
        }
    }
    kwargs_.update(kwargs)
    return click.command(*args, **kwargs_)
'''Like `click.command`, but by default use short and long help options''' 

option = partial(click.option, show_default=True, required=True)
'''Like `click.option`, but by default ``show_default=True, required=True``'''

argument = partial(click.argument, required=True)
'''Like `click.argument`, but by default ``required=True``'''

password_option = partial(option, prompt=True, hide_input=True, show_default=False)
'''Like click.option, but by default ``prompt=True, hide_input=True, show_default=False, required=True``.'''

class Context(object):
    
    '''
    CLI Application Context
    
    The application context is meant to be passed around to disseminate what
    would otherwise be global variables or singletons, e.g. a database
    connection pool or a file cache.
    
    Usage example::
    
        from my_project import __version  # optional, but good practice
        from chicken_turtle_util.cli import Context
        
        # Put together an application context with mixins that fit your needs
        class MyAppContext(Mixin1, Mixin2, Context):
            pass
        
        @click.command()
        @click.version_option(version=__version__)  # optional, but good practice
        @MyAppContext.cli_options()  # options provided by the mixins
        def main(**kwargs):
            context = MyAppContext(**kwargs)  # option values are fed back to the mixins, e.g. database credentials
            
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
            def cli_options(cls):
                # combine our cli options with that of super (decorators are single argument functions, so we can use function.compose)
                return compose(
                    cli.option('--name', help='Your name.'),
                    # <-- you can add more options here if you like
                    super().cli_options()
                )
    '''
    
    def __init__(self, *args, **kwargs):
        pass
    
    @classmethod
    def cli_options(cls):
        '''
        Get CLI options corresponding to the required kwargs to `__init__`
        
        Returns
        -------
        decorator
            Decorator that decorates a function with the CLI options
        '''
        return lambda x: x
    
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
    
    Returns
    -------
    Context mixin
    '''
    
    class _DatabaseMixin(Context):
        
        def __init__(self, database_host, database_user, database_password, database_name, **kwargs):
            super().__init__(**kwargs)
            self._database = create_database(context=self, host=database_host, user=database_user, password=database_password, name=database_name)
        
        @property
        def database(self):
            return self._database
        
        @classmethod
        def cli_options(cls):
            return compose(
                option('--database-host', help='Host running the database to connect to. Provide its DNS or IP.'),
                option('--database-user', help='User name to authenticate with.'),
                password_option('--database-password', help='Password corresponding to user to authenticate with.'),
                option('--database-name', help='Name to use for SQL database on given host.'),
                super().cli_options()
            )
    
    return _DatabaseMixin
    
    