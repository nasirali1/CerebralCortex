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
from cerebralcortex.data_processor.data_diagnostic.post_processing import *

def packet_loss_marker(stream_id, CC_obj, config, type: str):

    #only create windows if a window has data in it
    stream = CC_obj.get_datastream(stream_id, type="data")
    windowed_data = window(stream.data, config['general']['window_size'], False)

    results = OrderedDict()


    if type=="ecg":
        sampling_rate = config["sampling_rate"]["ecg"]
        threshold_val = config["packet_loss_marker"]["ecg_acceptable_packet_loss"]
        label = config["labels"]["ecg_packet_loss"]
    elif type=="rip":
        sampling_rate = config["sampling_rate"]["rip"]
        threshold_val = config["packet_loss_marker"]["rip_acceptable_packet_loss"]
        label = config["labels"]["rip_packet_loss"]
    elif type=="motionsense":
        sampling_rate = config["sampling_rate"]["motionsense"]
        threshold_val = config["packet_loss_marker"]["motionsense_acceptable_packet_loss"]
        label = config["labels"]["motionsense_packet_loss"]
    else:
        raise ValueError("Incorrect sensor type.")

    for key, data in windowed_data.items():

        available_packets = len(data)
        expected_packets = sampling_rate * config['general']['window_size']

        if (available_packets/expected_packets)< threshold_val:
            results[key] = label


    merged_windows = merge_consective_windows(results)
    store(stream_id, merged_windows, CC_obj, config, type, config["algo_names"]["packet_loss"])
