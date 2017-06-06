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

async def stubborn_gather(*awaitables):
    '''
    Stubbornly wait for awaitables, despite some of them raising

    Like a more stubborn version of asyncio.gather.

    Continue until all awaitables have finished or have raised. If one or more
    awaitables raise, a new `Exception` is raised with the traceback and message
    of each exception as message. However, if all exceptions raised are
    `asyncio.CancelledError`, `asyncio.CancelledError` is raised instead.

    If cancelled, cancels the (futures associated with the) awaitables.

    Parameters
    ----------
    awaitables : iterable(awaitable)
        Awaitables to await

    Returns
    -------
    results :: (any, ...)
        Return of each awaitable. The return of ``awaitables[i]`` is ``results[i]``.
    '''
    if awaitables:
        futures = [asyncio.ensure_future(awaitable) for awaitable in awaitables]
        results = [None] * len(futures)  # return values
        exceptions = []  # [(future_index, exception_raised)]

        # Await all and fill `results` and `exceptions`
        pending = futures
        while pending:
            try:
                done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_EXCEPTION)
                for future in done:
                    i = futures.index(future)
                    ex = future.exception()
                    if ex:
                        _logger.error('stubborn_gather: Awaitable {} raised:\n{}'.format(i, _format_exception(ex)))
                        exceptions.append((i, ex))
                    else:
                        results[i] = future.result()
            except asyncio.CancelledError:
                for future in pending:
                    future.cancel()
                raise

        # Raise cancelled if all raised cancelled
        if len(exceptions) == len(results) and all(isinstance(ex, asyncio.CancelledError) for _, ex in exceptions):
            raise asyncio.CancelledError()

        # Raise concatenation of exception messages if any raised
        if exceptions:
            formatted_exceptions = []
            for i, ex in exceptions:
                formatted_exceptions.append('Awaitable {}:\n{}'.format(i, _format_exception(ex)))
            formatted_exceptions = '\n'.join(formatted_exceptions)
            raise Exception('One or more awaitables raised an exception (not necessarily in this order):\n\n{}'.format(formatted_exceptions))

        # Simply return results otherwise
        return tuple(results)
    return ()

def _format_exception(ex):
    return ''.join(traceback.format_exception(ex.__class__, ex, ex.__traceback__))
