# Copyright (C) 2016 VIB/BEG/UGent - Tim Diels <timdiels.m@gmail.com>
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
Test pytil.observable
'''

from pytil import observable
import pytest

class TestSet(object):

    @pytest.fixture
    def listener(self, mocker):
        return mocker.Mock()

    @pytest.fixture
    def set_(self, listener):
        set_ = observable.Set()
        set_.change_listeners.append(listener)
        return set_

    def test_construction(self):
        assert observable.Set() == set()
        assert observable.Set({5}) == {5}
        assert observable.Set([5, 5]) == {5}
        assert observable.Set((5, 5, 2)) == {5, 2}

    def test_add(self, set_, listener):
        # when adding new element, notify
        set_.add(5)
        assert set_ == {5}
        listener.assert_called_once_with(added=frozenset({5}), removed=frozenset())
        listener.reset_mock()

        # when adding existing, ignore
        set_.add(5)
        assert set_ == {5}
        listener.assert_not_called()

    def test_update(self, set_, listener):
        set_.update({1, 2, 3})
        assert set_ == {1, 2, 3}
        listener.assert_called_once_with(added=frozenset({1,2,3}), removed=frozenset())
        listener.reset_mock()

        set_.update({3, 4, 5})
        assert set_ == {1, 2, 3, 4, 5}
        listener.assert_called_once_with(added=frozenset({4, 5}), removed=frozenset())
        listener.reset_mock()

    def test_update_op(self, set_, listener):
        set_ |= {1, 2, 3}
        assert set_ == {1, 2, 3}
        listener.assert_called_once_with(added=frozenset({1,2,3}), removed=frozenset())
        listener.reset_mock()

        set_ |= {3, 4, 5}
        assert set_ == {1, 2, 3, 4, 5}
        listener.assert_called_once_with(added=frozenset({4, 5}), removed=frozenset())
        listener.reset_mock()

    def test_intersection(self, set_, listener):
        # setup
        set_ |= {1, 2}
        listener.reset_mock()

        # test
        set_.intersection_update({2, 3})
        assert set_ == {2}
        listener.assert_called_once_with(added=frozenset(), removed=frozenset({1}))
        listener.reset_mock()

    def test_intersection_op(self, set_, listener):
        # setup
        set_ |= {1, 2}
        listener.reset_mock()

        # test
        set_ &= {2, 3}
        assert set_ == {2}
        listener.assert_called_once_with(added=frozenset(), removed=frozenset({1}))
        listener.reset_mock()

    def test_difference(self, set_, listener):
        # setup
        set_ |= {1, 2, 3}
        listener.reset_mock()

        # test
        set_.difference_update({2, 3})
        assert set_ == {1}
        listener.assert_called_once_with(added=frozenset(), removed=frozenset({2, 3}))
        listener.reset_mock()

    def test_difference_op(self, set_, listener):
        # setup
        set_ |= {1, 2, 3}
        listener.reset_mock()

        # test
        set_ -= {2, 3}
        assert set_ == {1}
        listener.assert_called_once_with(added=frozenset(), removed=frozenset({2, 3}))
        listener.reset_mock()

    def test_symmetric_difference(self, set_, listener):
        # setup
        set_ |= {1, 2}
        listener.reset_mock()

        # test
        set_.symmetric_difference_update({2, 3})
        assert set_ == {1, 3}
        listener.assert_called_once_with(added=frozenset({3}), removed=frozenset({2}))
        listener.reset_mock()

    def test_symmetric_difference_op(self, set_, listener):
        # setup
        set_ |= {1, 2}
        listener.reset_mock()

        # test
        set_ ^= {2, 3}
        assert set_ == {1, 3}
        listener.assert_called_once_with(added=frozenset({3}), removed=frozenset({2}))
        listener.reset_mock()

    def test_remove(self, set_, listener):
        # setup
        set_ |= {1, 2}
        listener.reset_mock()

        # test
        set_.remove(2)
        assert set_ == {1}
        listener.assert_called_once_with(added=frozenset(), removed=frozenset({2}))
        listener.reset_mock()

    def test_discard(self, set_, listener):
        # setup
        set_ |= {1, 2}
        listener.reset_mock()

        # when discarding existing, notify
        set_.discard(2)
        assert set_ == {1}
        listener.assert_called_once_with(added=frozenset(), removed=frozenset({2}))
        listener.reset_mock()

        # when discarding missing, ignore
        set_.discard(5)
        listener.assert_not_called()
        listener.reset_mock()

    def test_pop(self, set_, listener):
        # setup
        set_ |= {1}
        listener.reset_mock()

        # test
        assert set_.pop() == 1
        assert set_ == set()
        listener.assert_called_once_with(added=frozenset(), removed=frozenset({1}))
        listener.reset_mock()

    def test_clear(self, set_, listener):
        # setup
        set_ |= {1, 2}
        listener.reset_mock()

        # test
        set_.clear()
        assert set_ == set()
        listener.assert_called_once_with(added=frozenset(), removed=frozenset({1, 2}))
        listener.reset_mock()

    def test_rollback(self, set_, listener):
        '''
        When a listener returns False, rollback the change and don't notify any other listeners
        '''
        # setup
        set_.add(1)
        listener.reset_mock()

        def on_changed(added, removed):
            raise Exception()
        set_.change_listeners.insert(0, on_changed)

        # test add
        with pytest.raises(Exception):
            set_.add(5)
        assert set_ == {1}
        listener.assert_not_called()

        # test remove
        with pytest.raises(Exception):
            set_.remove(1)
        assert set_ == {1}
        listener.assert_not_called()
