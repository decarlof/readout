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
    2022-12-21 15:48:22,430 - Logs are saved at: /home/beams/USER2BMB/logs/readout_2022-12-21_15:48:22.log
    2022-12-21 15:48:22,436 - General
    2022-12-21 15:48:22,436 -   config           /home/beams/USER2BMB/readout.conf
    2022-12-21 15:48:22,436 -   verbose          True
    2022-12-21 15:48:22,436 - Checking  2bmbSP1:
    2022-12-21 15:48:23,447 -   OK  2bmbSP1:cam1:Manufacturer_RBV is connected: FLIR
    2022-12-21 15:48:23,447 - stopping the camera
    2022-12-21 15:48:23,560 - Sensor size: (2448, 2048)
    2022-12-21 15:48:24,183 - 0 s: 71.0 fps
    2022-12-21 15:48:25,184 - 1 s: 44.0 fps
    2022-12-21 15:48:26,185 - 2 s: 86.0 fps
    2022-12-21 15:48:26,185 - Max: 86.0 fps
    2022-12-21 15:48:26,186 - Readout time 11.627906976744185 ms
    2022-12-21 15:48:27,187 - restarting the camera

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

