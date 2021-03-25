My personal library of Python utilities.

### Links
- [Conda](https://anaconda.org/timdiels/pytil)
- [GitHub](https://github.com/timdiels/pytil/)
- [Old PyPI](https://pypi.python.org/pypi/pytil/), for older versions of the
  library.

### Usage
Add pytil as a dependency to your conda recipe. Some submodules have additional
dependencies; open up each submodule you use and add dependencies corresponding
to third party imports. You needn't constrain those dependencies (unless you
need a particular version of them yourself), pytil's conda `run_constrained:`
will constrain them for you.

### Development guide
Guide for developing pytil itself.

#### Setting up a development environment
Install miniconda and then:

```
git checkout ...
cd $dir_containing_setup_py
conda create -n pytil 'python==3.8.*'
conda activate pytil
conda install pylint
pip install -e .
```

You still need to install dependencies. If they are the same as one of the
released conda pkgs you can use `conda install --only-deps`. Otherwise open
`conda/meta.yaml` and `conda install` anything listed in run. You can find the
conda channels to use in the conda build command in
`.github/workflows/publish.yaml`. In order to run the tests, also install the
test requirements from `meta.yaml`. Now you can run tests with `pytest`. (I
only list dependencies in conda recipe, not in `setup.py`, keeps it DRY at the
cost of having to install them manually to set up dev env).

#### Releasing a new version
The version needs to be adjusted in `setup.py` and `pytil/__init__.py`. Release
it with github releases, tag it as github suggests (v1.2.3) and list the
changes in its description. The GitHub repo will publish to anaconda when you
publish a new GitHub release.

#### Building a conda pkg
This is just in case you want to try out the build before creating a release on
github. The conda recipe runs pytest after the build.

First time setup:

```
conda create -n conda-build 'python==3.8.*'
conda activate conda-build
conda install conda-build
```

Building a pkg (to try it out before pushing to master):

```
cd $dir_containing_meta.yaml
conda-build . --channel ...
```

If for some reason you want to try it out, create a new conda env, install
dependencies manually (or `conda install --only-deps` with a previous version
if deps are the same) and finally `conda install --use-local pytil`.

#### Notes
`$repo/tests` is kept separate from `$repo/pytil` to prevent including them in
the conda package.
