Changelog
=========
`Semantic versioning <semver_>`_ is used (starting with v3.0.0).

6.0.0
-----
- Backwards incompatible changes:

  - Remove ``asyncio.stubborn_gather``: More often than not, when you need this,
    you should look into a full blown pipeline framework such as Nextflow
    instead.

  - Remove ``click.assert_runs``:  It is usually simpler to use pytest's
    isolation and output capturing than to use this function

  - Remove ``click.argument``: Click's arguments are required by default, you
    can simply use the real click.argument directly.

  - Remove ``dict.assign``: Esoteric and easily replaced by: ``destination.clear();
    destination.update(source)``.

  - Remove ``function.compose``: Compose can be found in other PyPI packages,
    e.g. in Toolz: ``toolz.functoolz.compose``.

  - Remove ``http.download``: `urllib.request.urlretrieve` can be used instead,
    though the filename suggested by the server is not used. Only the extension of
    the downloaded file will match that of the server.

  - Remove ``inspect.call_args``: Esoteric, can achieve something very
    similar with::

        args = inspect.signature(f).bind_partial(*args, **kwargs)
        args.apply_defaults()
        dict(args.arguments)

  - Remove ``iterable.sliding_window``: Use `more_itertools.windowed` instead.
    Drop in replacement.

  - Remove ``iterable.partition``: If your data is sorted by key, you can just
    use `itertools.groupby` as drop in replacement. Else, you can use
    ``toolz.itertoolz.groupby``, but arg order is swapped and element order may not be
    preserved.

  - Remove ``iterable.flatten``: Use `more_itertools.collapse` instead.
    ``flatten(a, b)`` becomes ``collapse(a, levels=b)``.

  - Remove ``path.write``: Use `pathlib.Path.write_text` instead. However, you
    are now responsible for creating any missing ancestor directories
    (`os.makedirs`). The use of mode can be replaced by ``p.touch();
    p.chmod(mode); p.write_text()`` or a variation depending on your use case.

  - Remove ``path.read``: Use `pathlib.Path.read_text` instead.

  - Remove ``pymysql.patch``: Instead of globally patching it, use the ``conv``
    argument when creating a pymysql Connection.

  - `algorithms.multi_way_partitioning` now returns a frozenbag instead of a bag.

  - `multi_dict.MultiDict.invert` now returns a MultiDict instead of a dict.

- Enhancements/additions:

  - Add `difflib.line_diff`
  - Add `numpy.ArrayLike`
  - Add `path.TemporaryDirectory`
  - Add `path.is_descendant`
  - Add `path.is_descendant_or_self`
  - Add `path.sorted_lines`
  - Add `path.tsv_lines`
  - Add `pkg_resources.resource_copy`
  - Add `test.assert_dir_unchanged`
  - Add `test.assert_lines_equal`
  - Add `test.assert_xml_equals`
  - Add `test.reset_loggers`
  - `test.assert_text_equals`: Show diff when not equal

- Fixes:

  - Fix package: Add missing data files and dependencies
  - Fix formatting of `test.assert_matches`, `test.assert_search_matches`:
    forgot newline after ``Actual:``

5.0.0
-----

Major backwards incompatible change: Renamed root package, pypi name and
project to pytil.

4.1.2
-----
Announce rename to pytil.

4.1.1
-----
- Fixes:

  - add missing keys to ``extras_require``: ``hashlib``, ``multi_dict``,
    ``test``

4.1.0
-----
- Backwards incompatible changes: None

- Enhancements/additions:

  - ``click.assert_runs``: pass on extra args to click's ``invoke()``
  - ``path.chmod``, ``path.remove``: ignore disappearing children instead of
    raising
  - Add ``exceptions.exc_info``: exc_info tuple as seen in function parameters
    in the ``traceback`` standard module
  - Add ``extras_require['all']`` to ``setup.py``: union of all extra
    dependencies

- Fixes:

  - ``path.chmod``: do not follow symlinks
  - ``iterable.flatten``: removed debug prints: ``+``, ``-``

- Internal / implementation details:

  - use simple project structure instead of Chicken Turtle Project
  - ``pytest-catchlog`` instead of ``pytest-capturelog``
  - ``extras_require['dev']``: test dependencies were missing
  - ``test_http`` created ``existing_file`` in working dir instead of in test
    dir

v4.0.1
------
- Fixed: README formatting error

v4.0.0
------
- Major:

  - ``path.digest`` renamed to ``path.hash`` (and added ``hash_function`` parameter)
  - renamed ``cli`` to ``click``
  - require Python 3.5 or newer
  - Changed: ``asyncio.stubborn_gather``:

    - raise ``CancelledError`` if all its awaitables raised ``CancelledError``.
    - raise summary exception if any awaitable raises exception other than
      ``CancelledError``
    - log exceptions, as soon as they are raised

- Minor:

  - Added:

    - ``click.assert_runs``
    - ``hashlib.base85_digest``
    - ``logging.configure``
    - ``path.assert_equals``
    - ``path.assert_mode``
    - ``test.assert_matches``
    - ``test.assert_search_matches``
    - ``test.assert_text_contains``
    - ``test.assert_text_equals``

- Fixes:

  - ``path.remove``: raised when ``path.is_symlink()`` or contains a symlink
  - ``path.digest/hash``: directory hash collisions were more likely than necessary
  - ``pymysql.patch``: change was not picked up in recent pymysql versions

v3.0.1
------
- Fixed: README formatting error

v3.0.0
------

- Removed: 

  - ``cli.Context``, ``cli.BasicsMixin``, ``cli.DatabaseMixin``,
    ``cli.OutputDirectoryMixin``
  - ``pyqt`` module
  - ``URL_MAX_LENGTH``
  - ``various`` module: ``Object``, ``PATH_MAX_LENGTH``

- Enhanced:

  - ``data_frame.split_array_like``: ``columns`` defaults to ``df.columns``
  - ``sqlalchemy.pretty_sql``: much better formatting

- Added:

  - ``algorithms.toset_from_tosets``: Create totally ordered set (toset) from
    tosets
  - ``configuration.ConfigurationLoader``: loads a single configuration from one
    or more files directory according to XDG standards
  - ``data_frame.assert_equals``: Assert 2 data frames are equal
  - ``data_frame.equals``: Get whether 2 data frames are equal
  - ``dict.assign``: assign one dict to the other through mutations
  - ``exceptions.InvalidOperationError``: raise when an operation is
    illegal/invalid, regardless of the arguments you throw at it (in the
    current state).
  - ``inspect.call_args``: Get function call arguments as a single dict
  - ``observable.Set``: set which can be observed for changes
  - ``path.chmod``: change file or directory mode bits (optionally recursively)
  - ``path.digest``: Get SHA512 checksum of file or directory
  - ``path.read``: get file contents
  - ``path.remove``: remove file or directory (recursively), unless it's missing
  - ``path.write``: create or overwrite file with contents
  - ``series.assert_equals``: Assert 2 series are equal
  - ``series.equals``: Get whether 2 series are equal
  - ``series.split``: Split values
  - ``test.temp_dir_cwd``: pytest fixture that sets current working directory to
    a temporary directory

v2.0.4
------
No changelog

.. _semver: http://semver.org/spec/v2.0.0.html
