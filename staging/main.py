import json
import os
from flask import request, Response, redirect
from update_user_attribute_value import get_user_id_by_email, set_user_attribute_user_value, toggle_user_attr

BASE_DOMAIN = f"https://{os.environ.get('REGION')}-{os.environ.get('PROJECT')}.cloudfunctions.net/{os.environ.get('ACTION_NAME')}-"

def handle_error(message, status):
    """Prints and return error message"""
    print(message)
    response = {'looker': {'success': False, 'message': message}}
    return Response(json.dumps(response), status=status, mimetype='application/json')

# https://github.com/looker-open-source/actions/blob/master/docs/action_api.md#actions-list-endpoint
def action_list(request):
    """Return action hub list endpoint data for action"""
    # auth = utils.authenticate(request)
    # if auth.status_code != 200:
    #     return auth

    response = {
        'label': 'Switch ONE or Customer View',
        'integrations': [
            {
                'name': os.environ.get('ACTION_NAME'),
                'label': os.environ.get('ACTION_LABEL'),
                'supported_action_types': ['cell','query','dashboard'],
                'url': BASE_DOMAIN + 'execute',
                "required_fields": [{"any_tag": ["update_user_type"]}],
                'params': [
                    {'name': 'user_id', 'label': 'User ID',
                        'user_attribute_name': 'id', 'required': True},
                    {'name': 'user_type', 'label': 'User Type',
                        'user_attribute_name': 'user_type', 'required': True}
                ]                
            }
        ]
    }
    print('returning integrations json')
    return Response(json.dumps(response), status=200, mimetype='application/json')

# https://github.com/looker-open-source/actions/blob/master/docs/action_api.md#action-form-endpoint
def action_form(request):
    """Return form endpoint data for action"""
    # auth = utils.authenticate(request)
    # if auth.status_code != 200:
    #     return auth

    response = [{
            'name': 'user_email',
            'label': 'Your User Email',
            'description': "Please enter your user email. DO NOT enter a different user's email, as this action will update the user attributes for the specified email",
            'type': 'text',
            'required': True
        },
            {
            'name': 'user_type',
            'label': 'User Type',
            'description': "Select 'internal' for ONE view or 'external' for Customer view. This will update the user type attribute for the specified email",
            'type': 'select',
            'required': True,
            'options': [
                {
                    'label': 'Internal',
                    'value': 'internal'
                },
                {
                    'label': 'External',
                    'value': 'external'
                }
            ]
        }
    ]
    print(f'returning form json: {json.dumps(response)}')
    return Response(json.dumps(response), status=200, mimetype='application/json')

def action_execute(request):
    request_json = request.get_json()
    action_params = request_json['data']
    print(request_json)

    try:
        user_id = action_params['user_id']
        user_type = action_params['user_type']
    except KeyError as e:
        return handle_error(f"Missing required parameter: {e}", 400)
    user_attribute_id = "39" # ID of the user attribute "User Type in stg instance"
    response = toggle_user_attr(user_id, attribute_id=user_attribute_id, attribute_value=user_type)
    print(f'Looker response: {response}')
    return Response(status=200, mimetype="application/json")