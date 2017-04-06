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


def variance_based_data_quality(datapoints: List[DataPoint], window_size: int, type: str) -> OrderedDict:
    """
    This method accepts one window at a time
    :param datapoints:
    :param window_size: in seconds
    :param type: acceptable types are: phone, autosense, motionsense
    :return: OrderedDict representing [(st,et),[label],
                                       (st,et),[label],
                                        ...]
    """
    windowed_data = window(datapoints, window_size, False)
    results = OrderedDict()
    sampling_rate = None
    threshold_val = None

    if type=="autosense":
        threshold_val = 12

    elif type=="motionsense":
        threshold_val = 12
    else:
        raise ValueError("Incorrect sensor type.")

    for key, data in windowed_data.items():
        # remove outliers from the window data
        normal_values = outlier_detection(data)

        # TO-DO: move all threshold values in config
        if np.var(normal_values) < threshold_val:
            results[key] = "off-body"
        else:
            results[key] = "on-body"

    merged_windows = merge_consective_windows(results)
    return merged_windows

def bb():
    #get GSR stream
    #create non-empty windows
    #get_stream_data()
    pass
def outlier_detection(window_data: list) -> list:
    """
    removes outliers from a list
    This algorithm is modified version of Chauvenet's_criterion (https://en.wikipedia.org/wiki/Chauvenet's_criterion)
    :param window_data:
    :return:
    """
    if not window_data:
        raise ValueError("List is empty.")

    median = np.median(window_data)
    standard_deviation = np.std(window_data)
    normal_values = list()

    for val in window_data:
        if (abs(val) - median) < standard_deviation:
            normal_values.append(val)

    return normal_values


variance_based_data_quality([1, 2, 3])
