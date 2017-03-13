import numpy as np

def variance_based_data_quality(window_data):
    """
    This method accepts one window at a time
    :param raw_sensor_data:
    """
    #remove outliers from the window data
    normal_values = outlier_detection(window_data)

    #TO-DO: move all threshold values in config
    if np.var(normal_values) < 0.7:
        return "off-body"

    return "on-body"


def outlier_detection(signal_values):
    if not signal_values:
        return

    median = np.median(signal_values)
    standard_deviation = np.std(signal_values)
    normal_values = ""

    for val in signal_values:
        if (abs(val) - median) < standard_deviation:
            normal_values.extend(val)

    return normal_values

variance_based_data_quality([1,2,3])