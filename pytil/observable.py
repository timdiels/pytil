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
Observable collections. Only contains `Set` currently.
'''

from contextlib import contextmanager

class Set(set):

    '''
    Observable set
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._change_listeners = []
        self._watching = False

    @property
    def change_listeners(self):
        '''
        Get change listeners

        Each change listener is called immediately after a mutating operation
        that actually changed the set. E.g. redundant additions are ignored.

        Returns
        -------
        [(added :: frozenset, removed :: frozenset) -> bool or None]
            List of change listeners. `added` are the items that were added,
            `removed` contains the items that were removed. Note: Items can be
            added and removed from a set in a single operation. When a listener
            raises, the change is rolled back without further notification.
        '''
        return self._change_listeners

    @contextmanager
    def _notify_if_changed(self):
        if self._watching:
            yield
            return
        else:
            try:
                self._watching = True
                original = self.copy()
                yield
                added = self - original
                removed = original - self
                if added or removed:
                    added = frozenset(added)
                    removed = frozenset(removed)
                    for listener in self._change_listeners:
                        try:
                            listener(added=added, removed=removed)
                        except Exception as ex:
                            self -= added
                            self |= removed
                            raise ex
            finally:
                self._watching = False

    def add(self, item):
        with self._notify_if_changed():
            super().add(item)

    def discard(self, item):
        with self._notify_if_changed():
            super().discard(item)

    def update(self, *args):
        with self._notify_if_changed():
            super().update(*args)

    def __ior__(self, *args):
        with self._notify_if_changed():
            return super().__ior__(*args)

    def intersection_update(self, *args):
        with self._notify_if_changed():
            super().intersection_update(*args)

    def __iand__(self, *args):
        with self._notify_if_changed():
            return super().__iand__(*args)

    def difference_update(self, *args):
        with self._notify_if_changed():
            super().difference_update(*args)

    def __isub__(self, *args):
        with self._notify_if_changed():
            return super().__isub__(*args)

    def symmetric_difference_update(self, other):
        with self._notify_if_changed():
            super().symmetric_difference_update(other)

    def __ixor__(self, *args):
        with self._notify_if_changed():
            return super().__ixor__(*args)

    def remove(self, elem):
        with self._notify_if_changed():
            super().remove(elem)

    def pop(self):
        with self._notify_if_changed():
            return super().pop()

    def clear(self):
        with self._notify_if_changed():
            super().clear()

# Potential future additions http://code.activestate.com/recipes/306864-list-and-dictionary-observer/
