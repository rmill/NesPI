# -*- coding: utf-8 -*-
# uinput - Python bindings for Linux uinput system
# Copyright © 2012 Tuomas Jorma Juhani Räsänen <tuomasjjrasanen@tjjr.fi>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Python bindings to Linux uinput system.

Usage:
>>> events = (
>>>     uinput.BTN_JOYSTICK,
>>>     uinput.ABS_X + (0, 255, 0, 0),
>>>     uinput.ABS_Y + (0, 255, 0, 0),
>>>     )
>>> device = uinput.Device(events)
>>> device.emit(uinput.ABS_X, 5, syn=False)
>>> device.emit(uinput.ABS_Y, 5)
>>> device.emit(uinput.BTN_JOYSTICK, 1) # Press.
>>> device.emit(uinput.BTN_JOYSTICK, 0) # Release.
"""

from __future__ import absolute_import

import ctypes
import os
import distutils.sysconfig as sysconfig

from .ev import *

_UINPUT_MAX_NAME_SIZE = 80
_ABS_CNT = ABS_MAX[1] + 1

class _struct_input_id(ctypes.Structure):
    _fields_ = [("bustype", ctypes.c_int16),
                ("vendor", ctypes.c_int16),
                ("product", ctypes.c_int16),
                ("version", ctypes.c_int16),
                ]

class _struct_uinput_user_dev(ctypes.Structure):
    _fields_ = [("name", ctypes.c_char * _UINPUT_MAX_NAME_SIZE),
                ("id", _struct_input_id),
                ("ff_effects_max", ctypes.c_int),
                ("absmax", ctypes.c_int * _ABS_CNT),
                ("absmin", ctypes.c_int * _ABS_CNT),
                ("absfuzz", ctypes.c_int * _ABS_CNT),
                ("absflat", ctypes.c_int * _ABS_CNT),
                ]

def _error_handler(result, fn, args):
    if result == -1:
        code = ctypes.get_errno()
        raise OSError(code, os.strerror(code))
    elif result < -1:
        raise RuntimeError("unexpected return value: %s" % result)
    return result

_libsuinput_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "_libsuinput" + sysconfig.get_config_var("SO")))
_libsuinput = ctypes.CDLL(_libsuinput_path, use_errno=True)
_libsuinput.suinput_open.errcheck = _error_handler
_libsuinput.suinput_enable_event.errcheck = _error_handler
_libsuinput.suinput_create.errcheck = _error_handler
_libsuinput.suinput_write_event.errcheck = _error_handler
_libsuinput.suinput_emit.errcheck = _error_handler
_libsuinput.suinput_syn.errcheck = _error_handler
_libsuinput.suinput_destroy.errcheck = _error_handler

class Device(object):

    """Device handle.

    `events`  - a sequence of event capability descriptors

    `name`    - name displayed in /proc/bus/input/devices

    `bustype` - bus type identifier, see linux/input.h

    `vendor`  - vendor identifier

    `product` - product identifier

    `version` - version identifier
    """

    def __init__(self, events, name="python-uinput",
                 bustype=0, vendor=0, product=0, version=0):
        self.__events = events
        self.__uinput_fd = -1
        self.__name = name.encode()

        user_dev = _struct_uinput_user_dev(self.__name)
        user_dev.id.bustype = bustype
        user_dev.id.vendor = vendor
        user_dev.id.product = product
        user_dev.id.version = version
        self.__uinput_fd = _libsuinput.suinput_open()
        for ev_spec in self.__events:
            ev_type, ev_code = ev_spec[:2]
            _libsuinput.suinput_enable_event(self.__uinput_fd, ev_type, ev_code)
            if len(ev_spec) > 2:
                absmin, absmax, absfuzz, absflat = ev_spec[2:]
                user_dev.absmin[ev_code] = absmin
                user_dev.absmax[ev_code] = absmax
                user_dev.absfuzz[ev_code] = absfuzz
                user_dev.absflat[ev_code] = absflat

        _libsuinput.suinput_create(self.__uinput_fd, ctypes.pointer(user_dev))

    def syn(self):
        """Fire all emitted events.

        All emitted events will be placed in a certain kind of event
        queue. Queued events will be fired when this method is
        called. This makes it possible to emit "atomic" events. For
        example sending REL_X and REL_Y atomically requires to emit
        first event without syn and the second with syn::

          d.emit(uinput.REL_X, 1, syn=False)
          d.emit(uinput.REL_Y, 1)

        The call above appears as a single (+1, +1) event.
        """

        _libsuinput.suinput_syn(self.__uinput_fd)

    def emit(self, event, value, syn=True):
        """Emit event.

        `event` - event identifier, for example uinput.REL_X

        `value` - value of the event
           KEY/BTN      : 1 (key-press) or 0 (key-release)
           REL          : integer value of the relative change
           ABS          : integer value in the range of min and max values

        `syn` - If True, Device.syn(self) will be called before return.
        """

        ev_type, ev_code = event
        _libsuinput.suinput_emit(self.__uinput_fd, ev_type, ev_code, value)
        if syn:
            self.syn()

    def __del__(self):
        if self.__uinput_fd >= 0:
            _libsuinput.suinput_destroy(self.__uinput_fd)
