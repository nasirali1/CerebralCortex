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
import uuid

class StoreMetadata:

    # stream_identifier, ownerID, name,
    # data_descriptor, execution_context,
    # annotations,
    # stream_type

    def store_stream_info(self, stream_identifier: int = None, stream_owner_id: str = None, name: str = None, description: str= None,
                          data_descriptor: dict = None,
                          execution_context: dict = None,
                          annotations: dict = None, stream_type: str = None):
        """
        This method will update a record if stream already exist else it will insert a new record.
        :param stream_identifier:
        :param stream_owner_id:
        :param name:
        :param description:
        :param data_descriptor:
        :param execution_context:
        :param annotations:
        :param stream_type:
        """

        isStreamCreated = self.is_stream_created(stream_identifier, stream_owner_id, name, description, data_descriptor, execution_context, stream_type)

        if (isStreamCreated == True):
            qry = "UPDATE " + self.datastreamTable + " set annotations=JSON_ARRAY_APPEND(annotations, '$',  '" + self.cleanJson(annotations) + "') where identifier=" + str(stream_identifier)
        else:
            qry = "INSERT INTO " + self.datastreamTable + " (identifier, owner, name, description, data_descriptor, execution_context, annotations, type) VALUES('" + str(
                stream_identifier) + "','" + str(stream_owner_id) + "','" + str(name) + "','" + str(
                description) + "','" + str(json.dumps(data_descriptor)) + "','" + str(json.dumps(execution_context)) + "', '"+json.dumps(annotations)+"', '"+stream_type+"'"

        self.cursor.execute(qry)
        self.dbConnection.commit()
        self.cursor.close()
        self.dbConnection.close()

    def is_stream_created(self, stream_identifier: uuid, stream_owner_id: uuid, name: str, description: str, data_descriptor: dict,
                          execution_context: dict,
                          stream_type: str):
        """
        This method will check if the stream already exist with the same data (as provided in params) except annotations.
        :param stream_identifier:
        :param stream_owner_id:
        :param name:
        :param description:
        :param data_descriptor:
        :param execution_context:
        :param stream_type:
        """
        qry = "select * from "+self.datastreamTable+" where identifier="+stream_identifier

        self.cursor.execute(qry)
        result = self.cursor.fetchall()

        if(result[0][0]==stream_identifier):
            if(result[0][1]!=stream_owner_id):
                raise "Update failed: owner ID is not same.."
            elif (result[0][2] != name):
                raise "Update failed: name is not same.."
            elif (result[0][3] != description):
                raise "Update failed: description is not same.."
            elif (sorted(json.loads(str(result[0][4])).items()) != sorted(json.loads(json.dumps(data_descriptor)).items())):
                raise "Update failed: data descriptor is not same."
            elif (sorted(json.loads(str(result[0][5])).items()) != sorted(json.loads(json.dumps(execution_context)).items())):
                raise "Update failed: execution context is not same."
            elif (result[0][7] != stream_type):
                raise "Update failed: type is not same."
            else:
                return True
        else:
            return False

    def cleanJson(self, jsonObj):
        cleaned = json.dumps(jsonObj).strip().replace('\\"','\"')
        return cleaned