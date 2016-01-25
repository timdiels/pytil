# Copyright (C) 2016 VIB/BEG/UGent - Tim Diels <timdiels.m@gmail.com>
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

from urllib.parse import urlparse
import pandas as pd
import requests
import re
import plumbum as pb
from chicken_turtle.pandas import df_expand_iterable_values

class Object(object):
    '''
    Like object, but doesn't complain on __init__ when given args.
    
    This behaviour used to be the default before Python 3. 
    '''
    def __init__(self, *args, **kwargs):
        super().__init__()

# Based on http://stackoverflow.com/a/16696317/1031434
def download_file(url, dest_dir):
    '''
    Download `url` resource content to `dest_dir`
    
    Parameters
    ----------
    url : str
    dest_dir : plumbum.Path
        Directory to save download in.
    
    Returns
    -------
    plumbum.Path
        Path to which file was downloaded. The filename suggested by the server
        is used if provided, else the last part of the url path is used (without
        query and fragment parts).
    '''
    response = requests.get(url, stream=True)
    
    # derive file_name
    file_name = None
    if 'content-disposition' in response.headers:
        match = re.match(r'filename=(.+)', response.headers['content-disposition'])
        if match:
            file_name = match.groups(0)
    if not file_name:
        file_name = pb.local.path(urlparse(url).path).name
    
    # download  
    dest = dest_dir / file_name
    with open(dest, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
    return dest

def is_data_file(path):
    '''
    Is a regular data file or directory, e.g. a clustering.
    
    Parameters
    ----------
    path : plumbum.Path
    
    Returns
    -------
    bool
    '''
    return not path.name.startswith('.')
    # XXX add filecmp.DEFAULT_IGNORES to things to ignore

if __name__ == '__main__':
    df = pd.DataFrame([[1,[1,2],[1]],[1,[1,2],[3,4,5]],[2,[1],[1,2]]], columns='check a b'.split())
    print(df)
    print(df_expand_iterable_values(df, ['a', 'b']))
    