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
Extensions to asyncio.

Requires Python >=3.5
'''

import asyncio
import logging
import traceback

_logger = logging.getLogger(__name__)

async def stubborn_gather(*futures):
    '''
    Stubbornly wait for futures, despite some of them raising
    
    Like a more stubborn version of asyncio.gather.
    
    Continue until all futures have finished or have raised. If one or more
    futures raise, a new `Exception` is raised with the traceback and message of
    each exception as message. However, if all exceptions raised are
    `asyncio.CancelledError`, `asyncio.CancelledError` is raised instead.
    
    If cancelled, cancels the futures.
    
    Parameters
    ----------
    futures : iterable(awaitable)
        Futures to await
        
    Returns
    -------
    results :: (any, ...)
        Return of each future. The return of ``futures[i]`` is ``results[i]``.
    '''
    if futures:
        results = await asyncio.gather(*futures, return_exceptions=True)
        formatted_exceptions = []
        all_cancelled = True
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                if not isinstance(result, asyncio.CancelledError):
                    all_cancelled = False
                formatted_exception = ''.join(traceback.format_exception(result.__class__, result, result.__traceback__))
                formatted_exceptions.append('Future {}:\n{}'.format(i, formatted_exception))
            else:
                all_cancelled = False
        if formatted_exceptions:
            if all_cancelled:
                raise asyncio.CancelledError()
            else:
                formatted_exceptions = '\n'.join(formatted_exceptions)
                raise Exception('One or more futures raised an exception (not necessarily in this order):\n\n{}'.format(formatted_exceptions))
        return results
    return ()
