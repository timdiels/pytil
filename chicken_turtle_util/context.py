# Copyright (C) 2015, 2016 VIB/BEG/UGent - Tim Diels <timdiels.m@gmail.com>
# 
# This file is part of Chicken Turtle.
# 
# Chicken Turtle is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Chicken Turtle is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with Chicken Turtle.  If not, see <http://www.gnu.org/licenses/>.

'''
Mixins to build a Context class (or 'Application' class if you prefer)

To create a context class: e.g. class MyContext(Mixin1, Mixin2, ...): pass
'''

from chicken_turtle_util import compose
from chicken_turtle_util import flatten
from chicken_turtle import cli
import click

        
def cli_options(class_):
    '''
    Get click CLI options of the built context class 
    '''
    options = flatten([cls._cli_options for cls in class_.__mro__[1:] if hasattr(cls, '_cli_options')])
    return compose(*options)

class Context(object):
    def __init__(self, *args, **kwargs):
        pass
    
def DatabaseMixin(Database):
    
    '''
    Database access
    '''
    
    class _DatabaseMixin(Context):
    
        _cli_options = [
            cli.option('--database-host', help='Host running the database to connect to. Provide its DNS or IP.'),
            cli.option('--database-user', help='User name to authenticate with.'),
            cli.password_option('--database-password', help='Password corresponding to user to authenticate with.'),
            cli.option('--database-name', help='Name to use for SQL database on given host.'),
        ]
        
        def __init__(self, database_host, database_user, database_password, database_name, **kwargs):
            super().__init__(**kwargs)
            self._database = Database(host=database_host, user=database_user, password=database_password, name=database_name)
        
        @property
        def database(self):
            return self._database
    
    return _DatabaseMixin
    
    