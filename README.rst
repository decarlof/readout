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
    2022-12-21 16:04:24,939 - Logs are saved at: /home/beams/USER2BMB/logs/readout_2022-12-21_16:04:24.log
    2022-12-21 16:04:24,942 - General
    2022-12-21 16:04:24,942 -   config           /home/beams/USER2BMB/readout.conf
    2022-12-21 16:04:24,942 -   verbose          True
    2022-12-21 16:04:24,943 - Checking  2bmbSP1:
    2022-12-21 16:04:25,950 -   OK  2bmbSP1:cam1:Manufacturer_RBV is connected: FLIR
    2022-12-21 16:04:25,950 - Camera Model: FLIR
    2022-12-21 16:04:25,950 - Camera Model: Oryx ORX-10G-51S5M
    2022-12-21 16:04:25,950 - Sensor size: (2448, 2048)
    2022-12-21 16:04:25,950 - Image  size: (2448, 2448)
    2022-12-21 16:04:26,575 - 0 s: 0.0 fps
    2022-12-21 16:04:27,576 - 1 s: 8.0 fps
    2022-12-21 16:04:28,577 - 2 s: 90.0 fps
    2022-12-21 16:04:28,577 - Max: 90.0 fps
    2022-12-21 16:04:28,578 - Readout time 11.11111111111111 ms

For all options::

    $ readout -h
    usage: readout [-h] [--config FILE]  ...

    optional arguments:
      -h, --help     show this help message and exit
      --config FILE  File name of configuration

    Commands:
      
        init         Create configuration file
        status       Show the readout-cli status
        show         show readout value


Installation
============

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

    $  conda install pyepics

