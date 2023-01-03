"""Various utility functions."""
import argparse
import os
import time
import numpy as np

from epics import PV
from readout import log
from readout import utils

def measure(epics_pvs, args):

    camera_acquire = 0
    if epics_pvs['CamAcquire'].get() == 1:
        camera_acquire = 1
        log.info('Stopping camera')
        epics_pvs['CamAcquire'].put('Done')
        utils.wait_pv(epics_pvs['CamAcquire'], 0)

    epics_pvs['CamBinX'].put(pow(2,args.binning), wait=True)
    epics_pvs['CamBinY'].put(pow(2,args.binning), wait=True)

    if args.size_x == -1 or args.size_y == -1:
        epics_pvs['CamSizeX'].put(epics_pvs['CamMaxSizeXRBV'].get()) 
        epics_pvs['CamSizeY'].put(epics_pvs['CamMaxSizeYRBV'].get()) 
        epics_pvs['CamMinX'].put(0)
        epics_pvs['CamMinY'].put(0)
        args.size_x = epics_pvs['CamMaxSizeXRBV'].get()
        args.size_y = epics_pvs['CamMaxSizeYRBV'].get()

    exposure_time = epics_pvs['CamAcquireTime'].get()
    epics_pvs['CamAcquireTime'].put(0, wait=True)
    epics_pvs['CamMinX'].put(args.min_x, wait=True)
    epics_pvs['CamMinY'].put(args.min_y, wait=True)
    epics_pvs['CamSizeX'].put(args.size_x, wait=True)
    epics_pvs['CamSizeY'].put(args.size_y, wait=True)
    if epics_pvs['CamSizeXRBV'].get() != args.size_x:
        log.warning('Region size x adjusted by AD from %s to %s', args.size_x, epics_pvs['CamSizeXRBV'].get())
        epics_pvs['CamSizeX'].put(epics_pvs['CamSizeXRBV'].get())
    if epics_pvs['CamSizeYRBV'].get() != args.size_y:
        epics_pvs['CamSizeY'].put(epics_pvs['CamSizeYRBV'].get())
        log.warning('Region size y adjusted by AD from %s to %s', args.size_y, epics_pvs['CamSizeYRBV'].get())
    epics_pvs['CamImageMode'].put('Continuous', wait=True)

    if not args.manual:
        camera_bit(epics_pvs, args)

    # start the camera
    epics_pvs['CamAcquire'].put('Acquire')
    utils.wait_pv(epics_pvs['CamAcquire'], 1)

    array_rate = []
    for sec in utils.max_seconds(2, interval=1):
        rate = epics_pvs['CamArrayRateRBV'].get()
        array_rate.append(rate)
        log.info('%d s: %s fps', sec, rate)

    # stop the camera
    epics_pvs['CamAcquire'].put('Done')
    utils.wait_pv(epics_pvs['CamAcquire'], 0)

    log.info('Camera Model: %s', epics_pvs['CamManufacturerRBV'].get())
    log.info('Camera Model: %s', epics_pvs['CamModelRBV'].get())
    log.info('Sensor size: (%s, %s)', epics_pvs['CamMaxSizeXRBV'].get(), epics_pvs['CamMaxSizeYRBV'].get())
    log.info('Image  size: (%s, %s)', epics_pvs['CamArraySizeXRBV'].get(), epics_pvs['CamArraySizeYRBV'].get())
    log.info('Binning: %s', int(np.log2(epics_pvs['CamBinXRBV'].get())))
    log.info('ADC bit depth: %s', epics_pvs['CamGC_AdcBitDepthRBV'].get(as_string=True))
    log.info('Pixel format: %s', epics_pvs['CamPixelFormatRBV'].get(as_string=True))
    log.info('Convert pixel format: %s', epics_pvs['CamConvertPixelFormatRBV'].get(as_string=True))
    log.info('Max: %s fps', max(array_rate))
    log.warning('Readout time %s ms', 1.0/max(array_rate)*1000)


    # update entries to RBV
    epics_pvs['CamSizeX'].put(epics_pvs['CamSizeXRBV'].get()) 
    epics_pvs['CamSizeY'].put(epics_pvs['CamSizeYRBV'].get()) 

    epics_pvs['CamAcquireTime'].put(exposure_time, wait=True)

    # if the camera was collecting images start it again
    if camera_acquire == 1:
        time.sleep(1)
        log.info('Restarting camera')
        epics_pvs['CamAcquire'].put('Acquire')
        utils.wait_pv(epics_pvs['CamAcquire'], 1)

    return 1.0/max(array_rate)*1000

def camera_bit(epics_pvs, args):
    
    camera_model = epics_pvs['CamModelRBV'].get()
    log.info("Set bit rate for camera %s to %s" % (camera_model, args.bits))
    # 2bmbSP1: 'Oryx ORX-10G-51S5M'
    # 2bmbSP2: 'Oryx ORX-10G-310S9M' 

    # args.bits
    # ======================================
    # 0:  8-bit
    # 1: 10-bit
    # 2: 12-bit
    # 3: 16-bit

    # GC_AdcBitDepth 2bmbSP1: 2bmbSP2:
    # ================================
    # STATE  0:      Bit8     Bit8
    # STATE  1:      Bit10    Bit10
    # STATE  2:      Bit12    Bit12

    # PixelFormat 2bmbSP1:     2bmbSP2:
    # ======================================
    # STATE  0:   Mono8        Mono8  
    # STATE  1:   Mono16       Mono16 
    # STATE  2:   Mono12Packed Mono10Packed 
    # STATE  3:   Mono12p      Mono12Packed 
    # STATE  4:     N/A        Mono10p
    # STATE  5:     N/A        Mono12p

    # ConvertPixelFormat 2bmbSP1:    2bmbSP2:
    # ============================================
    # STATE  0:          None        None
    # STATE  1:          Mono8       Mono8
    # STATE  2:          Mono16      Mono16
    # STATE  3:          Raw16       Raw16
    # STATE  4:          RGB8        RGB8
    # STATE  5:          RGB16       RGB16 


    bit_selected = [8, 10, 12, 16].index(args.bits)
    
    status = 1
    log.info('Try to setting camera %s', camera_model)
    if camera_model == 'Oryx ORX-10G-310S9M':
        log.info('OK')
        if (bit_selected == 0):
            epics_pvs['CamGC_AdcBitDepth'].put(0, wait=True)
            epics_pvs['CamPixelFormat'].put(0, wait=True)
            epics_pvs['CamConvertPixelFormat'].put(1, wait=True)
        elif (bit_selected == 1):
            epics_pvs['CamGC_AdcBitDepth'].put(1, wait=True)
            epics_pvs['CamPixelFormat'].put(2, wait=True)
            epics_pvs['CamConvertPixelFormat'].put(2, wait=True)
        elif (bit_selected == 2):
            epics_pvs['CamGC_AdcBitDepth'].put(2, wait=True)
            epics_pvs['CamPixelFormat'].put(3, wait=True)
            epics_pvs['CamConvertPixelFormat'].put(2, wait=True)
        elif (bit_selected == 3):
            epics_pvs['CamGC_AdcBitDepth'].put(2, wait=True)
            epics_pvs['CamPixelFormat'].put(1, wait=True)
            epics_pvs['CamConvertPixelFormat'].put(2, wait=True)
    elif camera_model == 'Oryx ORX-10G-51S5M':
        log.info('OK')
        if (bit_selected == 0):
            epics_pvs['CamGC_AdcBitDepth'].put(0, wait=True)
            epics_pvs['CamPixelFormat'].put(0, wait=True)
            epics_pvs['CamConvertPixelFormat'].put(1, wait=True)
        elif (bit_selected == 1):
            epics_pvs['CamGC_AdcBitDepth'].put(1, wait=True)
            epics_pvs['CamPixelFormat'].put(2, wait=True)
            epics_pvs['CamConvertPixelFormat'].put(2, wait=True)
        elif (bit_selected == 2):
            epics_pvs['CamGC_AdcBitDepth'].put(2, wait=True)
            epics_pvs['CamPixelFormat'].put(2, wait=True)
            epics_pvs['CamConvertPixelFormat'].put(2, wait=True)
        elif (bit_selected == 3):
            epics_pvs['CamGC_AdcBitDepth'].put(2, wait=True)
            epics_pvs['CamPixelFormat'].put(1, wait=True)
            epics_pvs['CamConvertPixelFormat'].put(2, wait=True)
    else:
        log.error('Camera %s is not supported', camera_model)
        status = 0

    return status
    
