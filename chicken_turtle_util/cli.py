# Copyright (C) 2016 VIB/BEG/UGent - Tim Diels <timdiels.m@gmail.com>
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
click options with better defaults
'''

from functools import partial
import click

option = partial(click.option, show_default=True, required=True)
'''Like click.option, but by default show_default=True, required=True'''

argument = partial(click.argument, required=True)
'''Like click.argument, but by default required=True'''

def password_option(*args, **kwargs):
    '''
    Like click.option, but by default prompt=True, hide_input=True, show_default=False, required=True.
    '''
    kwargs_ = dict(prompt=True, hide_input=True, show_default=False)
    kwargs_.update(kwargs)
    return option(*args, **kwargs_)
