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
Test chicken_turtle_util.logging
'''

from chicken_turtle_util.logging import set_level
import logging

def test_set_level(caplog):
    logger = logging.getLogger('test89374.logger')
    logger.setLevel(logging.WARNING)
    with set_level(logger, logging.INFO):
        logger.info('not ignored')
        logger.warning('not ignored')
    logger.info('ignored')
    logger.warning('not ignored')
    assert [x.msg for x in caplog.records()] == ['not ignored'] * 3