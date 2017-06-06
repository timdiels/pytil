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
Test chicken_turtle_util.algorithms
'''

import pytest
import numpy as np
from chicken_turtle_util.algorithms import spread_points_in_hypercube, multi_way_partitioning
from scipy.spatial.distance import euclidean
from itertools import product
from collections_extended import bag, frozenbag

class TestSpreadPointsInHypercube(object):

    def test_invalid_point_count(self):
        '''When point_count < 0, ValueError'''
        with pytest.raises(ValueError):
            spread_points_in_hypercube(point_count=-1, dimension_count=1)

    def test_invalid_dimension_count(self):
        '''When dimension_count < 1, ValueError'''
        with pytest.raises(ValueError):
            spread_points_in_hypercube(point_count=1, dimension_count=-1)

    @pytest.mark.parametrize('dims', range(1,5))    
    def test_no_points(self, dims):
        '''When point_count = 0, returns empty np.array, regardless of dimension_count'''
        assert np.array_equal(spread_points_in_hypercube(point_count=0, dimension_count=dims), np.empty(shape=(0,dims)))

    @pytest.mark.parametrize('dims', range(1,5))    
    def test_one_point(self, dims):
        '''When point_count = 1, it should lay in the hypercube'''
        points = spread_points_in_hypercube(point_count=1, dimension_count=dims)
        assert np.all((points >= 0) & (points <= 1))

    @pytest.mark.parametrize('point_count,dim_count', product((2,5,10,30), range(1,5)))    
    def test_happy_days(self, point_count, dim_count):
        '''When any other input, perform at least as well as a hypergrid layout of points'''
        points = spread_points_in_hypercube(point_count=point_count, dimension_count=dim_count)
        assert points.shape == (point_count, dim_count)

        # points must lay in the hypercube
        assert np.all((points >= 0) & (points <= 1))

        # actual min distance >= min distance in a hypergrid 
        min_distance = min(euclidean(points[i], points[j]) for i in range(point_count) for j in range(i+1, point_count))
        points_per_side = np.ceil(point_count ** (1/dim_count))
        hypergrid_min_distance = 1 / (points_per_side - 1)
        assert min_distance > hypergrid_min_distance or np.isclose(min_distance, hypergrid_min_distance)         

        # Note: alternatively we could test that relative error stays within
        # some constant, relative to the ideal solution (found through brute force)

class TestMultiWayPartitioning(object):

    # From http://stackoverflow.com/a/18354471/1031434
    def _groups(self, list_, group_count):
        if list_:
            prev = None
            for t in self._groups(list_[1:], group_count):
                tup = sorted(t)
                if tup != prev:
                    prev = tup
                    for i in range(group_count):
                        yield tup[:i] + [[list_[0]] + tup[i],] + tup[i+1:]
        else:
            yield [[] for _ in range(group_count)]

    def _multi_way_partitioning_brute_force(self, items, bin_count):
        '''Brute force that generates ideal solution'''
        assert bin_count > 1
        best_bins = [items, []*(bin_count-1)]
        best_diff = np.inf
        for bins in self._groups(items, bin_count):
            diff= self.get_distance(bins)
            if diff < best_diff:
                best_bins = bins
                best_diff = diff
        return best_bins

    def get_distance(self, bins):
        sums = set()
        for bin_ in bins:
            sums.add(sum(weight for _, weight in bin_))
        return max(sums) - min(sums)

    def reapply_weights(self, items, bins):
        weights = dict(items)
        return [[(x, weights[x]) for x in bin_] for bin_ in bins]

    def generate_test_data(self):
        items = list(enumerate(list(range(1,4))*20))
        params = list(product((2,5,10,12), range(2,6)))
        params = [(items[:item_count], bin_count) for item_count, bin_count in params]
        solutions = []
        for items, bin_count in params:
            bins = self._multi_way_partitioning_brute_force(items, bin_count)
            distance = self.get_distance(bins)
            solutions.append((items, bin_count, distance))
            print('+', end='', flush=True)
        print()
        print(repr(solutions))

    def test_invalid_bin_count(self):
        '''When bin_count < 1, ValueError'''
        with pytest.raises(ValueError):
            multi_way_partitioning({(1,2)}, bin_count=0)

    def test_no_items(self):
        '''When no items, return empty bins'''
        assert multi_way_partitioning([], bin_count=2) == bag([frozenbag(), frozenbag()])

    def test_one_item(self):
        '''When one item, return 1 singleton and x empty bins'''
        assert multi_way_partitioning([(1,2)], bin_count=2) == bag([frozenbag([1]), frozenbag()])

    def test_one_bin(self):
        '''When one bin, return single bin containing all items'''
        assert multi_way_partitioning([(1,2), (2,3)], bin_count=1) == bag([frozenbag([1,2])])

    params=[([(0, 1), (1, 2)], 2, 1), ([(0, 1), (1, 2)], 3, 2), ([(0, 1), (1, 2)], 4, 2), ([(0, 1), (1, 2)], 5, 2), ([(0, 1), (1, 2), (2, 3), (3, 1), (4, 2)], 2, 1), ([(0, 1), (1, 2), (2, 3), (3, 1), (4, 2)], 3, 0), ([(0, 1), (1, 2), (2, 3), (3, 1), (4, 2)], 4, 1), ([(0, 1), (1, 2), (2, 3), (3, 1), (4, 2)], 5, 2), ([(0, 1), (1, 2), (2, 3), (3, 1), (4, 2), (5, 3), (6, 1), (7, 2), (8, 3), (9, 1)], 2, 1), ([(0, 1), (1, 2), (2, 3), (3, 1), (4, 2), (5, 3), (6, 1), (7, 2), (8, 3), (9, 1)], 3, 1), ([(0, 1), (1, 2), (2, 3), (3, 1), (4, 2), (5, 3), (6, 1), (7, 2), (8, 3), (9, 1)], 4, 1), ([(0, 1), (1, 2), (2, 3), (3, 1), (4, 2), (5, 3), (6, 1), (7, 2), (8, 3), (9, 1)], 5, 1), ([(0, 1), (1, 2), (2, 3), (3, 1), (4, 2), (5, 3), (6, 1), (7, 2), (8, 3), (9, 1), (10, 2), (11, 3)], 2, 0), ([(0, 1), (1, 2), (2, 3), (3, 1), (4, 2), (5, 3), (6, 1), (7, 2), (8, 3), (9, 1), (10, 2), (11, 3)], 3, 0), ([(0, 1), (1, 2), (2, 3), (3, 1), (4, 2), (5, 3), (6, 1), (7, 2), (8, 3), (9, 1), (10, 2), (11, 3)], 4, 0), ([(0, 1), (1, 2), (2, 3), (3, 1), (4, 2), (5, 3), (6, 1), (7, 2), (8, 3), (9, 1), (10, 2), (11, 3)], 5, 1)]
    @pytest.mark.parametrize('items,bin_count,ideal_distance', params)
    def test_happy_days(self, items, bin_count, ideal_distance):
        '''When any other input, ...'''
        bins = multi_way_partitioning(items, bin_count)

        # Fill as many bins as possible
        assert bins.count(frozenbag()) == max(bin_count - len(items), 0)

        # Relative error to ideal solution should be acceptable
        actual_distance = self.get_distance(self.reapply_weights(items, bins))
        assert actual_distance >= (ideal_distance - 1e8), 'bug in test'
        assert actual_distance <= 1.3 * ideal_distance

        # TODO could use more varied input

# TestMultiWayPartitioning().generate_test_data()
