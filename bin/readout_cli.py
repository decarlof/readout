import os
import sys
import time
import pathlib
import argparse
import numpy as np

from epics import PV
from datetime import datetime

from readout import log
from readout import config
from readout import util

def init(args):
    if not os.path.exists(str(args.config)):
        config.write(str(args.config))
    else:
        raise RuntimeError("{0} already exists".format(args.config))

def status(args):
    config.show_config(args)

def show_readout(args):

    log.info('Checking\t%s', args.camera_prefix)
    pv_in = PV(args.camera_prefix)
    # pv_value = pv_in.get()
    connected, message = util.check_pvs_connected(pv_in)

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
