# Copyright (C) 2017 VIB/BEG/UGent - Tim Diels <timdiels.m@gmail.com>
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
File parsers
'''

from csv import DictReader

def tsv(file, *args, **kwargs):
    return csv(file, delimiter='\t', *args, **kwargs)

class csv:
    '''
    Parse CSV file.

    Parameters
    ----------
    file : Path
    *args
        csv.DictReader args (except the f arg)
    **kwargs
        csv.DictReader args

    Examples
    --------
    for row in parse.csv(file):
        print(row['column'])

    with parse.csv(file) as reader:
        for row in reader:
            pass
    '''

    def __init__(self, file, *args, **kwargs):
        self._file = file
        self._args = args
        self._kwargs = kwargs

    def __iter__(self):
        with self as reader:
            yield from reader

    def __enter__(self):
        self._f = self._file.open('r', newline='')
        return DictReader(self._f, *self._args, **self._kwargs)

    def __exit__(self, *_):
        self._f.close()
