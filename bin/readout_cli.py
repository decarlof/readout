import os
import sys
import time
import pathlib
import argparse
import numpy as np

from epics import PV
from datetime import datetime

from readout import readout
from readout import log
from readout import config
from readout import utils



def init(args):
    if not os.path.exists(str(args.config)):
        config.write(str(args.config))
    else:
        raise RuntimeError("{0} already exists".format(args.config))

def init_pvs(args):
    epics_pvs = {}

    #Define PVs from the camera IOC that we will need
    prefix = args.camera_prefix
    camera_prefix = prefix + 'cam1:'

    epics_pvs['CamAcquire']             = PV(camera_prefix + 'Acquire')
    epics_pvs['CamAcquireBusy']         = PV(camera_prefix + 'AcquireBusy')
    epics_pvs['CamAcquireTime']         = PV(camera_prefix + 'AcquireTime')
    epics_pvs['CamAcquireTimeRBV']      = PV(camera_prefix + 'AcquireTime_RBV')
    epics_pvs['CamArrayCounterRBV']     = PV(camera_prefix + 'ArrayCounter_RBV')
    epics_pvs['CamArraySizeXRBV']        = PV(camera_prefix + 'ArraySizeX_RBV')
    epics_pvs['CamArraySizeYRBV']        = PV(camera_prefix + 'ArraySizeY_RBV')
    epics_pvs['CamBinX']                = PV(camera_prefix + 'BinX')
    epics_pvs['CamBinY']                = PV(camera_prefix + 'BinY')
    epics_pvs['CamBinXRBV']              = PV(camera_prefix + 'BinX_RBV')
    epics_pvs['CamBinYRBV']              = PV(camera_prefix + 'BinY_RBV')
    epics_pvs['CamConvertPixelFormat']   = PV(camera_prefix + 'ConvertPixelFormat')
    epics_pvs['CamGC_AdcBitDepth']       = PV(camera_prefix + 'GC_AdcBitDepth')
    epics_pvs['CamImageMode']           = PV(camera_prefix + 'ImageMode')
    epics_pvs['CamManufacturer']        = PV(camera_prefix + 'Manufacturer_RBV')
    epics_pvs['CamMaxSizeXRBV']          = PV(camera_prefix + 'MaxSizeX_RBV')
    epics_pvs['CamMaxSizeYRBV']          = PV(camera_prefix + 'MaxSizeY_RBV')
    epics_pvs['CamMinXRBV']              = PV(camera_prefix + 'MinX_RBV')
    epics_pvs['CamMinYRBV']              = PV(camera_prefix + 'MinY_RBV')
    epics_pvs['CamMinX']                 = PV(camera_prefix + 'MinX')
    epics_pvs['CamMinY']                 = PV(camera_prefix + 'MinY')
    epics_pvs['CamModel']               = PV(camera_prefix + 'Model_RBV')
    epics_pvs['CamNDAttributesFile']    = PV(camera_prefix + 'NDAttributesFile')
    epics_pvs['CamNDAttributesMacros']  = PV(camera_prefix + 'NDAttributesMacros')
    epics_pvs['CamNumImages']           = PV(camera_prefix + 'NumImages')
    epics_pvs['CamNumImagesCounter']    = PV(camera_prefix + 'NumImagesCounter_RBV')
    epics_pvs['CamPortNameRBV']            = PV(camera_prefix + 'PortName_RBV')
    epics_pvs['CamPixelFormat']          = PV(camera_prefix + 'PixelFormat')
    epics_pvs['CamSizeX']                = PV(camera_prefix + 'SizeX')
    epics_pvs['CamSizeY']                = PV(camera_prefix + 'SizeY')
    epics_pvs['CamSizeXRBV']             = PV(camera_prefix + 'SizeX_RBV')
    epics_pvs['CamSizeYRBV']             = PV(camera_prefix + 'SizeY_RBV')
    epics_pvs['CamTriggerMode']         = PV(camera_prefix + 'TriggerMode')
    epics_pvs['CamUniqueIdMode']        = PV(camera_prefix + 'UniqueIdMode')
    epics_pvs['CamWaitForPlugins']      = PV(camera_prefix + 'WaitForPlugins')

    # Wait 1 second for all PVs to connect
    time.sleep(1)

    return epics_pvs

def status(args):
    config.show_config(args)

def show_readout(args):

    log.info('Checking\t%s', args.camera_prefix)
    epics_pvs = init_pvs(args)
    connected, message = utils.check_pvs_connected(epics_pvs['CamManufacturer'])
    if connected:
        readout.measure(epics_pvs)

def main():

    # set logs directory
    home = os.path.expanduser("~")
    logs_home = home + '/logs/'
    # make sure logs directory exists
    if not os.path.exists(logs_home):
        os.makedirs(logs_home)
    # setup logger
    lfname = logs_home + 'slack_' + datetime.strftime(datetime.now(), "%Y-%m-%d_%H:%M:%S") + '.log'
    log.setup_custom_logger(lfname)
    log.warning('Logs are saved at: %s' % lfname)

    
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', **config.SECTIONS['general']['config'])
    status_params = config.READOUT_PARAMS
    show_params   = config.READOUT_PARAMS

    cmd_parsers = [
        ('init',        init,           (),                             "Create configuration file"),
        ('status',      status,         status_params,                  "Show the readout-cli status"),
        ('show',        show_readout,   show_params,                    "show readout value"),
     ]

    subparsers = parser.add_subparsers(title="Commands", metavar='')

    for cmd, func, sections, text in cmd_parsers:
        cmd_params = config.Params(sections=sections)
        cmd_parser = subparsers.add_parser(cmd, help=text, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        cmd_parser = cmd_params.add_arguments(cmd_parser)
        cmd_parser.set_defaults(_func=func)

    args = config.parse_known_args(parser, subparser=True)
    args.lfname = lfname
    
    try: 
        # load args from default (config.py) if not changed
        config.log_values(args)
        args._func(args)
        # undate meta5.config file
        sections = config.READOUT_PARAMS
        config.write(args.config, args=args, sections=sections)
    except RuntimeError as e:
        log.error(str(e))
        sys.exit(1)


if __name__ == "__main__": 
    main()
