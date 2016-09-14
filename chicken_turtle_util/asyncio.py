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

#TODO doc and test (API stuff checklist)

import asyncio

async def stubborn_gather(*futures): #TODO untested
    '''
    Stubbornly wait for futures, despite some of them raising
    
    Like a more stubborn version of asyncio.gather.
    
    Continue until all futures have finished or have raised. If one or more
    futures raise, one of the exceptions is reraised.
    
    If cancelled, cancels the futures. If a future is cancelled, the future
    raises an exception, which is handled like any other exception raised by
    a future (see above).
    
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
        for result in results:
            if isinstance(result, Exception):
                raise result
        return results
    return ()
