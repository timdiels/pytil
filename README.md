Python 3 utility library. Looks like a turtle, tastes like chicken.

Chicken Turtle Util (CTU) provides various an API of Python utility functions.

Chicken Turtle Util is pre-alpha. None of the interface is stable, meaning it may
change in the future.

Chicken Turtle Util has some optional dependencies. E.g. to use
`chicken_turtle.pyqt`, you will need to add PyQt to your project's
dependencies. For now, you'll have to let the `ImportError`s guide you to the
right dependencies to add to setup.py assuming your tests have full coverage.

## Project decisions

### API design

If it's a path, expect a `pathlib.Path`, not a `str`.

If extending a module from another project, e.g. `pandas`, use the same name
as the module. While a `from pandas import *` would allow the user to access
functions of the real pandas module through the extended module, we have no
control over additions to the real pandas, which could lead to name clashes
later on, so don't. 