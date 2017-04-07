from cerebralcortex.kernel.datatypes.datastream import *


def store(parent_stream_id, data, CC_obj):
    data_descriptor = {"data_descriptor":{}}
    execution_context = {"execution_context":{}}
    annotations = {"execution_context":{}}


    metadata = CC_obj.get_datastream(parent_stream_id, type="metadata")

    stream_uuid = 123
    #identifier = metadata._identifier
    owner = metadata._owner
    name = "attachment-marker"
    description = "Sensor on/off body status."
    stream_type = "annotation"
    datapoints = map_data_to_datapoints(data)

    data_descriptor["data_descriptor"] = [{"unit": "13", "type": "24"}]


    ds = DataStream(stream_uuid, owner, name, description, data_descriptor, execution_context, annotations,
                      stream_type, datapoints)

    CC_obj.save_datastream(ds)


def attachment_marker():
    pass

def battery_data_marker():
    pass

def packet_loss_marker():
    pass

def sensor_unavailable():
    pass


def map_data_to_datapoints(data):
    datapoint_list = []
    for key, value in data.items():
        datapoint_list.append(DataPoint(key[0], key[1], value))
    return datapoint_list