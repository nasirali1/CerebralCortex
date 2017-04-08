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

from cerebralcortex.data_processor.data_diagnostic.post_processing import *
from cerebralcortex.data_processor.signalprocessing.window import window
from cerebralcortex.data_processor.data_diagnostic.util import *


def battery_marker(stream_id, CC_obj, config, type: str) -> OrderedDict:
    """
    :param datapoints:
    :param window_size: in seconds
    :param type: acceptable types are: phone, autosense, motionsense
    :return: OrderedDict representing [(st,et),[label],
                                       (st,et),[label],
                                        ...]
    """
    results = OrderedDict()

    stream = CC_obj.get_datastream(stream_id, type="all")
    windowed_data = window(stream.data, config['general']['window_size'], True)

    for key, data in windowed_data.items():
        dp = []
        for k in data:
            dp.append(float(k.sample))

        if type == "phone":
            results[key] = phone_battery(dp, config)
        elif type == "motionsense":
            results[key] = motionsense_battery(dp, config)
        elif type == "autosense":
            results[key] = autosense_battery(dp, config)
        else:
            raise ValueError("Incorrect sensor type.")

    merged_windows = merge_consective_windows(results)
    store(stream_id, merged_windows, CC_obj, config, type, config["algo_names"]["battery_marker"])
    # return merged_windows


def phone_battery(dp: List, config) -> str:
    """

    :param dp:
    :return:
    """
    dp_sample_avg = np.mean(dp)
    if dp_sample_avg <= config['battery_marker']['phone_powered_off']:
        return config['labels']['sensor_powered_off']
    else:
        # get sampling rate and check if the current window has acceptable number of samples
        # get one minute previous window of powered off phone to see if it was powered of manually or due to low battery
        """TO-DO"""
        if dp_sample_avg < config['battery_marker']['phone_battery_down']:
            return config['labels']['phone_battery_down']
    return None


def motionsense_battery(dp: List, config) -> str:
    """

    :param dp:
    :return:
    """
    dp_sample_avg = np.mean(dp)

    if dp_sample_avg <= config['battery_marker']['motionsense_powered_off']:
        return config['labels']['motionsense_powered_off']
    else:
        # get sampling rate and check if the current window has acceptable number of samples
        """TO-DO"""
        if dp_sample_avg < config['battery_marker']['phone_powered_off']:
            return config['labels']['motionsense_battery_down']
    return None


def autosense_battery(dp: List, config) -> str:
    """

    :param dp:
    :return:
    """
    dp_sample_avg = np.mean(dp)
    if dp_sample_avg <= config['battery_marker']['autosense_powered_off']:
        return config['labels']['autosesen_powered_off']
    else:
        # Values (Min=0 and Max=6) in battery voltage.
        voltageValue = (dp_sample_avg / 4096) * 3 * 2
        if voltageValue < config['battery_marker']['autosense_battery_down']:
            return config['labels']['autosense_battery_down']
    return None
