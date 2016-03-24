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
Test chicken_turtle_util.pyqt
'''

from PyQt5.QtCore import QObject
from chicken_turtle_util.pyqt import block_signals

def test_block_signals():
    obj = QObject()
    
    assert not obj.signalsBlocked()
    with block_signals(obj):
        assert obj.signalsBlocked()
    assert not obj.signalsBlocked()
    
    obj.blockSignals(True)
    with block_signals(obj):
        assert obj.signalsBlocked()
    assert obj.signalsBlocked()