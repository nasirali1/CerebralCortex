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

def phoneBatteryMarker(battery_levels: list, window_size: int) -> str:
    # TO-DO: if battery levels are empty for the whole window then check for the previous marked window
    # and mark this window as the previous one

    """

    :param battery_levels:
    :param window_size:
    :return:
    """
    if not battery_levels:
        pass

    phone_battery_down = 0
    phone_battery_charged = 0

    for val in battery_levels:
        if val < 10:
            ++phone_battery_down
        elif val > 50:
            ++phone_battery_charged

    battery_down = phone_battery_down / len(battery_levels)
    battery_charged = phone_battery_charged / len(battery_levels)

    if battery_down > 0.50:
        return "phone-battery-down"
    elif battery_charged > 0.80:
        return "phone-powered-off"


def autosenseBatteryMarker(battery_levels: list, window_size: int) -> str:
    """

    :param battery_levels:
    :param window_size:
    :return:
    """
    sensor_battery_down = 0
    sensor_battery_charged = 0

    for val in battery_levels:
        # ADC value to voltage
        # Values (Min=0 and Max=6) in battery voltage.
        voltageValue = (val / 4096) * 3 * 2

        if voltageValue <= 2:
            ++sensor_battery_down
        elif voltageValue > 2:
            ++sensor_battery_charged

    battery_down = sensor_battery_down / len(battery_levels)
    battery_charged = sensor_battery_charged / len(battery_levels)

    if battery_down > 0.50:
        return "sensor-battery-down"
    elif battery_charged > 0.80:
        return "sensor-powered-off"


def motionSenseBatteryMarker():
    # same as phone-battery-marker
    pass
