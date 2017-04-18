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

from cerebralcortex.kernel.DataStoreEngine.Metadata.Metadata import Metadata
from cerebralcortex.kernel.datatypes.datastream import DataStream

class StoreData:
    def store_stream(self, datastream: DataStream):
        """

        :param datastream:
        """
        stream_identifier = datastream.identifier
        ownerID = datastream.user
        name = datastream.name
        data_descriptor = datastream.data_descriptor
        execution_context = datastream.execution_context
        annotations = datastream.annotations
        stream_type = datastream.datastream_type
        data = datastream.data



        if data:
            Metadata(self.configuration).store_stream_info(stream_identifier, ownerID, name,
                                                           data_descriptor, execution_context,
                                                           annotations,
                                                           stream_type)
            dataframe = self.map_datapoint_to_dataframe(stream_identifier, data)

            self.store_data(dataframe, self.datapointTable)

    def store_data(self, dataframe_data: object, table_name: str):
        """
        :param dataframe_data: pyspark Dataframe
        :param table_name: Cassandra table name
        """

        if table_name == "":
            raise Exception("Table name cannot be null.")
        elif dataframe_data == "":
            raise Exception("Data cannot be null.")

        dataframe_data.write.format("org.apache.spark.sql.cassandra") \
            .mode('append') \
            .options(table=table_name, keyspace=self.keyspaceName) \
            .save()


    def map_datapoint_to_dataframe(self, stream_id, datapoints):
        temp = []
        for i in datapoints:
            day = i.start_time
            day = day.strftime("%Y%m%d")
            dp = str(stream_id), day, i.start_time, i.end_time, i.sample
            temp.append(dp)

        temp_RDD = self.sparkContext.parallelize(temp)
        df = self.sqlContext.createDataFrame(temp_RDD,
                                             ["identifier", "day", "start_time", "end_time", "sample"])

        return df


