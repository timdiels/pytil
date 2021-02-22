Changelog
=========
`Semantic versioning <semver_>`_ is used (starting with v3.0.0). At some point
the library was called Chicken Turtle Util instead.

8.0.0
-----
- Backwards incompatible changes:

  - Remove ``.data_frame.split_array_like``: use upstream ``df.explode``
    instead.

  - Rename ``.data_frame.equals`` to ``.data_frame.df_equals``.

  - Rename ``.data_frame.assert_equals`` to ``.data_frame.assert_df_equals``.

  - Remove ``.series.split``: use upstream ``series.explode`` instead.

  - Remove ``.data_frame.replace_na_with_none``: float columns would become the
    less efficient dtype=object if you used None instead of nan. While
    ``bool(np.nan) != bool(None)``, you can use ``pd.isna(value)`` and
    ``pd.notna``. In cases where None/np.nan do cause trouble downstream you
    could make things consistent by replacing None with nan
    ``df.fillna(np.nan)`` though likely you'll prefer some value more specific
    to what you're doing e.g. ``df.replace(np.nan, '')``; which replaces any NA
    value, including None.

  - Remove ``.logging.configure``: too project specific. Use logging directly
    instead.

  - Remove ``.logging.set_level``: only 1 or so project still uses this, just
    inline it into the project.

  - Remove ``.test.reset_loggers``: either mock anything that configures logging
    or when testing a CLI, call it in a subprocess. It might not be a problem
    anymore with today's pytest caplog.

  - Remove some ``.test.assert*``. Usually the default pytest reporting for
    these is good enough when straight up using ``assert``. If you do want
    different reporting it would be better to define
    ``pytest_assertrepr_compare`` instead.

    - Remove ``assert_text_equals``: use ``assert actual == expected``

    - Remove ``assert_text_contains(whole, part)``:
      use ``assert part in whole``

    - Remove ``assert_matches(actual, pattern, flags=0)``:
      use ``assert re.match(pattern, actual, flags)``

    - Remove ``assert_search_matches(actual, pattern, flags=0)``:
      use ``assert re.search(pattern, actual, flags)``

    - Remove ``assert_lines_equal``:
      use ``assert tuple(actual) == tuple(expected)``

  - Remove ``.test.assert_dir_equals``: too project specific / inflexible, e.g.
    do you care about line order in files or just want hashes to match...
    better to compare the contents yourself as then you can pick the right
    assert for ways to compare files. Copy it to your project instead.

  - Remove ``.test.assert_file_mode``: too project specific. Copy it instead.

  - Remove ``.test.assert_file_equals``: too project specific. Copy it instead.

  - Remove ``.algorithms.multiway_partitions``: copy it instead.

  - Remove ``.algorithms.toset_from_tosets``: copy it instead.

  - Remove ``.click.option`` and ``.click.password_option``: too project
    specific. Copy it instead.

  - Remove ``.configuration.ConfigurationLoader``: most projects can make do
    with pyxdg's ``load_first_config``, so no inheritance and the config does
    not provide defaults for the CLI. If you do need this, you can probably
    find a different library that does something similar or copy the old code.

  - Remove ``.debug.pretty_memory_info``: can probably be found in some other
    library or use a proper memory profiler.

  - Remove ``.dict.pretty_print_head``: too trivial, copy it instead.

  - Remove ``.dict.DefaultDict``: probably can be found elsewhere.

  - Remove ``.dict.invert``: might find it in some other library, probably
    better redesign your algorithm to avoid needing this in the first place.

  - Remove ``.multi_dict.MultiDict``: can be found in other libraries.

  - Remove ``.difflib.line_diff``: too project specific, copy it if you need
    that specific behaviour or use difflib directly or find a 3rd party
    library.

  - Remove ``.exceptions.exc_info``: too trivial, copy it into your project if
    needed

  - Remove ``.exceptions.UserException``: too project specific.

  - Remove ``.exceptions.InvalidOperationError``: too project specific.

  - Remove ``.hashlib.base85_digest``: too trivial, just copy it.

  - Remove ``.iterable.is_sorted``: surely this already exists in
    more_itertools, toolz.itertoolz or something.

  - Rename ``.numpy`` to ``.typing``

  - Remove ``.parse.tsv``, ``.parse.csv``: too project specific, copy it.

  - Remove ``.path.sorted_lines``: too project specific, copy it.

  - Remove ``.sqlalchemy.log_sql``: too trivial, copy it.

  - Remove ``.sqlalchemy.pretty_sql``: too trivial, copy it.

  - Remove ``.write.tsv``, ``.write.csv``: too project specific, copy it.

  - Rename ``.various.join_multiline`` to ``.various.join_lines``

  - Remove ``.pkg_resources.resource_path``: use importlib_resources instead;
    it is more convenient and supposedly faster. You'll have to wrap it in Path
    yourself.

  - Remove ``.pkg_resources.resource_copy``: this broke on python 3.8 (or
    earlier), it could be reimplemented with importlib_resources or better yet
    you could store a zip/tgz to avoid needing to copy a dir.

  - Rename ``.test.assert_xlsx_equals`` to ``.xlsx_compare.assert_xlsx_equals``
  - Rename ``.test.assert_xml_equals`` to ``.xml_compare.assert_xml_equals``


7.0.0
-----
- Backwards incompatible changes:

  - Remove ``path.tsv_lines``: use ``parse.tsv`` instead.

  - Remove ``algorithms.spread_points_in_hypercube``: it simply returned opints
    on a grid, which can be achieved with numpy.meshgrid, e.g. 3D grid::

        import numpy as np
        side = np.linspace(0, 1, ceil(n**(1/3)))
        points = np.array(np.meshgrid(side, side, side)).reshape(3,-1).T

  - Rename ``path.assert_mode`` to ``test.assert_file_mode``

  - Rename ``path.assert_equals`` to ``test.assert_file_equals``

- Enhancements/additions:

  - Add ``test.assert_dir_equals``
  - Add ``various.join_multiline``
  - Add ``test.assert_xlsx_equals``
  - Add ``parse.csv``
  - Add ``parse.tsv``
  - Add ``write.csv``
  - Add ``write.tsv``

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
  - Add ``path.tsv_lines``
  - Add `pkg_resources.resource_copy`
  - Add ``test.assert_dir_unchanged``
  - Add ``test.assert_lines_equal``
  - Add ``test.assert_xml_equals``
  - Add ``test.reset_loggers``
  - ``test.assert_text_equals``: Show diff when not equal

- Fixes:

  - Fix package: Add missing data files and dependencies
  - Fix formatting of ``test.assert_matches``, ``test.assert_search_matches``:
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
