==========
AD readout
==========

**readout** measure the readout time for a camera running under areaDetector

Usage
=====

::

    $ readout show --camera-prefix 2bmb:SP1


::

For help::

    readout show -h

For all options::

    $ readout -h
    usage: pv [-h] [--config FILE]  ...


Installation
============

P
Installing from source
======================

In a prepared virtualenv or as root for system-wide installation clone **readout** from its github repository

::

    $ conda create -n readut
    $ conda activate pv
    $ git clone https://github.com/decarlof/readout

To install pv, run::

    $ cd readout
    $ pip install .


Dependencies
============

Install the following package::

    $ conda install ....

