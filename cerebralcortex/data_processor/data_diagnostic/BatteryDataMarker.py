# Copyright (c) 2016, MD2K Center of Excellence
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
from typing import List
import numpy as np

from cerebralcortex.kernel.datatypes.datapoint import DataPoint
from cerebralcortex.data_processor.signalprocessing.window import window
from cerebralcortex.data_processor.data_diagnostic.util import *

def battery_marker(datapoints: List[DataPoint], window_size: int, type: str) -> OrderedDict:
    """
    :param datapoints:
    :param window_size: in seconds
    :param type: acceptable types are: phone, autosense, motionsense
    :return: OrderedDict representing [(st,et),[label],
                                       (st,et),[label],
                                        ...]
    """
    windowed_data = window(datapoints, window_size, True)
    results = OrderedDict()
    for key, data in windowed_data.items():
        dp = []
        for k in data:
            dp.append(float(k.sample))

        if type=="phone":
            results[key] = phone_battery(dp)

        elif type=="motionsense":
            results[key] = phone_battery(dp)
        elif type=="autosense":
            results = phone_battery(dp)
        else:
            raise ValueError("Incorrect sensor type.")
    merged_windows = merge_consective_windows(results)
    return merged_windows

def phone_battery(dp: List) -> str:
    """

    :param dp:
    :return:
    """
    if not dp:
        return "phone-off"
    else:
        #get sampling rate and check if the current window has acceptable number of samples
        """TO-DO"""
        dp_sample_avg = np.mean(dp)
        if dp_sample_avg<10:
            return "phone-battery-down"
    return  None

def motionSenseBatteryMarker(dp: List) -> str:
    """

    :param dp:
    :return:
    """
    if not dp:
        return "motionsense-off"
    else:
        #get sampling rate and check if the current window has acceptable number of samples
        """TO-DO"""
        dp_sample_avg = np.mean(dp)
        if dp_sample_avg<10:
            return "motionsense-battery-down"
    return None

def autosense_battery(dp: List) -> str:
    """

    :param dp:
    :return:
    """
    if not dp:
        return "sensor-off"
    else:
        dp_sample_avg = np.mean(dp)
        # Values (Min=0 and Max=6) in battery voltage.
        voltageValue = (dp_sample_avg / 4096) * 3 * 2
        if voltageValue<0.5:
            return "sensor-battery-down"
    return None


