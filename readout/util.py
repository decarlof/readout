"""Various utility functions."""
import argparse
import os
import time

from epics import PV
from readout import log


def onChanges(pvname=None, value=None, char_value=None, **kw):

    log.warning('PV Changed => Slack: %s %s', pvname, char_value)
    bot_token = os.environ.get("BOT_TOKEN")
    app_token = os.environ.get("APP_TOKEN") 

    # WebClient insantiates a client that can call API methods
    client = WebClient(token=bot_token)

    # ID of channel you want to post message to
    channel_id = "automated"
    message = pvname + ': ' + char_value

    try:
        # Call the conversations.list method using the WebClient
        result = client.chat_postMessage(
            channel=channel_id,
            text=message
        )
    except SlackApiError as e:
        log.error(f"Error: {e}")

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


def tupleize(num_items=None, conv=float, dtype=tuple):
    """Convert comma-separated string values to a *num-items*-tuple of values converted with
    *conv*.
    """
    def split_values(value):
        """Convert comma-separated string *value* to a tuple of numbers."""
        try:
            result = dtype([conv(x) for x in value.split(',')])
        except:
            raise argparse.ArgumentTypeError('Expect comma-separated tuple')

        if num_items and len(result) != num_items:
            raise argparse.ArgumentTypeError('Expected {} items'.format(num_items))

        return result

    return split_values
