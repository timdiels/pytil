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

from chicken_turtle_util import logging as logging_, path as path_
from chicken_turtle_util.test import assert_text_equals
from pathlib import Path
from textwrap import dedent
import logging
import re

def test_set_level(caplog):
    logger = logging.getLogger('test89374.logger')
    logger.setLevel(logging.WARNING)
    with logging_.set_level(logger, logging.INFO):
        logger.info('not ignored')
        logger.warning('not ignored')
    logger.info('ignored')
    logger.warning('not ignored')
    assert [x.msg for x in caplog.records] == ['not ignored'] * 3

def test_configure(temp_dir_cwd, capsys, caplog):
    log_file = Path('file.log')
    stderr_handler, file_handler = logging_.configure(log_file)
    assert isinstance(stderr_handler, logging.StreamHandler)
    assert isinstance(file_handler, logging.FileHandler)

    logger = logging.getLogger(__name__)
    logger.info('Fake info')
    logger.debug('Ignored debug')
    logger.setLevel(logging.DEBUG)
    logger.debug('Fake debug')

    # stderr
    #
    # - level is INFO
    # - terse format
    expected = 'I: Fake info\n'
    actual = capsys.readouterr()[1]
    assert_text_equals(actual, expected)

    # log file
    #
    # - level is DEBUG
    # - long format with fairly unambiguous source
    log_file_content = path_.read(log_file)
    def prefix(log_type, package, module_name):
        return r'{} [0-9]{{4}}-[0-9]{{2}}-[0-9]{{2}} [0-9]{{2}}:[0-9]{{2}}:[0-9]{{2}},[0-9]{{3}} {} \({}:[0-9]+\):'.format(
            log_type, package, module_name
        )
    pattern = dedent('''\
        {}
        Fake info
        
        {}
        Fake debug
        '''
        .format(
            prefix('I', __name__, 'test_logging'),
            prefix('D', __name__, 'test_logging'),
        )
    )
    assert re.match(pattern, log_file_content, re.MULTILINE), 'Actual:{}\n\nExpected to match:\n{}'.format(log_file_content, pattern)
