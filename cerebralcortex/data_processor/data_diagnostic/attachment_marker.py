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

import statistics as stat

from cerebralcortex.data_processor.signalprocessing.window import window
from cerebralcortex.data_processor.data_diagnostic.util import *
from cerebralcortex.data_processor.data_diagnostic.post_processing import *


def attachment_marker(stream_id, CC_obj, config) -> OrderedDict:
    """
    This method accepts one window at a time
    :param datapoints:
    :param window_size: in seconds
    :param type: acceptable types are: phone, autosense, motionsense
    :return: OrderedDict representing [(st,et),[label],
                                       (st,et),[label],
                                        ...]
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


"""TO-DO"""


# This method is not being used. Need to make sure whether GSR values actually respresent GSR data.
def gsr_response(stream_id, start_time, end_time, label_attachment, label_off, CC_obj, config):
    datapoints = CC_obj.get_datastream(stream_id, start_time=start_time, end_time=end_time, type="data")

    vals = []
    for dp in datapoints:
        vals.append(dp.sample)

    if stat.median(stat.array(vals)) < config["attachment_marker"]["improper_attachment"]:
        return label_attachment
    elif stat.median(stat.array(vals)) > config["attachment_marker"]["gsr_off_body"]:
        return label_off


def outlier_detection(window_data: list) -> list:
    """
    removes outliers from a list
    This algorithm is modified version of Chauvenet's_criterion (https://en.wikipedia.org/wiki/Chauvenet's_criterion)
    :param window_data:
    :return:
    """
    if not window_data:
        raise ValueError("List is empty.")

    vals = []
    for dp in window_data:
        vals.append(float(dp.sample))

    median = stat.median(vals)
    standard_deviation = stat.stdev(vals)
    normal_values = list()

    for val in window_data:
        if (abs(float(val.sample)) - median) < standard_deviation:
            normal_values.append(float(val.sample))

    return normal_values
