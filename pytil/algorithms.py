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

from collections_extended import frozenbag, setlist
from more_itertools import windowed
import networkx as nx

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
