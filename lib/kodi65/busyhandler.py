# -*- coding: utf8 -*-

# Copyright (C) 2015 - Philipp Temminghoff <phil65@kodi.tv>
# This program is Free Software see LICENSE file for details

import xbmc
from kodi65 import utils
import traceback
from functools import wraps


class BusyHandler(object):
    """
    Class to deal with busydialog handling
    """
    def __init__(self, *args, **kwargs):
        self.busy = 0
        self.enabled = True

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def show_busy(self):
        """
        Increase busycounter and open busydialog if needed
        """
        if not self.enabled:
            return None
        if self.busy == 0:
            xbmc.executebuiltin("ActivateWindow(busydialog)")
        self.busy += 1

    def hide_busy(self):
        """
        Decrease busycounter and close busydialog if needed
        """
        if not self.enabled:
            return None
        self.busy = max(0, self.busy - 1)
        if self.busy == 0:
            xbmc.executebuiltin("Dialog.Close(busydialog)")


def set_busy(func):
    """
    Decorator to show busy dialog while function is running
    """
    @wraps(func)
    def decorator(self, *args, **kwargs):
        busyhandler.show_busy()
        result = func(self, *args, **kwargs)
        try:
            result = func(self, *args, **kwargs)
        except Exception:
            result = None
            utils.log(traceback.format_exc())
            utils.notify("Error", "please contact add-on author")
        finally:
            busyhandler.hide_busy()
        return result

    return decorator

busyhandler = BusyHandler()
