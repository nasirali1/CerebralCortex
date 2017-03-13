
def phoneBatteryMarker(window_data, window_size):

    #mark window as battery down if 33% of the battery data was available
    # else mark window as phone powered-off
    data_available = len(window_data)/window_size
    if data_available < 0.20 & data_available>0.5:
        return "battery-down"
    else:
        return "phone-off"



def senseBatteryMarker():
    pass

def motionSenseBatteryMarker():
    pass