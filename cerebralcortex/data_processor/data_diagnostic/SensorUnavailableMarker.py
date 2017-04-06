import numpy as np
import math

from cerebralcortex.kernel.datatypes.datapoint import DataPoint
from cerebralcortex.data_processor.signalprocessing.window import window

def autosense_calculate_magnitude(accel_x, accel_y, accel_z):
    datapointsList = []
    max_list_size = len(max(accel_x, accel_y, accel_z, key=len))

    for i in range(max_list_size):
        x = 0 if len(accel_x) - 1 < i else float(accel_x[i].sample)
        y = 0 if len(accel_y) - 1 < i else float(accel_y[i].sample)
        z = 0 if len(accel_z) - 1 < i else float(accel_z[i].sample)

        if len(accel_x) == max_list_size:
            start_time = accel_x[i].start_time
        elif len(accel_y) == max_list_size:
            start_time = accel_y[i].start_time
        elif len(accel_z) == max_list_size:
            start_time = accel_z[i].start_time

        magnitude = math.sqrt(math.pow(x, 2) + math.pow(y, 2) + math.pow(z, 2));

        dp = DataPoint(start_time, '', magnitude)
        datapointsList.append(dp)


    return datapointsList
    # windowed_data = window(datapointsList, window_size, False)
    #
    # del accel_x[:]
    # del accel_y[:]
    # del accel_z[:]
    # del datapointsList[:]
    #
    # WirelessDisconnection(datapointsList, "autoSenseWirelessDC")
    # print("wow")

    #print("done")

def WirelessDisconnection(accelerometer_data_window, CC_obj, caller_method):
    # pass windows that are marked as sensor-powered off
    # also a previous window before sensor-powered off to analyze whether
    # the disconnection was due to power-off or wireless disconnection

    """
    This method will analyze whether a disconnection was due to a wireless disconnection
    or due to sensor powered off.
    :param accelerometer_data_window:
    :param caller_method:
    :return:
    """

    autosense_battery_dc = CC_obj.get_datastream(7664, type="data")

    if autosense_battery_dc.start_time!="" and autosense_battery_dc.end_time!="":
        autosense_acc_x = CC_obj.get_datastream(7664, start_time=autosense_battery_dc.start_time, end_time=autosense_battery_dc.end_time, type="data")
        autosense_acc_y = CC_obj.get_datastream(7669, start_time=autosense_battery_dc.start_time, end_time=autosense_battery_dc.end_time, type="data")
        autosense_acc_z = CC_obj.get_datastream(7673, start_time=autosense_battery_dc.start_time, end_time=autosense_battery_dc.end_time, type="data")

        magnitude = autosense_calculate_magnitude(autosense_acc_x, autosense_acc_y, autosense_acc_z)

    threshold = 0
    if caller_method == "autoSenseWirelessDC":
        threshold = 4000
    elif caller_method == "motionsenseWirelessDC":
        threshold = 0.005

    tmp = np.var(accelerometer_data_window);

    if tmp > threshold:
        return "sensor-unavailable"
    else:
        return "sensor-powered-off"

def motionsenseWirelessDC(sensor_powed_off_windows):
    pass