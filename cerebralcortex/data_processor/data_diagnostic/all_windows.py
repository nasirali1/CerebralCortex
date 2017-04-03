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

import math
from collections import OrderedDict
from datetime import datetime, timedelta
from typing import List

import pytz

from cerebralcortex.kernel.datatypes.datapoint import DataPoint

class All_Windows:
    def window(self, data: List[DataPoint],
               window_size: float) -> OrderedDict:
        start_time = data[0].start_time
        end_time = data[len(data)-1].start_time

        self.create_blank_windows(data, window_size, start_time, end_time);


    def create_blank_windows(self, data, window_size, start_time, end_time):
        time_delta = (end_time-start_time).total_seconds()
        total_windows = math.floor(time_delta/window_size)
        print(total_windows)
        end_time2 = start_time
        for i in range(total_windows):
            start_time = end_time2
            end_time2 = start_time + timedelta(seconds=window_size)

            data2 = [i for i in data if start_time<= i.start_time and i.start_time <= end_time2]
            if not data2:
                print(str(start_time)+""+str(end_time2)+" NO DATA")
            else:
                print(str(start_time)+""+str(end_time2)+" - "+str(data2))
            # for j in range(len(data)):
            #     #print(j)
            #     if start_time<= data[j].start_time and data[j].start_time <= end_time2:
            #         print(str(start_time) +" - "+str(end_time2))
            #         #data.pop(j)
            #         #continue
            #     print("IN "+str(start_time))
            # print("out "+str(start_time))
            # for j in self.simple_gen(data, start_time, end_time2):
            #     print(j)
            # print("out "+str(start_time))

    def simple_gen(self,data, st, et):
        for j in range(len(data)):
            if st<= data[j].start_time and data[j].start_time <= et:
                yield str(st) +" - "+str(et)
            #print(st)
            #print(str(len(data))+"yild "+str(j))
            print("IN "+str(st))

