"""Various utility functions."""
import argparse
import os
import time

from epics import PV
from readout import log
from readout import utils

def measure(epics_pvs, exposure_time=1, size_x=512, size_y=512, binning=1):

    camera_acquire = 0
    if epics_pvs['CamAcquire'].get() == 1:
        camera_acquire = 1
        log.info('Stopping camera')
        epics_pvs['CamAcquire'].put('Done')
        utils.wait_pv(epics_pvs['CamAcquire'], 0)

    cam_acquire_time        = epics_pvs['CamAcquireTime'].get()
    cam_acquire_time_rbv    = epics_pvs['CamAcquireTimeRBV'].get()
    cam_min_x               = epics_pvs['CamMinX'].get()
    cam_min_y               = epics_pvs['CamMinY'].get()       
    cam_min_x_rbv           = epics_pvs['CamMinXRBV'].get()    
    cam_min_y_rbv           = epics_pvs['CamMinYRBV'].get()    
    cam_size_x              = epics_pvs['CamSizeX'].get()      
    cam_size_y              = epics_pvs['CamSizeY'].get()      
    cam_size_x_rbv          = epics_pvs['CamSizeXRBV'].get()   
    cam_size_y_rbv          = epics_pvs['CamSizeYRBV'].get()   
    cam_max_size_x_rbv      = epics_pvs['CamMaxSizeXRBV'].get()
    cam_max_size_y_rbv      = epics_pvs['CamMaxSizeYRBV'].get()
    cam_image_mode          = epics_pvs['CamImageMode'].get()
    cam_image_mode_rbv      = epics_pvs['CamImageModeRBV'].get()
    cam_model_rbv           = epics_pvs['CamModelRBV'].get()
    cam_manufacturer_rbv    = epics_pvs['CamManufacturerRBV'].get()
    cam_array_size_x_rbv    = epics_pvs['CamArraySizeXRBV'].get()
    cam_array_size_y_rbv    = epics_pvs['CamArraySizeXRBV'].get()

    log.info('Camera Model: %s', cam_manufacturer_rbv)
    log.info('Camera Model: %s', cam_model_rbv)
    log.info('Sensor size: (%s, %s)', cam_max_size_x_rbv, cam_max_size_y_rbv)
    log.info('Image  size: (%s, %s)', cam_array_size_x_rbv, cam_array_size_y_rbv)

    epics_pvs['CamAcquireTime'].put(0)
    epics_pvs['CamMinX'].put(0)
    epics_pvs['CamMinY'].put(0)
    epics_pvs['CamSizeX'].put(cam_max_size_x_rbv)
    epics_pvs['CamSizeY'].put(cam_max_size_y_rbv)
    epics_pvs['CamImageMode'].put('Continuous')

    epics_pvs['CamAcquire'].put('Acquire')
    utils.wait_pv(epics_pvs['CamAcquire'], 1)

    array_rate = []
    for sec in utils.max_seconds(2, interval=1):
        rate = epics_pvs['CamArrayRateRBV'].get()
        array_rate.append(rate)
        log.info('%d s: %s fps', sec, rate)
    log.info('Max: %s fps', max(array_rate))
    log.info('Readout time %s ms', 1.0/max(array_rate)*1000)
    # if the camera was collecting images start it again
    if camera_acquire == 1:
        time.sleep(1)
        log.info('Restarting amera')
        epics_pvs['CamAcquire'].put('Acquire')
        utils.wait_pv(epics_pvs['CamAcquire'], 1)
