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
Test pytil.function
'''

import pytest
from pytil.function import compose

class TestCompose(object):

    def double(self, x):
        return 2*x

    def add(self, x):
        return x+1

    def test_empty(self):
        '''When composing nothing, ValueError'''
        with pytest.raises(ValueError):
            compose()

    def test_one(self):
        '''Allow 'composing' just 1 function'''
        assert compose(self.double)(2) == 4

    def test_order(self):
        '''Compose in the right order'''
        assert compose(self.double, self.add)(2) == 2 * (2+1)
        assert compose(self.add, self.double)(2) == 1 + 2*2
