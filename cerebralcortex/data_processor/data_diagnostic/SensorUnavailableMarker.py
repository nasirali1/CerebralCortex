import numpy as np
import math

from cerebralcortex.kernel.datatypes.datapoint import DataPoint
from cerebralcortex.data_processor.signalprocessing.window import window



def WirelessDisconnection(stream_id, CC_obj, window_size, type):
    #if the type is autosense then pass the stream-id of autosense. This method will automatically load related accelerometer value


    """
    This method will analyze whether a disconnection was due to a wireless disconnection
    or due to sensor powered off.
    :param accelerometer_data_window:
    :param type:
    :return:
    """
    datapointsList = []
    threshold = 0

    """TO-DO"""
    #find accelerometer stream id(s) and sensor-battery-off stream-id of a given stream_id

    if type == "autosense":
        threshold = 4000
    elif type == "motionsense":
        threshold = 0.005

    autosense_battery_off = CC_obj.get_datastream(7664, type="data")

    for dp in range(len(autosense_battery_off)):
        if autosense_battery_off.start_time!="" and autosense_battery_off.end_time!="":
            #get a window prior to a battery powered off
            start_time = autosense_battery_off.start_time - window_size
            end_time = autosense_battery_off.start_time

            autosense_acc_x = CC_obj.get_datastream(7664, start_time=start_time, end_time=end_time, type="data")
            autosense_acc_y = CC_obj.get_datastream(7669, start_time=start_time, end_time=end_time, type="data")
            autosense_acc_z = CC_obj.get_datastream(7673, start_time=start_time, end_time=end_time, type="data")

            magnitudeVals = autosense_calculate_magnitude(autosense_acc_x, autosense_acc_y, autosense_acc_z)


        if np.var(magnitudeVals) > threshold:
            datapointsList.append(DataPoint(autosense_battery_off.start_time, autosense_battery_off.end_time, "sensor-unavailable"))
        #     return "sensor-unavailable"
        # else:
        #     return "sensor-powered-off"

def autosense_calculate_magnitude(accel_x, accel_y, accel_z):
    magnitudeList = []
    max_list_size = len(max(accel_x, accel_y, accel_z, key=len))

    for i in range(max_list_size):
        x = 0 if len(accel_x) - 1 < i else float(accel_x[i].sample)
        y = 0 if len(accel_y) - 1 < i else float(accel_y[i].sample)
        z = 0 if len(accel_z) - 1 < i else float(accel_z[i].sample)

        # if len(accel_x) == max_list_size:
        #     start_time = accel_x[i].start_time
        # elif len(accel_y) == max_list_size:
        #     start_time = accel_y[i].start_time
        # elif len(accel_z) == max_list_size:
        #     start_time = accel_z[i].start_time

        magnitude = math.sqrt(math.pow(x, 2) + math.pow(y, 2) + math.pow(z, 2));

        magnitudeList.append(magnitude)


    return magnitudeList
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

"""TO-DO"""
#Write a separate method for motionsense magnitude calculation
def motionsenseWirelessDC(sensor_powed_off_windows):
    pass