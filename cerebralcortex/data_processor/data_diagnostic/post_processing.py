from cerebralcortex.kernel.datatypes.datastream import *
from cerebralcortex.configuration import Configuration

import json
import uuid


def store(parent_stream_id, data, CC_obj, config, stream_name, algo_type):
    if isinstance(parent_stream_id, list):
        #in sensor-unavailable algos, I simply passed whole input stream object
        input_streams = parent_stream_id
        parent_stream_id = input_streams[0]["id"]
    else:
        input_streams = [{"name": stream_name, "id": str(parent_stream_id)}];


    """TO-DO"""
    stream_uuid = 123  # uuid.uuid4()
    result = dd(algo_type, stream_name, config, input_streams, stream_uuid)

    # if stream_name == "ecg" or stream_name == "autosense":
    #
    # elif stream_name == "rip" or stream_name == "autosense":
    #     dd(algo_type, stream_name, config, input_streams, stream_uuid)
    #     #atch = attachment_marker("rip", input_streams, stream_uuid)
    # elif stream_name == "motionsense":
    #     #atch = attachment_marker("motionsense", input_streams, stream_uuid)
    #     dd(algo_type, stream_name, config, input_streams, stream_uuid)
    # elif stream_name == "phone":
    #     #only battery
    #     pass
    # else:
    #     raise ValueError("Incorrect sensor type")

    data_descriptor = json.loads(result["dd"])
    execution_context = json.loads(result["ec"])
    annotations = json.loads(result["ann"])

    metadata = CC_obj.get_datastream(parent_stream_id, type="metadata")

    owner = metadata._owner
    name = execution_context["execution_context"]["processing_module"]["output_streams"][0]["name"]
    description = "This field is redundant and shall be removed"
    stream_type = "datastream"
    datapoints = map_data_to_datapoints(data)

    ds = DataStream(stream_uuid, owner, name, description, data_descriptor, execution_context, annotations,
                    stream_type, datapoints)

    CC_obj.save_datastream(ds)


def dd(algo_type, stream_name, config, input_streams, stream_uuid):
    if algo_type == config["algo_names"]["attachment_marker"]:
        result = attachment_marker(stream_name, input_streams, stream_uuid)
    elif algo_type == config["algo_names"]["battery_marker"]:
        result = battery_data_marker(stream_name, input_streams, stream_uuid)
    elif algo_type == config["algo_names"]["sensor_unavailable_marker"]:
        pass
    elif algo_type == config["algo_names"]["packet_loss_marker"]:
        result = packet_loss_marker(stream_name, input_streams, stream_uuid)
    return result


def attachment_marker(type, input_streams, generated_stream_id):
    config = Configuration(filepath="data_diagnostic_config.yml").config

    # if type == "ecg" or type == "rip":
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

    output_stream = [{"name": name, "id": str(generated_stream_id)}];
    algo_description = 'This algorithm uses variance of a windowed signals to mark the window as on/off body or improperly attached.'
    module_description = 'This is a data-diagnostic module that helps to identify the causes of missing data.'
    method = 'cerebralcortex.data_processor.data_diagnostic.attachment_marker'

    ec = get_execution_context(name, module_description, input_param, input_streams, output_stream, method,
                               algo_description)
    dd = get_data_descriptor()
    ann = get_annotations()

    return {"ec": ec, "dd": dd, "ann": ann}


def battery_data_marker(type, input_streams, generated_stream_id):
    config = Configuration(filepath="data_diagnostic_config.yml").config

    if type == "phone":
        name = 'phone_battery_marker'
        input_param = {"window_size": config["general"]["window_size"],
                       "phone_powered_off_threshold": config["battery_marker"]["phone_powered_off"],
                       "phone_battery_down_threshold": config["battery_marker"]["phone_powered_down"]}
    elif type == "autosense":
        name = 'autosense_battery_marker'
        input_param = {"window_size": config["general"]["window_size"],
                       "autosense_powered_off_threshold": config["battery_marker"]["autosense_powered_off"],
                       "autosense_battery_down_threshold": config["battery_marker"]["autosense_powered_down"]}

    elif type == "motionsense":
        name = 'motionsense_battery_marker'
        input_param = {"window_size": config["general"]["window_size"],
                       "motionsense_powered_off_threshold": config["battery_marker"]["motionsense_powered_off"],
                       "motionsense_battery_down_threshold": config["battery_marker"]["motionsense_powered_down"]}
    else:
        raise ValueError("Incorrect sensor type")

    output_stream = [{"name": name, "id": str(generated_stream_id)}];
    algo_description = 'This algorithm uses battery levels to label when the batter was down or device was powered off.'
    module_description = 'This is a data-diagnostic module that helps to identify the causes of missing data.'
    method = 'cerebralcortex.data_processor.data_diagnostic.BatteryDataMarker'

    ec = get_execution_context(name, module_description, input_param, input_streams, output_stream, method,
                               algo_description)
    dd = get_data_descriptor()
    ann = get_annotations()
    return {"ec": ec, "dd": dd, "ann": ann}


def packet_loss_marker(type, input_streams, generated_stream_id):
    config = Configuration(filepath="data_diagnostic_config.yml").config

    if type == "ecg":
        name = 'ecg_packet_loss_marker'
        input_param = {"window_size": config["general"]["window_size"],
                       "ecg_acceptable_packet_loss": config["packet_loss_marker"]["ecg_acceptable_packet_loss"]}
    elif type == "rip":
        name = 'rip_packet_loss_marker'
        input_param = {"window_size": config["general"]["window_size"],
                       "rip_acceptable_packet_loss": config["packet_loss_marker"]["rip_acceptable_packet_loss"]}

    elif type == "motionsense":
        name = 'motionsense_packet_loss_marker'
        input_param = {"window_size": config["general"]["window_size"],
                       "rip_acceptable_packet_loss": config["packet_loss_marker"]["motionsense_acceptable_packet_loss"]}
    else:
        raise ValueError("Incorrect sensor type")

    output_stream = [{"name": name, "id": str(generated_stream_id)}];
    algo_description = 'This algorithm mark a window as packet-loss if received packets in a window is less than the acceptable packet loss threshold.'
    module_description = 'This is a data-diagnostic module that helps to identify the causes of missing data.'
    method = 'cerebralcortex.data_processor.data_diagnostic.packet_loss_marker'

    ec = get_execution_context(name, module_description, input_param, input_streams, output_stream, method,
                               algo_description)
    dd = get_data_descriptor()
    ann = get_annotations()
    return {"ec": ec, "dd": dd, "ann": ann}


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
    author = ["Ali"]
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
                "name": "study",
                "identifier": "5b7fb6f3-7bf6-4031-881c-a25faf112dd9"
            }
        ]
    }
    return json.dumps(annotations)


def map_data_to_datapoints(data):
    datapoint_list = []
    for key, value in data.items():
        datapoint_list.append(DataPoint(key[0], key[1], value))
    return datapoint_list
