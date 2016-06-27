Chicken Turtle Util (CTU) provides an API of various Python utility functions.

Chicken Turtle Util is alpha. None of the interface is stable (yet), meaning it
may change in the future.

Chicken Turtle Util offers a variety of features, as such we kept most
dependencies optional.  When using a module, add/install its dependencies,
listed in its corresponding ``*_requirements.in`` file found in the root of the
project; e.g.  `cli_requirements.in`__ lists the dependencies of
`chicken_turtle_util.cli`.

.. __: https://github.com/timdiels/chicken_turtle_util/blob/master/cli_requirements.in

Links
=====
- `Documentation <http://pythonhosted.org/chicken_turtle_util/>`_
- `PyPI <https://pypi.python.org/pypi/chicken_turtle_util/>`_
- `GitHub <https://github.com/timdiels/chicken_turtle_util/>`_

Features
========

- `algorithms.spread_points_in_hypercube`:

  Place `n` points in a unit hypercube such that the minimum distance between
  points is approximately maximal

- `algorithms.multi_way_partitioning`: Greedily divide weighted items equally
  across bins (multi-way partition problem)       

- `data_frame` and `series`: `pandas <http://pandas.pydata.org/>`_ utility functions

  - `data_frame.replace_na_with_none`: Replace `NaN` values in `DataFrame` with `None`
  - `data_frame.split_array_like`: Split cells with `array_like` values along row axis.
  - `series.invert`: Swap index with values of series

- `dict`: dictionary utilities:

  - `invert`: Invert dict by swapping each value with its key
  - `DefaultDict`: Like `collections.defaultdict`, but its value factory function takes a key argument, e.g. ``DefaultDict(lambda key: MyClass(key))``
  - `pretty_print_head`: Pretty print the 'first' lines of a dict

- `path`: `pathlib.Path` utilities, including an equivalent of `shutil.rmtree`
  which reliably works on NFS.

- `application`: Mixins for building application (context) classes
- `function.compose`: Compose functions
- `http.download`: Download http resource (using `requests`) and save to file name suggested by HTTP server
- `iterable.sliding_window`: Iterate using a sliding window
- `iterable.partition`: Split iterable into partitions
- `iterable.is_sorted`: Get whether iterable is sorted ascendingly
- `iterable.flatten`: Flatten shallowly zero or more times
- `configuration.ConfigurationLoader`: loads a single configuration from one or
  more files spread across /etc and XDG config directories.
- `set.merge_by_overlap`: Of a list of sets, merge those that overlap, in place
- `logging.set_level`: Context manager to temporarily change log level of logger
- `cli`: extensions to `click <http://click.pocoo.org/>`_
- `pyqt.block_signals`: Context manager to temporarily turn on `QObject.blockSignals`
- `sqlalchemy.log_sql`: Context manager to temporarily log sql statements emitted by `sqlalchemy <http://www.sqlalchemy.org/>`_
- `various.Object`: Like `object`, but does not raise given args to `__init__`

Changelist
==========

.. todo: add to overview

v2.1.0 (to be released)
-----------------------

- Moved all `Context` related objects from `cli` to `application`.
- Added `exceptions.InvalidOperationError`: raise when an operation is
  illegal/invalid, regardless of the arguments you throw at it (in the current
  state).
- Added `application.ConfigurationMixin`: application context mixin for loading a configuration
- Added `application.ConfigurationsMixin`: application context mixin for loading multiple configurations
- Added `configuration.ConfigurationLoader`: loads a single configuration from one or more files
- `application.Context`: `cli_options()` replaced by `command()`, which is more flexible
- Removed `application.command`. Use ``cli.Context.command()`` instead
- Added `application.DataDirectoryMixin`: application context mixin, provides data
  directory according to XDG standards
- Added `path.write`: create or overwrite file with contents
- Added `path.read`: get file contents
- Added `path.remove`: remove file or directory (recursively), unless it's missing
- Added `path.chmod`: change file or directory mode bits (optionally recursively)
- Added `test.temp_dir_cwd`: pytest fixture that sets current working directory to a temporary directory
- Added `dict.assign`: assign one dict to the other through mutations
- Added `inspect.function_call_repr`: Get `repr` of a function call
- Added `inspect.function_call_args`: Get function call arguments as a single dict

v2.0.4
------
No changelist
