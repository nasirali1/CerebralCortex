from flask_restplus import fields as rest_fields

def stream_data_model(stream_api):
    data_descriptor = stream_api.model('DataDescriptor', {
        'type': rest_fields.String(required=True),
        'unit': rest_fields.String(required=True),
        'descriptive_statistic': rest_fields.String(required=False)
    })
    parameter = stream_api.model('Parameter', {
        'name': rest_fields.String(required=True),
        'value': rest_fields.Arbitrary(required=True)
    })
    stream_entry = stream_api.model('Stream Entry', {
        'name': rest_fields.String(required=True),
        'identifier': rest_fields.String(required=True)
        # "pattern": "^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$"
    })
    execution_context = stream_api.model('Execution Context', {
        'input_parameters': rest_fields.List(rest_fields.Nested(parameter)),
        'input_streams': rest_fields.List(rest_fields.Nested(stream_entry))
    })
    annotations = stream_api.model('Annotation', {
        'name': rest_fields.String(required=True),
        'identifier': rest_fields.String(required=True)
        # "pattern": "^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$"
    })
    data_element = stream_api.model('Data Element', {
        'start_time': rest_fields.DateTime(required=True),
        'end_time': rest_fields.DateTime(required=False),
        'sample': rest_fields.List(rest_fields.Raw(required=True))
    })
    stream = stream_api.model('Stream', {
        'identifier': rest_fields.String(required=True),
        # "pattern": "^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$"
        'owner': rest_fields.String(required=True),
        # "pattern": "^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$"
        'name': rest_fields.String(required=True),
        'data_descriptor': rest_fields.List(rest_fields.Nested(data_descriptor), required=True),
        'execution_context': rest_fields.Nested(execution_context, required=True),
        'annotations': rest_fields.List(rest_fields.Nested(annotations)),
        'raw_data': rest_fields.List(rest_fields.Nested(data_element))
    })



    stream_data = stream_api.model('Stream Data', {
        'identifier': rest_fields.String(required=True),
        # "pattern": "^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$"
        'data': rest_fields.List(rest_fields.Nested(data_element), required=True)
    })
    return stream

def auth_data_model(stream_api):
    auth = stream_api.model('Authentication', {
        'email_id': rest_fields.String(required=True),
        'password': rest_fields.String(required=True),
    })
    return auth