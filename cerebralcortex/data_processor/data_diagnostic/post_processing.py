from cerebralcortex.kernel.datatypes.datastream import *
from cerebralcortex.configuration import Configuration

import json


def store(parent_stream_id, data, CC_obj, stream_name):
    input_streams = {"name": stream_name, "id": parent_stream_id};
    stream_uuid = 12348695

    if stream_name == "ecg":
        atch = attachment_marker("ecg", input_streams, stream_uuid)
    elif stream_name == "rip":
        atch = attachment_marker("rip", input_streams, stream_uuid)
    elif stream_name == "motionsense":
        atch = attachment_marker("motionsense", input_streams, stream_uuid)
    else:
        raise ValueError("Incorrect sensor type")

    data_descriptor = json.loads(atch["dd"])
    execution_context = json.loads(atch["ec"])
    annotations = json.loads(atch["ann"])

    metadata = CC_obj.get_datastream(parent_stream_id, type="metadata")

    owner = metadata._owner
    name = execution_context["execution_context"]["processing_module"]["output_streams"][0]["name"]
    description = "This field is redundant and shall be removed"
    stream_type = "datastream"
    datapoints = map_data_to_datapoints(data)

    ds = DataStream(stream_uuid, owner, name, description, data_descriptor, execution_context, annotations,
                    stream_type, datapoints)

    CC_obj.save_datastream(ds)


def attachment_marker(type, input_streams, generated_stream_id):
    config = Configuration(filepath="data_diagnostic_config.yml").config

    #if type == "ecg" or type == "rip":
    if type == "ecg":
        name = 'ecg_attachment_marker'
        input_param = {"window_size": config["general"]["window_size"],
                           "ecg_vairance_threshold": config["attachment_marker"]["ecg_on_body"]}
    elif type == "rip":
        name = 'rip_attachment_marker'
        input_param = {"window_size": config["general"]["window_size"],
                           "rip_vairance_threshold": config["attachment_marker"]["rip_on_body"]}

    elif type == "motionsense":
        name = 'motionsense_attachment_marker'
        input_param = {"window_size": config["general"]["window_size"],
                       "motionsense_vairance_threshold": config["attachment_marker"]["motionsense_on_body"]}

    else:
        raise ValueError("Incorrect sensor type")

    output_stream = [{"name": name, "id": generated_stream_id}];
    algo_description = 'This algorithm uses variance of a windowed signals to mark the window as on/off body or improperly attached.'
    module_description = 'This is a data-diagnostic module that helps to identify the causes of missing data.'
    method = 'cerebralcortex.data_processor.data_diagnostic.attachment_marker'

    ec = get_execution_context(name, module_description, input_param, input_streams, output_stream, method,
                               algo_description)
    dd = get_data_descriptor()
    ann = get_annotations()

    return {"ec": ec, "dd": dd, "ann": ann}


def battery_data_marker():
    pass


def packet_loss_marker():
    pass


def sensor_unavailable():
    pass


def get_data_descriptor():
    data_descriptor = {
        "data_descriptor": [
            {
                "type": "number",
                "unit": "none"
            }
        ]
    }
    return json.dumps(data_descriptor)


def get_execution_context(name, module_description, input_param, input_streams, output_streams, method,
                          algo_description):
    author = ["Nasir Ali"]
    version = '0.0.1'
    ref = 'url of pub'
    execution_context = {
        "execution_context": {
            "processing_module": {
                "name": name,
                "description": module_description,
                "input_parameters": input_param,
                "input_streams": input_streams,
                "output_streams": output_streams,
                "algorithm": {
                    "method": method,
                    "description": algo_description,
                    "authors": author,
                    "version": version,
                    "reference": ref
                }
            }
        }
    }
    return json.dumps(execution_context)


def get_annotations():
    annotations = {
        "annotations": [
            {
                "name": "study",
                "identifier": "5b7fb6f3-7bf6-4031-881c-a25faf112dd9"
            },
            {
                "name": "privacy",
                "ssssss": "ooooooo"
            }
        ]
    }
    return json.dumps(annotations)


def map_data_to_datapoints(data):
    datapoint_list = []
    for key, value in data.items():
        datapoint_list.append(DataPoint(key[0], key[1], value))
    return datapoint_list
