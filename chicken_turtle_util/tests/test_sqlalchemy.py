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
Test chicken_turtle_util.sqlalchemy
'''

from chicken_turtle_util.sqlalchemy import pretty_sql

expected = '''
SELECT meh,
       *
FROM
  (SELECT magic
   FROM TABLE) AS t1
UNION
  (SELECT magic2
   FROM TABLE) t2
INNER JOIN table_thing t3 ON t2.id = t3.id
WHERE t3.thing = 5
GROUP BY t3.meh
'''.strip()

def test_pretty_sql():
    input_ = expected.replace('\n', ' ').replace('  ', ' ')
    actual = pretty_sql(input_)
    print(actual)
    assert actual == expected
