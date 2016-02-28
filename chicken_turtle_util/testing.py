# Copyright (C) 2016 Tim Diels <timdiels.m@gmail.com>
# 
# This file is part of Chicken Turtle.
# 
# Chicken Turtle is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Chicken Turtle is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with Chicken Turtle.  If not, see <http://www.gnu.org/licenses/>.

import pytest

def run_tests(project_name):
    args = (
        '-m current '
#         '-n auto --benchmark-disable'  # parallel testing (can't and shouldn't benchmark in parallel, so --benchmark-disable)
#         '--maxfail=1 '
        '--capture=no '
        '--basetemp=test/last_runs '
        '{}/test '
    ).format(project_name)
    pytest.main(args)