import numpy as np


def WirelessDisconnection(accelerometer_data_window, caller_method):
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

def autoSenseWirelessDC():
    pass



