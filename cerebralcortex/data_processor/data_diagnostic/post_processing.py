import json
import uuid

from cerebralcortex.kernel.datatypes.datastream import DataStream, Stream
from cerebralcortex.CerebralCortex import CerebralCortex
from cerebralcortex.data_processor.data_diagnostic.util import map_data_to_datapoints
#from cerebralcortex.data_processor.data_diagnostic.SensorUnavailableMarker import WirelessDisconnection



def store(input_streams: dict, data: Stream, CC_obj: CerebralCortex, config: dict, algo_type: str):

    #check if only one parent-stream ID is used or more than one
    # if isinstance(parent_stream_id, list):
    #     #in sensor-unavailable algos, I simply passed whole input stream object
    #     input_streams = parent_stream_id
    #     parent_stream_id = input_streams[0]["id"]
    # else:
    #     input_streams = [{"name": stream_name, "id": str(parent_stream_id)}]

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

    if stream_name == "ecg":
        name = 'ecg_attachment_marker'
        input_param = {"window_size": config["general"]["window_size"],
                       "ecg_vairance_threshold": config["attachment_marker"]["ecg_on_body"]}
    elif stream_name == "rip":
        name = 'rip_attachment_marker'
        input_param = {"window_size": config["general"]["window_size"],
                       "rip_vairance_threshold": config["attachment_marker"]["rip_on_body"]}
    elif stream_name == "motionsense":
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


def battery_data_marker(generated_stream_id, stream_name, input_streams, config):

    if stream_name == "phone":
        name = 'phone_battery_marker'
        input_param = {"window_size": config["general"]["window_size"],
                       "phone_powered_off_threshold": config["battery_marker"]["phone_powered_off"],
                       "phone_battery_down_threshold": config["battery_marker"]["phone_battery_down"]}
    elif stream_name == "autosense":
        name = 'autosense_battery_marker'
        input_param = {"window_size": config["general"]["window_size"],
                       "autosense_powered_off_threshold": config["battery_marker"]["autosense_powered_off"],
                       "autosense_battery_down_threshold": config["battery_marker"]["autosense_battery_down"]}

    elif stream_name == "motionsense":
        name = 'motionsense_battery_marker'
        input_param = {"window_size": config["general"]["window_size"],
                       "motionsense_powered_off_threshold": config["battery_marker"]["motionsense_powered_off"],
                       "motionsense_battery_down_threshold": config["battery_marker"]["motionsense_battery_down"]}
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


def sensor_unavailable(generated_stream_id, type, input_streams, config):

    if type == "ecg":
        name = 'autosense_unavailable_marker'
        input_param = {"window_size": config["general"]["window_size"],
                       "sensor_unavailable_threshold": config["sensor_unavailable_marker"]["ecg"]}
    elif type == "rip":
        name = 'autosense_unavailable_marker'
        input_param = {"window_size": config["general"]["window_size"],
                       "sensor_unavailable_threshold": config["sensor_unavailable_marker"]["rip"]}

    elif type == "motionsense":
        name = 'motionsense_unavailable_marker'
        input_param = {"window_size": config["general"]["window_size"],
                       "sensor_unavailable_threshold": config["sensor_unavailable_marker"]["motionsense"]}
    else:
        raise ValueError("Incorrect sensor type")

    output_stream = [{"name": name, "id": str(generated_stream_id)}];
    algo_description = "This algorithm analyze battery-off stream to analyze whether battery was actually powered off or a person walked away from the phone."
    module_description = 'This is a data-diagnostic module that helps to identify the causes of missing data.'
    method = 'cerebralcortex.data_processor.data_diagnostic.packet_loss_marker'

    ec = get_execution_context(name, module_description, input_param, input_streams, output_stream, method,
                               algo_description)
    dd = get_data_descriptor()
    ann = get_annotations()
    return {"ec": ec, "dd": dd, "ann": ann}


def packet_loss(generated_stream_id, type, input_streams, config):

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
    annotations = {}
    return json.dumps(annotations)



