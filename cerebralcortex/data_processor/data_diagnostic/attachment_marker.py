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

import uuid
import stat
from datetime import datetime
from collections import OrderedDict

from cerebralcortex.data_processor.signalprocessing.window import window
from cerebralcortex.data_processor.data_diagnostic.util import merge_consective_windows, outlier_detection
from cerebralcortex.data_processor.data_diagnostic.post_processing import store
from cerebralcortex.CerebralCortex import CerebralCortex


def attachment_marker(stream_id: uuid, CC_obj: CerebralCortex, config: dict):
    """
    Label sensor data as sensor-on-body, sensor-off-body, or improper-attachment.
    All the labeled data (st, et, label) with its metadata are then stored in a datastore
    :param stream_id: UUID
    :param CC_obj: CerebralCortex object
    :param config: Data diagnostics configurations
    """
    stream = CC_obj.get_datastream(stream_id, type="all")
    windowed_data = window(stream.data, config['general']['window_size'], False)

    results = OrderedDict()
    threshold_val = None
    name = stream._name

    if name == "ecg":
        threshold_val = config['attachment_marker']['ecg_on_body']
        label_on = config['labels']['ecg_on_body']
        label_off = config['labels']['ecg_off_body']
        label_attachment = config['labels']['ecg_improper_attachment']
    elif name == "rip":
        threshold_val = config['attachment_marker']['rip_on_body']
        label_on = config['labels']['rip_on_body']
        label_off = config['labels']['rip_off_body']
        label_attachment = config['labels']['rip_improper_attachment']
    elif name == "motionsense":
        threshold_val = config['attachment_marker']['motionsense_on_body']
        label_on = config['labels']['motionsense_on_body']
        label_off = config['labels']['motionsense_off_body']
        label_attachment = config['labels']['motionsense_improper_attachment']
    else:
        raise ValueError("Incorrect sensor type.")

    for key, data in windowed_data.items():
        # remove outliers from a window data
        normal_values = outlier_detection(data)

        if stat.variance(normal_values) < threshold_val:
            results[key] = label_on
        else:
            results[key] = label_off

    merged_windows = merge_consective_windows(results)
    store(stream_id, merged_windows, CC_obj, config, name, config["algo_names"]["attachment_marker"])


"""
TO-DO
gsr_response method is not being used. Need to make sure whether GSR values actually respresent GSR data.
"""


def gsr_response(stream_id: uuid, start_time: datetime, end_time: datetime, label_attachment: str, label_off: str, CC_obj: CerebralCortex, config: dict) -> str:
    """
    This method analyzes Galvanic skin response to label a window as improper attachment or sensor-off-body
    :param stream_id: UUID
    :param start_time:
    :param end_time:
    :param label_attachment:
    :param label_off:
    :param CC_obj:
    :param config:
    :return: string
    """
    datapoints = CC_obj.get_datastream(stream_id, start_time=start_time, end_time=end_time, type="data")

    vals = []
    for dp in datapoints:
        vals.append(dp.sample)

    if stat.median(stat.array(vals)) < config["attachment_marker"]["improper_attachment"]:
        return label_attachment
    elif stat.median(stat.array(vals)) > config["attachment_marker"]["gsr_off_body"]:
        return label_off