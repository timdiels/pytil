Chicken Turtle Util (CTU) is a broad scoped Python utility library.

Most dependencies are optional and grouped by module.  When using a module,
add/install its dependencies, listed in its corresponding ``*_requirements.in``
file found in the root of the project; e.g.  `cli_requirements.in`__ lists the
dependencies of `chicken_turtle_util.cli`.

.. __: https://github.com/timdiels/chicken_turtle_util/blob/master/cli_requirements.in

Links
=====
- `Documentation <http://pythonhosted.org/chicken_turtle_util/>`_
- `PyPI <https://pypi.python.org/pypi/chicken_turtle_util/>`_
- `GitHub <https://github.com/timdiels/chicken_turtle_util/>`_

API stability
=============
While all features are documented and tested, the API is changed frequently.
When doing so, the `major version <semver_>`_ is bumped and a changelog is kept
to help upgrade. Fixes will not be backported. It is recommended to pin the
major version in your setup.py, e.g. for 2.x.y::

    install_requires = ['chicken_turtle_util>=2.0.0,<3.0.0', ...]

If you see something you like but need long term stability (e.g. if low
maintenance cost is required), request to have it moved to a stable library
(one with fewer major releases) by `opening an issue`_.

.. _opening an issue: https://github.com/timdiels/chicken_turtle_util/issues

Changelog
=========

`Semantic versioning <semver_>`_ is used (starting with v3.0.0).

v4.0.1
------
- Fixed: README formatting error

v4.0.0
------
- Major:

  - `path.digest` renamed to `path.hash` (and added `hash_function` parameter)
  - renamed `cli` to `click`
  - require Python 3.5 or newer
  - Changed: `asyncio.stubborn_gather`:

    - raise `CancelledError` if all its awaitables raised `CancelledError`.
    - raise summary exception if any awaitable raises exception other than
      `CancelledError`
    - log exceptions, as soon as they are raised

- Minor:

  - Added:

    - `click.assert_runs`
    - `hashlib.base85_digest`
    - `logging.configure`
    - `path.assert_equals`
    - `path.assert_mode`
    - `test.assert_matches`
    - `test.assert_search_matches`
    - `test.assert_text_contains`
    - `test.assert_text_equals`

- Fixes:

  - `path.remove`: raised when ``path.is_symlink()`` or contains a symlink
  - `path.digest/hash`: directory hash collisions were more likely than necessary
  - `pymysql.patch`: change was not picked up in recent pymysql versions

v3.0.1
------
- Fixed: README formatting error

v3.0.0
------

- Removed: 

  - `cli.Context`, `cli.BasicsMixin`, `cli.DatabaseMixin`,
    `cli.OutputDirectoryMixin`
  - `pyqt` module
  - `URL_MAX_LENGTH`
  - `various` module: `Object`, `PATH_MAX_LENGTH`

- Enhanced:

  - `data_frame.split_array_like`: `columns` defaults to ``df.columns``
  - `sqlalchemy.pretty_sql`: much better formatting

- Added:

  - `algorithms.toset_from_tosets`: Create totally ordered set (toset) from
    tosets
  - `configuration.ConfigurationLoader`: loads a single configuration from one
    or more files directory according to XDG standards
  - `data_frame.assert_equals`: Assert 2 data frames are equal
  - `data_frame.equals`: Get whether 2 data frames are equal
  - `dict.assign`: assign one dict to the other through mutations
  - `exceptions.InvalidOperationError`: raise when an operation is
    illegal/invalid, regardless of the arguments you throw at it (in the
    current state).
  - `inspect.call_args`: Get function call arguments as a single dict
  - `observable.Set`: set which can be observed for changes
  - `path.chmod`: change file or directory mode bits (optionally recursively)
  - `path.digest`: Get SHA512 checksum of file or directory
  - `path.read`: get file contents
  - `path.remove`: remove file or directory (recursively), unless it's missing
  - `path.write`: create or overwrite file with contents
  - `series.assert_equals`: Assert 2 series are equal
  - `series.equals`: Get whether 2 series are equal
  - `series.split`: Split values
  - `test.temp_dir_cwd`: pytest fixture that sets current working directory to
    a temporary directory

v2.0.4
------
No changelist

.. _semver: http://semver.org/spec/v2.0.0.html
