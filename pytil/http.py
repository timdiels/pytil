# Copyright (C) 2015, 2016 VIB/BEG/UGent - Tim Diels <timdiels.m@gmail.com>
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
HTTP utilities. Contains only `download`, download a http resource.
'''

from urllib.parse import urlparse
from pathlib import Path
import requests
import re

#TODO should pass in a file/directory to store it. Gives flexibility to use a
#temp dir and wouldn't require this function to cleanup either, that's the
#responsibility of the caller

#TODO rm in favor of https://docs.python.org/3.0/library/urllib.request.html#urllib.request.urlretrieve
# or rewrite this to make use of it instead. Its returned filename has the right extension, just not the right name. Sometimes that's all you need
# It already nicely raises on 404

# Based on http://stackoverflow.com/a/16696317/1031434
def download(url, destination):
    '''
    Download an HTTP resource to a file

    Parameters
    ----------
    url : str
        HTTP resource to download
    destination : pathlib.Path
        Location at which to store downloaded resource. If `destination` does
        not exist, it's assumed to be a file path. If `destination` exists and
        is a file, it is overwritten. If `destination` exists and is a
        directory, the file will be saved inside the directory with as name the
        file name suggested by a server, if any, or the last part of the URL
        otherwise (excluding query and fragment parts).

    Returns
    -------
    path : pathlib.Path
        Path to the downloaded file.
    name : str or None
        File name suggested by the server or None if none was suggested.
    '''
    response = requests.get(url, stream=True)

    # Get file name suggested by server
    file_name = None
    if 'content-disposition' in response.headers:
        match = re.search(r'filename="?([^"]+)"?', response.headers['content-disposition'])
        if match:
            file_name = match.group(1)

    # Ensure destination is a file
    if destination.is_dir():
        if file_name:
            destination /= file_name
        else:
            name = Path(urlparse(url).path).name
            if name:
                destination /= name
            else:
                destination /= 'unknown' 

    # Download
    with destination.open('wb') as f:
        for chunk in response.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive chunks
                f.write(chunk)
    return destination, file_name
