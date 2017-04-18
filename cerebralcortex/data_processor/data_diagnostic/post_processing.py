import json
import uuid

from cerebralcortex.kernel.datatypes.datastream import DataStream, Stream
from cerebralcortex.CerebralCortex import CerebralCortex
from cerebralcortex.data_processor.data_diagnostic.util import map_data_to_datapoints



def store(input_streams: dict, data: Stream, CC_obj: CerebralCortex, config: dict, algo_type: str):

    parent_stream_id = input_streams[0]["id"]
    stream_name = input_streams[0]["name"]


    """TO-DO: use dynamic UUID"""
    stream_uuid = 123  # uuid.uuid4()
    result = process_data(stream_uuid, stream_name, input_streams, algo_type, config )

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



def process_data(stream_uuid, stream_name, input_streams, algo_type, config):

    if algo_type == config["algo_names"]["attachment_marker"]:
        result = attachment_marker(stream_uuid, stream_name, input_streams, config)
    elif algo_type == config["algo_names"]["battery_marker"]:
        result = battery_data_marker(stream_uuid, stream_name, input_streams, config)
    elif algo_type == config["algo_names"]["sensor_unavailable_marker"]:
        result = sensor_unavailable(stream_uuid, stream_name, input_streams, config)
    elif algo_type == config["algo_names"]["packet_loss_marker"]:
        result = packet_loss(stream_uuid, stream_name, input_streams, config)
    return result



def attachment_marker(generated_stream_id, stream_name, input_streams, config):

    if stream_name == config["sensor_types"]["autosense_ecg"]:
        name = 'ecg_attachment_marker'
        input_param = {"window_size": config["general"]["window_size"],
                       "ecg_vairance_threshold": config["attachment_marker"]["ecg_on_body"]}
    elif stream_name == config["sensor_types"]["autosense_rip"]:
        name = 'rip_attachment_marker'
        input_param = {"window_size": config["general"]["window_size"],
                       "rip_vairance_threshold": config["attachment_marker"]["rip_on_body"]}
    elif stream_name == config["sensor_types"]["motionsense_accel"]:
        name = 'motionsense_attachment_marker'
        input_param = {"window_size": config["general"]["window_size"],
                       "motionsense_vairance_threshold": config["attachment_marker"]["motionsense_on_body"]}
    else:
        raise ValueError("Incorrect sensor type")

    output_stream = [{"name": name, "id": str(generated_stream_id)}];
    method = 'cerebralcortex.data_processor.data_diagnostic.attachment_marker'
    algo_description = config["description"]["attachment_marker"]

    ec = get_execution_context(name, input_param, input_streams, output_stream, method,
                               algo_description, config)
    dd = get_data_descriptor()
    ann = get_annotations()

    return {"ec": ec, "dd": dd, "ann": ann}


def battery_data_marker(generated_stream_id, stream_name, input_streams, config):

    if stream_name == config["sensor_types"]["phone_battery"]:
        name = 'phone_battery_marker'
        input_param = {"window_size": config["general"]["window_size"],
                       "phone_powered_off_threshold": config["battery_marker"]["phone_powered_off"],
                       "phone_battery_down_threshold": config["battery_marker"]["phone_battery_down"]}
    elif stream_name == config["sensor_types"]["autosense_battery"]:
        name = 'autosense_battery_marker'
        input_param = {"window_size": config["general"]["window_size"],
                       "autosense_powered_off_threshold": config["battery_marker"]["autosense_powered_off"],
                       "autosense_battery_down_threshold": config["battery_marker"]["autosense_battery_down"]}

    elif stream_name == config["sensor_types"]["motionsense_battery"]:
        name = 'motionsense_battery_marker'
        input_param = {"window_size": config["general"]["window_size"],
                       "motionsense_powered_off_threshold": config["battery_marker"]["motionsense_powered_off"],
                       "motionsense_battery_down_threshold": config["battery_marker"]["motionsense_battery_down"]}
    else:
        raise ValueError("Incorrect sensor type")

    output_stream = [{"name": name, "id": str(generated_stream_id)}];

    algo_description = config["description"]["battery_data_marker"]

    method = 'cerebralcortex.data_processor.data_diagnostic.BatteryDataMarker'

    ec = get_execution_context(name, input_param, input_streams, output_stream, method,
                               algo_description, config)
    dd = get_data_descriptor()
    ann = get_annotations()
    return {"ec": ec, "dd": dd, "ann": ann}


def sensor_unavailable(generated_stream_id, type, input_streams, config):

    if type == config["sensor_types"]["autosense_ecg"]:
        name = 'autosense_unavailable_marker'
        input_param = {"window_size": config["general"]["window_size"],
                       "sensor_unavailable_threshold": config["sensor_unavailable_marker"]["ecg"]}
    elif type == config["sensor_types"]["autosense_rip"]:
        name = 'autosense_unavailable_marker'
        input_param = {"window_size": config["general"]["window_size"],
                       "sensor_unavailable_threshold": config["sensor_unavailable_marker"]["rip"]}

    elif type == config["sensor_types"]["motionsense_accel"]:
        name = 'motionsense_unavailable_marker'
        input_param = {"window_size": config["general"]["window_size"],
                       "sensor_unavailable_threshold": config["sensor_unavailable_marker"]["motionsense"]}
    else:
        raise ValueError("Incorrect sensor type")

    output_stream = [{"name": name, "id": str(generated_stream_id)}];
    algo_description = config["description"]["sensor_unavailable_marker"]
    method = 'cerebralcortex.data_processor.data_diagnostic.packet_loss_marker'

    ec = get_execution_context(name, input_param, input_streams, output_stream, method,
                               algo_description, config)
    dd = get_data_descriptor()
    ann = get_annotations()
    return {"ec": ec, "dd": dd, "ann": ann}


def packet_loss(generated_stream_id, type, input_streams, config):

    if type == config["sensor_types"]["autosense_ecg"]:
        name = 'ecg_packet_loss_marker'
        input_param = {"window_size": config["general"]["window_size"],
                       "ecg_acceptable_packet_loss": config["packet_loss_marker"]["ecg_acceptable_packet_loss"]}
    elif type == config["sensor_types"]["autosense_rip"]:
        name = 'rip_packet_loss_marker'
        input_param = {"window_size": config["general"]["window_size"],
                       "rip_acceptable_packet_loss": config["packet_loss_marker"]["rip_acceptable_packet_loss"]}

    elif type == config["sensor_types"]["motionsense_accel"]:
        name = 'motionsense_packet_loss_marker'
        input_param = {"window_size": config["general"]["window_size"],
                       "rip_acceptable_packet_loss": config["packet_loss_marker"]["motionsense_acceptable_packet_loss"]}
    else:
        raise ValueError("Incorrect sensor type")

    output_stream = [{"name": name, "id": str(generated_stream_id)}];
    algo_description = config["description"]["packet_loss_marker"]
    method = 'cerebralcortex.data_processor.data_diagnostic.packet_loss_marker'

    ec = get_execution_context(name, input_param, input_streams, output_stream, method,
                               algo_description, config)
    dd = get_data_descriptor()
    ann = get_annotations()
    return {"ec": ec, "dd": dd, "ann": ann}




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


def get_execution_context(name, input_param, input_streams, output_streams, method,
                          algo_description, config):
    author = ["Ali"]
    version = '0.0.1'
    ref = 'url of pub'
    execution_context = {
        "execution_context": {
            "processing_module": {
                "name": name,
                "description": config["description"]["data_diagnostic"],
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
    annotations = {}
    return json.dumps(annotations)



