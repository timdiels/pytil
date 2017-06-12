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
Test pytil.dict
'''

import pytest
import ast
from pytil.dict import pretty_print_head, DefaultDict, invert, assign

class TestPrettyPrintHead(object):

    def dict_(self, size):
        return dict(zip(range(size), range(size)))

    def test_invalid_count(self):
        '''When count < 1, ValueError'''
        with pytest.raises(ValueError):
            pretty_print_head(self.dict_(20), 0)

    @pytest.mark.parametrize('count', (1,10,19))
    def test_larger(self, capsys, count):
        '''When dict larger than `count`, print only `count` items'''
        pretty_print_head(self.dict_(20), count)
        out, _ = capsys.readouterr()
        actual = ast.literal_eval(out)
        assert isinstance(actual, dict)
        assert len(actual) == count

    @pytest.mark.parametrize('count', (0,1,10,19,20))
    def test_less_or_equal(self, capsys, count):
        '''When dict has less or equal length than count, print whole dict'''
        dict_ = self.dict_(count)
        pretty_print_head(dict_, 20)
        out, _ = capsys.readouterr()
        actual = ast.literal_eval(out)
        assert actual == dict_

def test_default_dict():
    '''Test everything of DefaultDict'''
    dict_ = DefaultDict(lambda key: key)
    assert dict_['missing'] == 'missing'

    dict_['present'] = 5
    assert dict_['present'] == 5

    del dict_['present']
    assert dict_['present'] == 'present'

def test_invert():
    '''Test everything of invert'''
    assert invert({}) == {}
    assert invert({1: 2, 3: 4}) == {2: {1}, 4: {3}}
    assert invert({1: 2, 3: 2, 4: 5}) =={2: {1,3}, 5: {4}}

def test_assign():
    destination = {1: 2, 3: 4}
    source = {3: 5, 6: 7}
    assign(destination, source)
    assert destination == {3: 5, 6: 7}
