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

from collections import OrderedDict
from datetime import datetime, timedelta
from typing import List


from cerebralcortex.kernel.datatypes.datapoint import DataPoint


class All_Windows:
    def window(self, data: List[DataPoint],
               window_size: float) -> OrderedDict:

        windowed_datastream = OrderedDict()
        for key, data in self.create_all_windows(data, window_size, ""):
            windowed_datastream[key] = data
            print(key, data)

    def create_all_windows(self, datapoint, window_size, window_offset: float):
        window_start_time = datapoint[0].start_time
        window_end_time = window_start_time + timedelta(seconds=window_size)
        window_data = []
        for dp in datapoint:
            if window_start_time <= dp.start_time <= window_end_time:
                window_data.append(dp)
            else:
                key = (window_start_time, window_end_time)
                yield key, window_data
                # when datapoint is not in current range, identify emtpy windows and yield.
                _w = window_end_time
                _w_end = _w + timedelta(seconds=window_size)
                while dp.start_time > _w_end:
                    key = (_w, _w_end)
                    yield key, []
                    window_data = []
                    _w = _w_end
                    _w_end = _w + timedelta(seconds=window_size)

                window_data.append(dp)
                window_end_time = _w_end
                window_start_time = _w
        key = (window_start_time, window_end_time)
        yield key, window_data
