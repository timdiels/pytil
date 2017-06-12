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
Set utilities. Contains only `merge_by_overlap`, merges overlapping sets in place.
'''

def _locate_bin(bins, n):
    """
    Find the bin where list n has ended up: Follow bin references until
    we find a bin that has not moved.
    """
    while bins[n] != n:
        n = bins[n]
    return n

# XXX test performance compared to original alg

# Original implementation by http://stackoverflow.com/users/699305/alexis
# at http://stackoverflow.com/a/9453249/1031434
# Modified slightly 
def merge_by_overlap(sets):
    '''
    Of a list of sets, merge those that overlap, in place.

    The result isn't necessarily a subsequence of the original `sets`.

    Parameters
    ----------
    sets : [{any}]
        Sets of which to merge those that overlap. Empty sets are ignored.

    Notes
    -----
    Implementation is based on `this StackOverflow answer`_. It outperforms all
    other algorithms in the thread (visited at dec 2015) on python3.4 using a
    wide range of inputs.

    .. _this StackOverflow answer: http://stackoverflow.com/a/9453249/1031434

    Examples
    --------
    >>> merge_by_overlap([{1,2}, set(), {2,3}, {4,5,6}, {6,7}])
    [{1,2,3}, {4,5,6,7}]
    '''
    data = sets
    bins = list(range(len(data)))  # Initialize each bin[n] == n
    nums = dict()

    for r, row in enumerate(data):
        if not row:
            data[r] = None
        else:
            for num in row:
                if num not in nums:
                    # New number: tag it with a pointer to this row's bin
                    nums[num] = r
                    continue
                else:
                    dest = _locate_bin(bins, nums[num])
                    if dest == r:
                        continue  # already in the same bin

                    if dest > r:
                        dest, r = r, dest  # always merge into the smallest bin

                    data[dest].update(data[r])
                    data[r] = None
                    # Update our indices to reflect the move
                    bins[r] = dest
                    r = dest 

    # Remove empty bins
    for i in reversed(range(len(data))):
        if not data[i]:
            del data[i]
