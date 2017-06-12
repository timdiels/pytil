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
Test pytil.set
'''

from pytil.set import merge_by_overlap

def test_merge_by_overlap():
    sets = [{1,2}, set(), {2,3}, {4,5,6}, {6,7}]
    merge_by_overlap(sets)
    assert sets == [{1,2,3}, {4,5,6,7}]  # Note: the order doesn't actually matter, our test is too stringent
