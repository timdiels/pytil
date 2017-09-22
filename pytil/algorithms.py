# Copyright (C) 2015 VIB/BEG/UGent - Tim Diels <timdiels.m@gmail.com>
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
Various algorithms.
'''

from sklearn.utils.extmath import cartesian
from collections_extended import frozenbag, setlist
from more_itertools import windowed
import networkx as nx
import numpy as np

def spread_points_in_hypercube(point_count, dimension_count): #TODO rename points_spread_in_hypercube #TODO rename dimension_count -> dimensions
    '''
    Place points in a unit hypercube, approximately maximising the minimum of
    distances between points.

    Euclidean distance is used.

    Parameters
    ----------
    point_count : int
        Number of points to pick.
    dimension_count : int
        Number of dimensions of the hypercube.

    Returns
    -------
    ~numpy.array[float]
        Points spread approximately optimally across the hypercube. Array shape
        is ``(point_count, dimension_count)``.

    Raises
    ------
    ValueError
        When ``point_count < 0 or dimension_count < 1``.

    Notes
    -----
    The current implementation puts points in a hypergrid. The exact solution to
    this problem is known for only a few ``n``. See also this `StackOverflow
    question with solutions to the problem <https://stackoverflow.com/q/2723626/1031434>`_.
    '''
    # Current implementation simply puts points in a grid
    if point_count < 0:
        raise ValueError('point_count must be at least 0')
    if dimension_count < 1:
        raise ValueError('dimension_count must be at least 1')
    if point_count == 0:
        return np.empty(shape=(0,dimension_count))
    side_count = np.ceil(point_count ** (1/dimension_count)) # number of points per side
    points = np.linspace(0, 1, side_count)
    points = cartesian([points]*dimension_count)
    return points[:point_count]

class _Bin(object):
    def __init__(self):
        self._items = []
        self._weights_sum = 0

    def add(self, item, weight):
        self._items.append(item)
        self._weights_sum += weight

    @property
    def items(self):
        return self._items

    @property
    def weights_sum(self):
        return self._weights_sum

def multi_way_partitioning(items, bin_count): #TODO rename bin_count -> bins
    '''
    Greedily divide weighted items equally across bins.

    This approximately solves a multi-way partition problem, minimising the
    difference between the largest and smallest sum of weights in a bin.

    Parameters
    ----------
    items : ~typing.Iterable[~typing.Tuple[~typing.Any, float]]
        Weighted items as ``(item, weight)`` tuples.
    bin_count : int
        Number of bins.

    Returns
    -------
    bins : ~collections_extended.frozenbag[~collections_extended.frozenbag[~typing.Any]]
        Item bins as a bag of item bags.

    Notes
    ----------
    - `A greedy solution <http://stackoverflow.com/a/6855546/1031434>`_
    - `Problem definition and solutions <http://ijcai.org/Proceedings/09/Papers/096.pdf>`_
    '''
    bins = [_Bin() for _ in range(bin_count)]
    for item, weight in sorted(items, key=lambda x: x[1], reverse=True):
        bin_ = min(bins, key=lambda bin_: bin_.weights_sum) 
        bin_.add(item, weight)
    return frozenbag(frozenbag(bin_.items) for bin_ in bins)

# Note: Currently unused. Test and polish before using it
# Note: a deterministic variant of this could be built with https://pypi.python.org/pypi/toposort/1.0
def toset_from_tosets(*tosets):  # Note: a setlist is perfect representation of a toset as it's totally ordered and it's a set, i.e. a toset
    '''
    Create totally ordered set (toset) from tosets.

    These tosets, when merged, form a partially ordered set. The linear
    extension of this poset, a toset, is returned.

    .. warning:: untested

    Parameters
    ----------
    tosets : Iterable[~collections_extended.setlist]
        Tosets to merge.

    Raises
    ------
    ValueError
        If the tosets (derived from the lists) contradict each other. E.g. 
        ``[a, b]`` and ``[b, c, a]`` contradict each other.

    Returns
    -------
    toset : ~collectiontions_extended.setlist
        Totally ordered set.
    '''
    # Construct directed graph with: a <-- b iff a < b and adjacent in a list
    graph = nx.DiGraph()
    for toset in tosets:
        graph.add_nodes_from(toset)
        graph.add_edges_from(windowed(reversed(toset)))

    # No cycles allowed
    if not nx.is_directed_acyclic_graph(graph): #TODO could rely on NetworkXUnfeasible https://networkx.github.io/documentation/networkx-1.9/reference/generated/networkx.algorithms.dag.topological_sort.html
        raise ValueError('Given tosets contradict each other')  # each cycle is a contradiction, e.g. a > b > c > a

    # Topological sort
    return setlist(nx.topological_sort(graph, reverse=True))
