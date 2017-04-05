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

from cerebralcortex.kernel.datatypes.datapoint import DataPoint
from cerebralcortex.data_processor.signalprocessing.window import window
from cerebralcortex.data_processor.data_diagnostic.util import *

def packet_loss_marker(datapoints: List[DataPoint], window_size: int, type: str) -> OrderedDict:
    """
    :param datapoints:
    :param window_size: in seconds
    :param type: acceptable types are: phone, autosense, motionsense
    :return: OrderedDict representing [(st,et),[label],
                                       (st,et),[label],
                                        ...]
    """
    #only create windows if a window has data in it
    windowed_data = window(datapoints, window_size, False)
    results = OrderedDict()
    sampling_rate = None
    threshold_val = None

    if type=="autosense":
        sampling_rate = 12

    elif type=="motionsense":
        sampling_rate = 12
    else:
        raise ValueError("Incorrect sensor type.")

    for key, data in windowed_data.items():

        available_packets = len(data)
        expected_packets = sampling_rate * window_size

        if (available_packets/expected_packets)< threshold_val:
            results[key] = "packet_loss"


    merged_windows = merge_consective_windows(results)
    return merged_windows
