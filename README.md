My personal library of Python utilities.

### Links
- [Conda](TODO)
- [Old PyPI](https://pypi.python.org/pypi/pytil/), for older versions of the
  library.
- [GitHub](https://github.com/timdiels/pytil/)

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
pip install -e .
```

You still need to install dependencies. If they are the same as one of the
released conda pkgs you can use `conda install --only-deps`. Otherwise open
`conda/meta.yaml` and `conda install` anything listed in run. In order to run
the tests, also install the test requirements from `meta.yaml`. Now you can run
tests with `pytest`. (I only list dependencies in conda recipe, not in
`setup.py`, keeps it DRY at the cost of having to install them manually to set
up dev env).

#### Building a conda pkg
This is just in case you want to try out the build before pushing a version tag
to master, which builds for you and pushes to conda. The conda recipe runs
pytest after the build either way.

First time setup:

```
conda create -n conda-build 'python==3.8.*'
conda activate conda-build
conda install conda-build
```

Building a pkg (to try it out before pushing to master):

```
cd $dir_containing_meta.yaml
conda-build . --channel anaconda --channel conda-forge
```

If for some reason you want to try it out, create a new conda env, install
dependencies manually (or `conda install --only-deps` with a previous version
if deps are the same) and finally `conda install --use-local pytil`.

#### Notes
`$repo/tests` is kept separate from `$repo/pytil` to prevent including them in
the conda package.
