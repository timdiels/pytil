from setuptools import setup, find_packages
from collections import defaultdict
from pathlib import Path
import os

setup_args = dict(
    version='5.0.0',
    name='pytil',
    description='Python 3 utility library',
    long_description=Path('README.rst').read_text(),
    url='https://github.com/timdiels/pytil',
    author='Tim Diels',
    author_email='timdiels.m@gmail.com',
    license='LGPL3',
    keywords='development util library utility utilities',
    packages=find_packages(),
    install_requires=[],
    extras_require={
        'algorithms': [
            'collections-extended==0.*',
            'networkx==1.*',
            'numpy==1.*',
            'scikit-learn==0.*',
            'scipy==0.*'
        ],
        'asyncio': [],
        'click': ['click==6.*'],
        'configuration': ['pyxdg==0.*'],
        'data_frame': [
            'numpy==1.*',
            'pandas==0.*'
        ],
        'debug': ['psutil==4.*'],
        'dev': [
            'numpydoc==0.*',
            'sphinx==1.*',
            'sphinx-rtd-theme==0.*',
            'coverage-pth==0.*',
            'networkx==1.*',
            'plumbum==1.*',
            'pytest==3.*',
            'pytest-asyncio==0.*',
            'pytest-catchlog==1.*',
            'pytest-cov==2.*',
            'pytest-env==0.*',
            'pytest-localserver==0.*',
            'pytest-mock==1.*'
        ],
        'dict': ['more-itertools==2.*'],
        'exceptions': [],
        'function': [],
        'hashlib': [],
        'http': ['requests==2.*'],
        'inspect': [],
        'iterable': [],
        'logging': [],
        'multi_dict': [],
        'observable': [],
        'path': [],
        'pymysql': ['pymysql==0.*'],
        'series': [
            'numpy==1.*',
            'pandas==0.*'
        ],
        'set': [],
        'sqlalchemy': ['sqlparse==0.*'],
        'test': [],
    },
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Natural Language :: English',
        'Operating System :: Android',
        'Operating System :: BeOS',
        'Operating System :: MacOS',
        'Operating System :: MacOS :: MacOS 9',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft',
        'Operating System :: Microsoft :: MS-DOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Microsoft :: Windows :: Windows 3.1 or Earlier',
        'Operating System :: Microsoft :: Windows :: Windows 7',
        'Operating System :: Microsoft :: Windows :: Windows 95/98/2000',
        'Operating System :: Microsoft :: Windows :: Windows CE',
        'Operating System :: Microsoft :: Windows :: Windows NT/2000',
        'Operating System :: Microsoft :: Windows :: Windows Server 2003',
        'Operating System :: Microsoft :: Windows :: Windows Server 2008',
        'Operating System :: Microsoft :: Windows :: Windows Vista',
        'Operating System :: Microsoft :: Windows :: Windows XP',
        'Operating System :: OS Independent',
        'Operating System :: OS/2',
        'Operating System :: Other OS',
        'Operating System :: PDA Systems',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: AIX',
        'Operating System :: POSIX :: BSD',
        'Operating System :: POSIX :: BSD :: BSD/OS',
        'Operating System :: POSIX :: BSD :: FreeBSD',
        'Operating System :: POSIX :: BSD :: NetBSD',
        'Operating System :: POSIX :: BSD :: OpenBSD',
        'Operating System :: POSIX :: GNU Hurd',
        'Operating System :: POSIX :: HP-UX',
        'Operating System :: POSIX :: IRIX',
        'Operating System :: POSIX :: Linux',
        'Operating System :: POSIX :: Other',
        'Operating System :: POSIX :: SCO',
        'Operating System :: POSIX :: SunOS/Solaris',
        'Operating System :: PalmOS',
        'Operating System :: Unix',
        'Operating System :: iOS',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: Stackless',
        'Topic :: Software Development',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
    ],
)

# Generate extras_require['all'], union of all extras
all_extra_dependencies = []
for dependencies in setup_args['extras_require'].values():
    all_extra_dependencies.extend(dependencies)
all_extra_dependencies = list(set(all_extra_dependencies))
setup_args['extras_require']['all'] = all_extra_dependencies

# Generate package data
#
# Anything placed underneath a directory named 'data' in a package, is added to
# the package_data of that package; i.e. included in the sdist/bdist and
# accessible via pkg_resources.resource_*
project_root = Path(__file__).with_name(setup_args['name'])
package_data = defaultdict(list)
for package in setup_args['packages']:
    package_dir = project_root / package.replace('.', '/')
    data_dir = package_dir / 'data'
    if data_dir.exists() and not (data_dir / '__init__.py').exists():
        # Found a data dir
        for parent, _, files in os.walk(str(data_dir)):
            package_data[package].extend(str((data_dir / parent / file).relative_to(package_dir)) for file in files)
setup_args['package_data'] = {k: sorted(v) for k,v in package_data.items()}  # sort to avoid unnecessary git diffs

# setup
setup(**setup_args)
