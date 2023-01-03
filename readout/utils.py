"""Various utility functions."""
import argparse
import os
import time

from epics import PV
from readout import log


def wait_pv(epics_pv, wait_val, timeout=-1):
    """Wait on a pv to be a value until max_timeout (default forever)
       delay for pv to change
    """

    time.sleep(.01)
    start_time = time.time()
    while True:
        pv_val = epics_pv.get()
        if isinstance(pv_val, float):
            if abs(pv_val - wait_val) < EPSILON:
                return True
        if pv_val != wait_val:
            if timeout > -1:
                current_time = time.time()
                diff_time = current_time - start_time
                if diff_time >= timeout:
                    log.error('  *** wait_pv(%s, %d, %5.2f reached max timeout. Return False',
                                  epics_pv.pvname, wait_val, timeout)
                    return False
            time.sleep(.01)
        else:
            return True

def check_pvs_connected(epics_pv):
    """
    Checks whether an EPICS PVs is connected.
    
    Returns
    -------
    bool
        True if PV is connected, otherwise False.
    string
        Message confirming the PV status
    """

    message = ()
    connected = True

    if not epics_pv.connected:
        log.error('\t\t%s is not connected', epics_pv.pvname)
        message += ('\nPV ' + epics_pv.pvname + ' is not connected', )
        connected = False
    else:
        log.info('\tOK\t%s is connected: %s', epics_pv.pvname, epics_pv.get(as_string=True))
        message += ('\n' + epics_pv.pvname + ': ' + epics_pv.get(as_string=True), )
    return connected, message

def max_seconds(max_seconds, *, interval=1):
    interval = int(interval)
    start_time = time.time()
    end_time = start_time + max_seconds
    yield 0
    while time.time() < end_time:
        if interval > 0:
            next_time = start_time
            while next_time < time.time():
                next_time += interval
            time.sleep(int(round(next_time - time.time())))
        yield int(round(time.time() - start_time))
        if int(round(time.time() + interval)) > int(round(end_time)): 
            return

def positive_int(value):
    """Convert *value* to an integer and make sure it is positive."""
    result = int(value)
    if result < 0:
        raise argparse.ArgumentTypeError('Only positive integers are allowed')

    return result