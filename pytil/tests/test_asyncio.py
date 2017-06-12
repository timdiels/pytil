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
Test pytil.asyncio
'''

from pytil import asyncio as asyncio_
from pytil.test import assert_search_matches
from textwrap import dedent
import pytest
import asyncio
import re

class TestStubbornGather(object):

    async def f(self, x):
        return x

    @pytest.mark.asyncio
    async def test_happy_days(self):
        '''
        When given 2 tasks, await and return the results of both
        '''
        actual = await asyncio_.stubborn_gather(self.f(1), self.f(2))
        assert actual == (1, 2)

    @pytest.mark.asyncio
    async def test_exception(self, caplog):
        '''
        When given 1 task raises, await the other tasks, then raise a new
        exception
        '''
        raised = asyncio.Event()
        finished = False
        exception = Exception('ex')
        async def succeed():
            await raised.wait()
            nonlocal finished
            finished = True  # @UnusedVariable
        async def fail():
            raised.set()
            raise exception
        with pytest.raises(Exception) as ex:
            await asyncio_.stubborn_gather(fail(), succeed())
        assert finished
        assert ex != exception

        # Log the exception
        expected = dedent('''\
            .*stubborn_gather: Awaitable 0 raised:
            Traceback \(most recent call last\):
              .*
              .*
              File ".*/test_asyncio.py", line .*, in fail
                raise exception
            Exception: ex'''
        )
        assert_search_matches(caplog.text, expected, re.MULTILINE)

        # Also mention it in the thrown exception
        expected = dedent('''\
            .*Awaitable 0:
            Traceback \(most recent call last\):
              .*
              .*
              File ".*/test_asyncio.py", line .*, in fail
                raise exception
            Exception: ex'''
        )
        assert_search_matches(str(ex.value), expected, re.MULTILINE) 

    @pytest.mark.asyncio
    async def test_cancel(self):
        '''
        When gather cancelled, cancel the gathered tasks
        '''
        forever_locked = asyncio.Lock()
        async with forever_locked:
            async def forever():
                async with forever_locked:
                    assert False
            with pytest.raises(asyncio.CancelledError):
                futures = [asyncio.ensure_future(forever()) for _ in range(2)]
                gather_future = asyncio.ensure_future(asyncio_.stubborn_gather(*futures))
                asyncio.get_event_loop().call_soon(gather_future.cancel)
                await gather_future
            assert gather_future.cancelled()
            for future in futures:
                assert future.cancelled()

    @pytest.mark.asyncio
    async def test_awaitable_cancelled(self):
        '''
        When one of gather's futures is cancelled, keep going
        '''
        cancelled = asyncio.Event()
        finished = False
        async def succeed():
            await cancelled.wait()
            nonlocal finished
            finished = True  # @UnusedVariable
        async def gets_cancelled():
            await cancelled.wait()
        gets_cancelled_future = asyncio.ensure_future(gets_cancelled())
        loop = asyncio.get_event_loop()
        loop.call_soon(gets_cancelled_future.cancel)  # these are called in order
        loop.call_soon(cancelled.set)
        with pytest.raises(Exception) as ex:
            await asyncio_.stubborn_gather(gets_cancelled_future, succeed())
        assert not isinstance(ex, asyncio.CancelledError)
        assert finished

    @pytest.mark.asyncio
    async def test_awaitables_cancelled(self):
        '''
        When all of gather's futures are cancelled, raise CancelledError
        '''
        forever_locked = asyncio.Lock()
        async with forever_locked:
            async def forever():
                async with forever_locked:
                    assert False
            with pytest.raises(asyncio.CancelledError):
                futures = [asyncio.ensure_future(forever()) for _ in range(2)]
                for future in futures:
                    asyncio.get_event_loop().call_soon(future.cancel)
                await asyncio_.stubborn_gather(*futures)
