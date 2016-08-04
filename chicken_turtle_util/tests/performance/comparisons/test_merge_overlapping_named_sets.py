# Copyright (C) 2015 VIB/BEG/UGent - Tim Diels <timdiels.m@gmail.com>
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
Performance tests of implementations for `merge_overlapping_named_sets`.

Most implementations and come from: http://stackoverflow.com/questions/9110837/python-simple-list-merging-based-on-intersections/9112588 
'''

# XXX some of the implementation has lagged behind on the rest of CTU
# development and no longer works

import pytest
import pandas as pd
import networkx as nx
import numpy as np
from chicken_turtle_util.iterable import sliding_window
from collections import deque
from more_itertools.more import first
import itertools
import heapq
from itertools import chain
import random
from _collections import defaultdict
import re


########################################
# Implementations

def niklas(lsts):
    sets = [set(lst) for lst in lsts if lst]
    merged = 1
    while merged:
        merged = 0
        results = []
        while sets:
            common, rest = sets[0], sets[1:]
            sets = []
            for x in rest:
                if x.isdisjoint(common):
                    sets.append(x)
                else:
                    merged = 1
                    common |= x
            results.append(common)
        sets = results
    return sets

def agf(lists):
    '''
    Fails on: http://pastebin.com/c83VyCMH
    '''
    sets = deque(set(lst) for lst in lists if lst)
    results = []
    disjoint = 0
    current = sets.pop()
    while True:
        merged = False
        newsets = deque()
        for _ in range(disjoint, len(sets)):
            this = sets.pop()
            if not current.isdisjoint(this):
                current.update(this)
                merged = True
                disjoint = 0
            else:
                newsets.append(this)
                disjoint += 1
        if sets:
            newsets.extendleft(sets)
        if not merged:
            results.append(current)
            try:
                current = newsets.pop()
            except IndexError:
                break
            disjoint = 0
        sets = newsets
    return results

def agf2(lists):
    newsets, sets = [set(lst) for lst in lists if lst], []
    while len(sets) != len(newsets):
        sets, newsets = newsets, []
        for aset in sets:
            for eachset in newsets:
                if not aset.isdisjoint(eachset):
                    eachset.update(aset)
                    break
            else:
                newsets.append(aset)
    return newsets

# TODO try optimise alexis?
# TODO use alexis' alg, but assume the input is list of set of any, input list is modified in place
class Alexis():
        
    def alexis(self, data):
        bins = list(range(len(data)))  # Initialize each bin[n] == n
        nums = dict()
    
        data = [set(m) for m in data ]  # Convert to sets    
        for r, row in enumerate(data):
            for num in row:
                if num not in nums:
                    # New number: tag it with a pointer to this row's bin
                    nums[num] = r
                    continue
                else:
                    dest = self.locatebin(bins, nums[num])
                    if dest == r:
                        continue # already in the same bin
    
                    if dest > r:
                        dest, r = r, dest   # always merge into the smallest bin
    
                    data[dest].update(data[r]) 
                    data[r] = None
                    # Update our indices to reflect the move
                    bins[r] = dest
                    r = dest 
    
        # Filter out the empty bins
        have = [ m for m in data if m ]
        return have
    
    def locatebin(self, bins, n):
        """
        Find the bin where list n has ended up: Follow bin references until
        we find a bin that has not moved.
        """
        while bins[n] != n:
            n = bins[n]
        return n
    
alexis = Alexis().alexis

def ecatmur(data):
    parents = {}
    def find(i):
        j = parents.get(i, i)
        if j == i:
            return i
        k = find(j)
        if k != j:
            parents[i] = k
        return k
    for l in filter(None, data):
        parents.update(dict.fromkeys(map(find, l), find(l[0])))
    merged = {}
    for k, v in parents.items():
        merged.setdefault(find(v), []).append(k)
    return merged.values()

def robert_king(lists):
    '''
    Fails on: http://pastebin.com/5XED11fX
    '''
    for l in lists:
        l.sort()
    one_list = heapq.merge(*[list(zip(l,[i]*len(l))) for i,l in enumerate(lists)]) #iterating through one_list takes 25 seconds!!
    previous = next(one_list)

    d = {i:i for i in range(len(lists))}
    for current in one_list:
        if current[0]==previous[0]:
            d[current[1]] = d[previous[1]]
        previous=current

    groups=[[] for i in range(len(lists))]
    for k in d:
        groups[d[k]].append(lists[k]) #add a each list to its group

    return [set(chain(*g)) for g in groups if g] #since each subroup in each g is sorted, it would be faster to merge these subgroups removing duplicates along the way.

class Katrielalex(object):
    def pairs(self, lst):
        i = iter(lst)
        first = prev = item = next(i)
        for item in i:
            yield prev, item
            prev = item
        yield item, first
    
    def katrielalex(self, lists):
        g = nx.Graph()
        for sub_list in lists:
            for edge in self.pairs(sub_list):
                    g.add_edge(*edge)
        return list(nx.connected_components(g))
    
katrielalex = Katrielalex().katrielalex

def connected_components(sets):
    g = nx.Graph()
    for name, set_ in sets.items():
        for item in set_:
            g.add_edge((item, True), (name, False))  # tried add_edges_from, but it was actually slower
    components = (bifilter_tuples(c) for c in nx.connected_components(g)) #TODO bifilter used to be part of chicken_turtle_util.itertools, not anymore
    return {frozenset(names) : items for items, names in components}

def connected_components2(sets):
    g = nx.Graph()
    sets = {k:v for k,v in sets.items() if v}
    g.add_nodes_from(sets.keys())
    for x, y in sliding_window(sorted((item, name) for name, set_ in sets.items() for item in set_)):
        if x[0] == y[0]:
            g.add_edge(x[1], y[1])
    return {frozenset(component) : set.union(*(set(sets[name]) for name in component)) for component in nx.connected_components(g)}

def steabert(lsts):
    # this is an index list that stores the joined id for each list
    joined = list(range(len(lsts)))
    # create an ordered list with indices
    indexed_list = sorted((el,index) for index,lst in enumerate(lsts) for el in lst)
    # loop throught the ordered list, and if two elements are the same and
    # the lists are not yet joined, alter the list with joined id
    el_0,idx_0 = None,None
    for el,idx in indexed_list:
            if el == el_0 and joined[idx] != joined[idx_0]:
                    old = joined[idx]
                    rep = joined[idx_0]
                    joined = [rep if id_ == old else id_ for id_ in joined]
            el_0, idx_0 = el, idx
    
    # Addition to steabert's answer to return actual lists
    lsts = list(map(set, lsts))
    result = []
    for i, j in enumerate(joined):
        if i == j:
            result.append(lsts[i])
        else:
            lsts[j] |= lsts[i]

    return result

def rik_poggi(data):
    sets = (set(e) for e in data if e)
    results = [next(sets)]
    for e_set in sets:
        to_update = []
        for i,res in enumerate(results):
            if not e_set.isdisjoint(res):
                to_update.insert(0,i)

        if not to_update:
            results.append(e_set)
        else:
            last = results[to_update.pop(-1)]
            for i in to_update:
                last |= results[i]
                del results[i]
            last |= e_set
    return results

def chessmaster(mylists):
    results, sets = [], [set(lst) for lst in mylists if lst]
    upd, isd, pop = set.update, set.isdisjoint, sets.pop
    while sets:
        if not [upd(sets[0],pop(i)) for i in range(len(sets)-1,0,-1) if not isd(sets[0],sets[i])]:
            results.append(pop(0))
    return results

def chrismit(starting_list):
    '''
    Fails on: http://pastebin.com/3q2t8kRK
    '''
    final_list = []
    for i,v in enumerate(starting_list[:-1]):
        if set(v) & set(starting_list[i+1]):
            starting_list[i+1].extend(list(set(v) - set(starting_list[i+1])))
        else:
            final_list.append(v)
    final_list.append(starting_list[-1])
    return final_list

################################
# Test data

# TODO this func so useful that it needs documentation and should be added to test.util
# XXX not using the right mean in dists (though still kind of in the right direction currently) 
def create_input(overlap, list_size_distribution, list_size_mean, set_count):
    # create without overlap
    min_ = 1
    max_ = 2 * list_size_mean - min_
    if list_size_distribution == 'constant':  # 1 list size
        list_sizes = np.full(set_count, list_size_mean, dtype=int)
    elif list_size_distribution == 'uniform':  # all sizes equally possible
        list_sizes = np.random.random_integers(min_, max_, set_count)
    elif list_size_distribution == 'left_triangular':  # more small lists
        list_sizes = np.random.triangular(min_, min_, max_, set_count).round()
    elif list_size_distribution == 'right_triangular':  # more large lists
        list_sizes = np.random.triangular(min_, max_, max_, set_count).round()
    else:
        assert False
    indices = np.insert(list_sizes.astype(int).cumsum(), 0, 0)
    sets = [set(range(start, end)) for start, end in sliding_window(indices)]
    
    # add overlap, with a skip every so often
    overlap_to_create = round(set_count * overlap)
    i = 0
    def get_next_skip_distance():
        return round(np.random.standard_exponential()) + 1
    next_skip = get_next_skip_distance()
    expected_output = []
    current_overlap = sets[0]
    overlap_to_create -= 1
    while overlap_to_create > 0:
        if i == next_skip and i < len(sets)-1 and overlap_to_create >= 2:
            # start new family of overlapping sets
            i += 1
            overlap_to_create -= 1
            expected_output.append(current_overlap)
            current_overlap = sets[i]
            next_skip = i + get_next_skip_distance()
        # create overlap
        sets[i+1].pop()
        sets[i+1].add(first(sets[i]))
        overlap_to_create -= 1
        current_overlap = current_overlap | sets[i+1]
        i += 1
    else:
        expected_output.append(current_overlap)
    expected_output.extend(sets[i+1:])
        
    # final things
    sets = [list(x) for x in sets]
    random.shuffle(sets)
    
    # debug info of this func
#     print()
#     print('{} overlap, {} set sizes with mean {}, {} sets'.format(overlap, list_size_distribution, list_size_mean, set_count))
#     print(pd.Series(len(x) for x in sets).describe())
#     
#     overlap = 1 - len(expected_output)/len(sets)
#     print('{:.2}% of sets removed due to overlap'.format(overlap))  # Note this is only a rough under-estimate of actual number of sets overlapping
    
    return sets, expected_output

def create_input_args():
    overlaps = np.array([0, .01, .03, .05, .25, .50, .75, 1])
    distributions = 'constant uniform left_triangular right_triangular'.split() 
    list_size_means = [2, 10, 100, 500]
    set_counts = [100, 1000, 3000]
    return [args for args in
        itertools.product(overlaps, distributions, list_size_means, set_counts)
        if args[2] * args[3] < 30000
    ]
_input_args = create_input_args()

@pytest.fixture(scope='session', params=_input_args, ids=_input_args)
def input_(request):
    return create_input(*request.param)

def as_unnamed(alg):
    def unnamed_alg(sets):
        named = {'n{}'.format(i) : x for i, x in enumerate(sets)}
        return alg(named).values()
    return unnamed_alg

_algs = dict(
#     niklas=niklas,
#     agf2=agf2,
    alexis=alexis,
#     ecatmur=ecatmur,
#     katrielalex=katrielalex,
#     connected_components_n=as_unnamed(connected_components),
#     connected_components2_n=as_unnamed(connected_components2), 
#     current_n=as_unnamed(merge_overlapping_named_sets),
#     rik_poggi=rik_poggi,
#     chessmaster=chessmaster,
#     steabert=steabert,
    # Broken for some inputs:
#     robert_king=robert_king,
#     agf=agf,
#     chrismit=chrismit,
)
@pytest.fixture(
    scope='session', 
    params=list(_algs.values()),
    ids=list(_algs.keys())
)
def alg(request):
    return request.param


#############################
# Test

@pytest.mark.skipif(True, reason='long test, only run on explicit request') # TODO condition is skipif not marked current
# @pytest.mark.current
@pytest.mark.timeout(10)
class TestMergeOverlappingPerformance(object):
    
    '''
    Test performance of implementations of `merge_overlapping_named_sets` minus the named aspect
    '''
    
    # Results from a last run: http://pastebin.com/raw/kttQR1Pt
    # Alexis' algorithm is faster than any other tested. robert_king, agf (first version only) and chrismit's algorithms were disqualified due to bugs. 
     
    def normalised(self, output):
        return sorted([sorted(list(x)) for x in output])
    
    def test_itt(self, alg, input_, benchmark):
        overlapping_sets, expected = input_
        merged = benchmark(alg, overlapping_sets)
        
#         print()
#         print(alg)
#         print(merged)
#         print('input = {}\nexpected = {}\nactual = {}'.format(
#             overlapping_sets,
#             expected,
#             merged
#         ))
#         print('sorted_input = {}\nsorted_expected = {}\nsorted_actual = {}'.format(
#             self.normalised(overlapping_sets),
#             self.normalised(expected),
#             self.normalised(merged)
#         ))
        
        assert self.normalised(merged) == self.normalised(expected)
        
# TODO either extract parser into util or figure out a way to get to the data from pytest-benchmark directly
def group_results():
    '''
    If having saved the output from a run of TestMergeOverlappingPerformance as merge_overlapping_sets_performance.log in the setup.py dir, this groups the results
    '''
    with open('merge_overlapping_sets_performance.log') as f:
        groups = defaultdict(list)
        
        # ad hoc parser
        is_prolog = True
        is_content = False
        performance_result_header = 'Name (time in us) Min Max Mean StdDev Median IQR Outliers(*) Rounds Iterations'.split()
        for line in f.readlines():
            if is_prolog:
                if line.split() == performance_result_header:
                    is_prolog = False
            elif not is_content:
                if line.startswith('-' * 40):
                    is_content = True
            else:
                if line.startswith('-' * 40):
                    break
                else:
                    # parse and group actual test line
                    line = re.match(r'.+\[(.+)-(.+)\](.+)', line)
                    groups[eval(line.group(2))].append((line.group(1), line.group(3)))
        
        # print grouped result
        for group, values in sorted(groups.items(), key=lambda x: (x[0][3], x[0][2], x[0][1], x[0][0])):
            print(group)
            print('\n'.join(['{} {}'.format(*x) for x in values]))
            print()
            
        # print detailed summary
        places = pd.DataFrame([(group, i, x[0]) for group, values in groups.items() for i, x in enumerate(values)], columns='group place alg'.split())
        print(places.groupby('alg')['place'].describe().to_string())
        print()
        
        # print percentage of times one alg was faster than the other
        def count_times_faster(places, alg1, alg2):
            return places.groupby('group').apply(lambda x: x[x['alg'] == alg1]['place'] < x[x['alg'] == alg2]['place']).sum() / len(places.groupby('group'))
        algs = list(sorted(_algs.keys()))
        times_faster = pd.DataFrame([[count_times_faster(places, alg1, alg2) for alg2 in algs] for alg1 in algs], index=algs, columns=algs)
        print('pct alg1 (rows) faster than alg2 (columns)')
        print(times_faster.to_string())
        print()
        
        # print real terse summary
        print(places.groupby('alg')['place'].mean().sort_values().to_string())
        print()
    
    
