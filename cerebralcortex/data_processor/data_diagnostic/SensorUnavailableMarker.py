import numpy as np
import math
from datetime import datetime, timedelta

from cerebralcortex.kernel.datatypes.datapoint import DataPoint
from cerebralcortex.kernel.DataStoreEngine.Metadata.Metadata import Metadata
from cerebralcortex.data_processor.data_diagnostic.util import *
from cerebralcortex.data_processor.data_diagnostic.post_processing import *


def WirelessDisconnection(stream_id, CC_obj, config, type: str):
    #if the type is autosense then pass the stream-id of autosense. This method will automatically load related accelerometer value
    #stream_id should be of "battery-powered-off"


    """
    This method will analyze whether a disconnection was due to a wireless disconnection
    or due to sensor powered off.
    :param accelerometer_data_window:
    :param type:
    :return:
    """
    datapointsList = []
    results = OrderedDict()
    threshold = 0

    #stream = CC_obj.get_datastream(stream_id, type="all")
    #windowed_data = window(stream.data, config['general']['window_size'], True)

    """TO-DO"""
    #find accelerometer stream id(s) and sensor-battery-off stream-id of a given stream_id
    stream_info = CC_obj.get_datastream(stream_id, type="metadata")

    owner_id = stream_info._owner
    """TO-DO: change type variable with this name (after finalizing the standard stream names)"""
    stream_name = stream_info._name


    if type == "ecg":
        threshold = config['sensor_unavailable_marker']['ecg']
        battery_off_stream_name = config['battery_marker']['autosense_powered_off']
        label =  config['labels']['autosense_unavailable']
    if type == "rip":
        threshold = config['sensor_unavailable_marker']['tip']
        battery_off_stream_name = config['battery_marker']['autosense_powered_off']
        label =  config['labels']['autosense_unavailable']
    elif type == "motionsense":
        threshold = config['sensor_unavailable_marker']['motionsense']
        battery_off_stream_name = config['battery_marker']['motionsense_powered_off']
        label =  config['labels']['motionsense_unavailable']

    battery_off_stream_id = Metadata.get_child_stream_id(owner_id, battery_off_stream_name)

    autosense_battery_off = CC_obj.get_datastream(battery_off_stream_id, type="metadata")


    for dp in range(len(autosense_battery_off)):
        if autosense_battery_off.start_time!="" and autosense_battery_off.end_time!="":
            #get a window prior to a battery powered off
            start_time = autosense_battery_off.start_time - timedelta(seconds=config['general']['window_size'])
            end_time = autosense_battery_off.start_time
            x = Metadata.get_autosense_accel_id_by_owner_id(owner_id, "x")
            y = Metadata.get_autosense_accel_id_by_owner_id(owner_id, "y")
            z = Metadata.get_autosense_accel_id_by_owner_id(owner_id, "z")
            autosense_acc_x = CC_obj.get_datastream(x, start_time=start_time, end_time=end_time, type="data")
            autosense_acc_y = CC_obj.get_datastream(y, start_time=start_time, end_time=end_time, type="data")
            autosense_acc_z = CC_obj.get_datastream(z, start_time=start_time, end_time=end_time, type="data")

            magnitudeVals = autosense_calculate_magnitude(autosense_acc_x, autosense_acc_y, autosense_acc_z)


        if np.var(magnitudeVals) > threshold:
            key = (autosense_battery_off.start_time, autosense_battery_off.end_time)
            results[key] = label

    input_streams = [{"name": stream_name, "id": str(stream_id)}, {"name": stream_name, "id": str(x)}, {"name": stream_name, "id": str(y)}, {"name": stream_name, "id": str(z)}]
    merged_windows = merge_consective_windows(results)
    store(input_streams, merged_windows, CC_obj, config, type, config["algo_names"]["sensor_unavailable_marker"])

def autosense_calculate_magnitude(accel_x, accel_y, accel_z):
    magnitudeList = []
    max_list_size = len(max(accel_x, accel_y, accel_z, key=len))

    for i in range(max_list_size):
        x = 0 if len(accel_x) - 1 < i else float(accel_x[i].sample)
        y = 0 if len(accel_y) - 1 < i else float(accel_y[i].sample)
        z = 0 if len(accel_z) - 1 < i else float(accel_z[i].sample)

        magnitude = math.sqrt(math.pow(x, 2) + math.pow(y, 2) + math.pow(z, 2));
        magnitudeList.append(magnitude)


    return magnitudeList

"""TO-DO"""
#Write a separate method for motionsense magnitude calculation
def motionsenseWirelessDC(sensor_powed_off_windows):
    pass