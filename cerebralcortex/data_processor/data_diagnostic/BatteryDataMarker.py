
def phoneBatteryMarker(window_data, window_size):

    #mark window as battery down if 33% of the battery data was available
    # else mark window as phone powered-off
    data_available = len(window_data)/window_size
    if data_available < 0.20 & data_available>0.5:
        return "battery-down"
    else:
        return "phone-off"



def senseBatteryMarker(window_data, window_size):

    sensor_battery_down = 0
    sensor_battery_off = 0

    for val in window_data:
        #ADC value to voltage
        #Values (Min=0 and Max=6) in battery voltage.
        voltageValue = ( val / 4096) * 3 * 2

        if voltageValue <= 2 & voltageValue>0:
            ++sensor_battery_down

    data_available = len(window_data)/window_size
    available_battery = sensor_battery_down / window_size

    if data_available < 0.05:
        return "sensor-powered-off"
    elif available_battery < 0.20:
        return "sensor-battery-down"

def motionSenseBatteryMarker():
    pass