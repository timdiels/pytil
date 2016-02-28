Python 3 utility library. Looks like a turtle, tastes like chicken.

Chicken Turtle provides a project template, development tools (CLI) and various
utility functions (API). Chicken Turtle primarily supports Python3.

Chicken Turtle is pre-alpha. None of the interface is stable, may be tailored
to the author's current needs and is probably not very reusable outside that
context.

Chicken Turtle has some optional dependencies. E.g. to use
`chicken_turtle.pyqt`, you will need to add PyQt to your project's
dependencies. For now, you'll have to let the `ImportError`s guide you to the
right dependencies to add to setup.py assuming your tests have full coverage.


## Project template usage

Instructions for the included project template.

To create a project with Chicken Turtle:

- Copy the template directory to start your project from.
- Replace all occurences of `$project_name` in the template files with your project name.
- Edit `setup.py` with the details of your project.
- Rename gitignore to .gitignore

To use the created project:

- venv_create.sh: create a virtual environment corresponding to setup.py. If requirements.txt exists, that list of packages will be installed. If extra_requirements.txt exists (corresponding to the extra dependencies in setup.py), these will also be installed. Then setup.py's deps are installed, without upgrading any other packages. 
- interpreter.sh: start an interpreter inside the virtual environment, ensuring the project source is in the PYTHONPATH and start an interactive session in which interpreter.py is first executed.
- test data should be placed in test/data
- output of last test runs is kept in test/last_runs 
- run_tests.py to run the tests, but you need to run it from withing the venv (i.e. `. venv/bin/activate` before running this)


