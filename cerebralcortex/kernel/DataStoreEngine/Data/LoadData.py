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

import json
from datetime import datetime
from pytz import timezone

from cerebralcortex.kernel.DataStoreEngine.Metadata.Metadata import Metadata
from cerebralcortex.kernel.datatypes.datastream import *

class LoadData:

    def get_stream(self, stream_id: int, start_time: int = "", end_time: int = "") -> DataStream:

        """
        :param stream_id:
        :param start_time:
        :param end_time:
        :return: spark dataframe
        """
        stream_id = str(stream_id)
        start_time = str(start_time)
        end_time = str(end_time)

        where_clause = "identifier=" + stream_id

        if stream_id == "":
            raise Exception("Stream identifier cannot be null.")

        if start_time != "":
            where_clause += " and start_time>='" + str(start_time) + "'"

        if end_time != "":
            where_clause += " and end_time<='" + str(end_time) + "'"

        #where_clause += " order by start_time"

        datapoints = self.map_dataframe_to_datapoint(self.load_data_from_cassandra(self.datapointTable, where_clause))
        stream = self.map_datapoint_and_metadata_to_datastream(stream_id, datapoints)

        return stream



    def map_dataframe_to_datapoint(self, dataframe: object) -> list:
        """
        Converts a PySpark DataFrame into a list of datapoint objects
        :param dataframe:
        :return: list of datapoint objects
        """
        datapointsList = []
        rows = dataframe.collect()
        for row in rows:
            #dp = DataPoint(self.get_epoch_time(row["start_time"]), self.get_epoch_time(row["end_time"]), row["sample"])
            localtz = timezone('US/Central')
            start_time = localtz.localize(row["start_time"])
            #print(row["end_time"])
            if row["end_time"]!=None:
                end_time = localtz.localize(row["end_time"])
            else:
                end_time = ""
            #d1 = row["start_time"].replace(tzinfo=pytz.UTC)
            #d2 = row["start_time"].replace(tzinfo=pytz.UTC)
            dp = DataPoint(start_time, end_time, row["sample"])
            datapointsList.append(dp)
        return datapointsList

    def map_datapoint_and_metadata_to_datastream(self, stream_id: int, data: list) -> DataStream:
        """
        This method will map the datapoint and metadata to datastream object
        :param stream_id:
        :param data: list
        :return: datastream object
        """

        # query datastream(mysql) for metadata
        datastream_info = Metadata(self.configuration).get_stream_info(stream_id)

        ownerID = datastream_info[0][1]
        name = datastream_info[0][2]
        description = datastream_info[0][3]
        data_descriptor = json.loads(datastream_info[0][4])
        execution_context = json.loads(datastream_info[0][5])
        annotations = json.loads(datastream_info[0][6])
        stream_type = datastream_info[0][7]

        return DataStream(stream_id, ownerID, name, description, data_descriptor, execution_context, annotations, stream_type, data)

    def load_data_from_cassandra(self, table_name: str, where_clause: str) -> object:
        """
        Establish connection with cassandra, load data, and filter based on the condition passed in whereClause argument
        :return:
        :param table_name:
        :param where_clause:
        :return: spark dataframe
        """
        #TO-DO, replace .filter with .where() for performance
        dataframe = self.sqlContext.read.format("org.apache.spark.sql.cassandra").options(table=table_name,
                                                                                          keyspace=self.keyspaceName).load().select("start_time", "end_time", "sample").filter(
            where_clause).orderBy('start_time', ascending=True)

        return dataframe

    def get_epoch_time(self, dt: datetime) -> datetime:
        """
        :param dt:
        :return:
        """
        epoch = datetime.utcfromtimestamp(0)
        return (dt - epoch).total_seconds() * 1000.0