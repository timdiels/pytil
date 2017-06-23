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
Test pytil.test
'''

from pytil.test import reset_loggers
import logging

def test_reset_loggers():
    '''
    When loggers have been messed with, reset resets them to a fresh state
    '''
    logger_names = (None, 'pytil.test.unusedmodulename')
    loggers = list(map(logging.getLogger, logger_names))

    # Mess with loggers
    for logger in loggers:
        logger.addHandler(logging.StreamHandler())
        logger.addFilter(logging.Filter())

    # Reset
    reset_loggers('pytil\.test\.unusedmodule.*')

    # Assert loggers have been reset
    for logger in loggers:
        assert not logger.handlers
        assert not logger.filters