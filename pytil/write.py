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
File writers
'''

from contextlib import contextmanager
from csv import DictWriter

def tsv(file, *args, **kwargs):
    return csv(file, delimiter='\t', *args, **kwargs)

@contextmanager
def csv(file, *args, **kwargs):
    '''
    Write CSV file.

    Parameters
    ----------
    file : Path
    *args
        csv.DictWriter args (except the f arg)
    **kwargs
        csv.DictWriter args

    Examples
    --------
    with write.csv(file) as writer:
        writer.writerow((1,2,3))
    '''
    with file.open('w', newline='') as f:
        yield DictWriter(f, *args, **kwargs)
