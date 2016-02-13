#!/bin/sh

# Create python virtual environment to develop in

set -e

# sip-based install like this
# or: http://stackoverflow.com/a/1962076/1031434
install_sip() {
    python -c 'import sip' && return
    version=4.17
    wget http://sourceforge.net/projects/pyqt/files/sip/sip-$version/sip-$version.tar.gz
    tar zxvf sip-$version.tar.gz
    pushd sip-$version
    python configure.py
    make
    make install
    popd
    rm -rf sip-$version{,.tar.gz}
}

install_pyqt() {
    python -c 'import PyQt5' && return
    version=5.5.1
    wget http://sourceforge.net/projects/pyqt/files/PyQt5/PyQt-$version/PyQt-gpl-$version.tar.gz
    tar zxvf PyQt-gpl-$version.tar.gz
    pushd PyQt-gpl-$version
    python configure.py
    make
    make install
    popd
    rm -rf PyQt-gpl-$version{,.tar.gz}
}

[ -d venv ] || python -m venv venv
. venv/bin/activate
pip install --upgrade pip
pip install --upgrade setuptools
pip install -r requirements.txt
pip install -r extra_requirements.txt
pip install '.[test,dev]'