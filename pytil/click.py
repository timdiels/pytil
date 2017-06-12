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
`click` utilities
'''

import click
from click.testing import CliRunner
from functools import partial
import traceback

option = partial(click.option, show_default=True, required=True)
'''Like `click.option`, but by default ``show_default=True, required=True``'''

argument = partial(click.argument, required=True)
'''Like `click.argument`, but by default ``required=True``'''

password_option = partial(option, prompt=True, hide_input=True, show_default=False)
'''Like click.option, but by default ``prompt=True, hide_input=True, show_default=False, required=True``.'''

def assert_runs(*args, **kwargs):
    '''
    Invoke click command and assert it completes successfully

    Parameters
    ----------
    *args, **kwargs
        CliRunner.invoke arguments, excluding catch_exceptions

    Returns
    -------
    result : click.testing.Result
    '''
    result = CliRunner().invoke(*args, **kwargs)
    if result.exception:
        print(result.output)
        traceback.print_exception(*result.exc_info)
        assert False
    return result
