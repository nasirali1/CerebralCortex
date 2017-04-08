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


class LoadMetadata:

    def mySQLQueryBuilder(self, jsonQueryParam: dict) -> str:
        """
        :param jsonQueryParam:
            This method accepts a json object to build a datastore query. Use the following json schema:
            jsonQueryParam = {
                "columnNames": "col1, col2",
                "tableName": "table_name"
                "whereClause": "",
                "orderedByColumnName": "",
                "sortingOrder":"",
                "limitBy": ""
            }
        Where
            "columnNames" are the names of the columns you want to retrieve. Please pass * if you want to retrieve all the columns of a table. "columnNames" is a mandatory field and cannot be empty.
            "tableName" is the name of the database table
            "whereClause" is any condition you want to put on a query. For example, "datastream_id=1 and participant_id=2". This field is option and can be empty.
            "orderedByColumnName" is the name of a column that you want data to be sorted by. This field is option and can be empty.
            "sortingOrder" is the sorting order. Available sorting arguments ASC and DESC. This field is option and can be empty.
            "limitBy" is the number of records you want to retrieve. For example, 1, 10. This field is option and can be empty.

        Note: Please look at Cassandra database schema for available column names per table.
        :return SQL Query (string)
        """

        if (jsonQueryParam["columnNames"].strip() != ""):
            columnNames = jsonQueryParam["columnNames"].strip()
        else:
            raise ValueError("No column name(s) has been defined.")

        if (jsonQueryParam["tableName"].strip() == ""):
            raise ValueError("No table name has been defined.")

        if (jsonQueryParam["whereClause"].strip() != ""):
            whereClause = "where " + jsonQueryParam["whereClause"].strip()
        else:
            whereClause = ""

        if (jsonQueryParam["orderedByColumnName"].strip() != ""):
            orderedByColumnName = "ORDER BY " + jsonQueryParam["orderedByColumnName"].strip()
        else:
            orderedByColumnName = ""

        if (jsonQueryParam["sortingOrder"].strip() != ""):
            sortingOrder = jsonQueryParam["sortingOrder"].strip()
        else:
            sortingOrder = ""

        if (jsonQueryParam["sortingOrder"].strip() != ""):
            limitBy = jsonQueryParam["limitBy"].strip()
        else:
            limitBy = ""

        qry = "Select " + columnNames + " from " + jsonQueryParam[
            "tableName"] + " " + whereClause + " " + orderedByColumnName + " " + sortingOrder + " " + limitBy
        return qry

    def get_stream_info(self, stream_id, stream_owner_id: int = "", records_limit: str = "") -> list:
        """
        :param stream_id:
        :param stream_owner_id:
        :param processinModuleID:
        :param records_limit: range (e.g., 1,10 or 130,200)
        :return: list
        """
        whereClause = "identifier=" + str(stream_id)

        if (stream_owner_id != ""):
            whereClause += " and owner=" + str(stream_owner_id)

        jsonQueryParam = {
            "columnNames": "*",
            "tableName": self.datastreamTable,
            "whereClause": whereClause,
            "orderedByColumnName": "identifier",
            "sortingOrder": "ASC",
            "limitBy": records_limit
        }
        return self.executeQuery(self.mySQLQueryBuilder(jsonQueryParam))

    def get_user_info(self, user_id, records_limit: str = "") -> list:
        """
        :param user_id:
        :param records_limit: range (e.g., 1,10 or 130,200)
        :return: list
        """
        whereClause = "id=" + str(user_id)

        jsonQueryParam = {
            "columnNames": "*",
            "tableName": self.userTable,
            "whereClause": whereClause,
            "orderedByColumnName": "id",
            "sortingOrder": "ASC",
            "limitBy": records_limit
        }
        return self.executeQuery(self.mySQLQueryBuilder(jsonQueryParam))


    def executeQuery(self, qry: str) -> list:
        """
        :param qry: SQL Query
        :return: results of a query
        """
        self.cursor.execute(qry)
        results = self.cursor.fetchall()
        self.cursor.close()
        self.dbConnection.close()
        if len(results) == 0:
            raise "No record found."
        else:
            return results

    def get_child_stream_id(self, owner_id, name):
        # if stream name, id, and owner are same then return true
        #qry = "SELECT * from stream where JSON_SEARCH(execution_context, 'all', '"+parent_stream_id+"', null, '$.execution_context.processing_module.input_streams[*].id')  is not null and owner='"+owner_id+"' and name='"+name+"'"
        qry = "SELECT * from stream where owner='"+owner_id+"' and name='"+name+"'"
        vals = owner_id, name
        self.cursor.execute(qry)
        result = self.cursor.fetchall()
        if result:
            return result[0][0]
        else:
            return False
    """TO-DO: update accel names"""
    def get_autosense_accel_id_by_owner_id(self, owner_id, type):
        if type=="x":
            name = "autosense-x"
        elif type=="y":
            name = "autosense-y"
        elif type=="z":
            name = "autosense-z"
        elif type=="motionsense":
            name = "motionsense_accel"
        else:
            raise ValueError("Unknown type. Only acceptable types are x, y, z, or motionsense.")

        qry = "SELECT * from stream where owner='"+owner_id+"' and name='"+name+"'"
        vals = owner_id, name
        self.cursor.execute(qry)
        result = self.cursor.fetchall()
        if result:
            return result[0][0]
        else:
            return False