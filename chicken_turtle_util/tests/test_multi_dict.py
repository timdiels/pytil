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
Test chicken_turtle_util.multi_dict
'''

from chicken_turtle_util.multi_dict import MultiDict

class TestMultiDict(object):

    def test_empty(self):
        actual = MultiDict({})
        assert set(actual.items()) == set()
        assert set(actual.keys()) == set()
        assert set(actual.values()) == set()
        assert actual.invert() == {}

    def test_normal(self):
        original = {
            1: {1,2,3},
            2: {1},
            3: {4,5}
        }

        actual_dict = original.copy()
        actual = MultiDict(actual_dict)

        assert actual.dict == actual_dict
        assert set(actual.items()) == {(1,1), (1,2), (1,3), (2,1), (3,4), (3,5)}
        assert set(actual.keys()) == {1, 2, 3}
        assert set(actual.values()) == {1, 2, 3, 4, 5}
        assert actual.invert() == {
            1: {1,2},
            2: {1},
            3: {1},
            4: {3},
            5: {3}
        }