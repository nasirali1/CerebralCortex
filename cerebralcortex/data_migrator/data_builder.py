# Copyright (c) 2017, MD2K Center of Excellence
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


import bz2
import datetime

from pytz import timezone
from typing import List

from cerebralcortex.kernel.datatypes.datastream import DataPoint


def bz2file_to_datapoints(filename: str) -> List[DataPoint]:
    """
    Read bz2 compressed files and map the data to Datapoints structure
    :param filename:
    :return:
    """
    datapoints = []
    bz_file = bz2.BZ2File(filename)

    for line in bz_file:
        tuple = line.decode("utf-8").replace("\r\n", "").split(
            ",")  # str(line).replace("b", "").replace("\\r\\n", "").replace("\'", "").split(",")
        if (len(tuple) == 5):
            sample = str([tuple[2], tuple[3], tuple[4]])
        else:
            sample = str([tuple[2]])

        start_time = datetime.datetime.fromtimestamp(int(tuple[0]) / 1000)
        localtz = timezone('US/Central')
        start_time = localtz.localize(start_time)
        end_time = ""

        datapoints.append(DataPoint(start_time=start_time, end_time=end_time, sample=sample))

    return datapoints
