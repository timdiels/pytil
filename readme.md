Python 3 utility library. Looks like a turtle, tastes like chicken.

Be warned: as a pre-alpha, none of the interface is stable yet, may be tailored to the author's current needs and is probably not very reusable outside that context.

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
