# users.py
from flask import Blueprint, request, Response
import logging
import os 
import pymysql
import json
from ..db_interface.query_tool import QueryTool
from ..db_interface.input_validator_tool import InputValidatorTool
from threading import Thread

# Allow users_api to be accessible to main.py
users_api = Blueprint('users_api', __name__)

# Define connection data
connection_name = 'cs467maia-backend:us-west1:employee-recognition-database'
if os.environ.get('ENV') == 'dev' or os.environ.get('ENV') == 'local': 
    connection_name = '127.0.0.1'
connection_data = { 
    'environment': os.environ.get('ENV'),
    'username': 'api_user', 
    'password': 'tj348$', 
    'database': 'maia',
    'connection_name': '{}'.format(connection_name) 
}

@users_api.route('/users', methods=['GET', 'POST'])
@users_api.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def users(user_id=None):
    """ Handle GET, POST /users, GET, PUT, DELETE /users/<user_id> 
    
    Arguments: 
        user_id: int. Default is None. URL Parameter. 
    
    Returns: see README for results expected for each endpoint 
    """
    # Initialize tool classes
    query = QueryTool(connection_data)
    ivt = InputValidatorTool()

    # GET /users
    if request.method == 'GET' and user_id is None: 
        # Make select query for all users against database
        result = query.get('users')
        # Determine success based on presence of 'user_ids' key
        try: 
            if type(result['user_ids']) == list: 
                status_code = 200
        except KeyError:
            status_code = 400

    # GET /users/<user_id>
    elif request.method == 'GET' and user_id is not None:
        # 
        result = query.get_by_id('users', {
            'user_id': user_id
        })  
        # Determine success based on presence of 'user_id' key
        try: 
            if result['user_id']:
                status_code = 200 
        except KeyError:
            status_code = 400

    # POST /users
    elif request.method == 'POST' and user_id is None: 
        # Parse JSON request data
        data = json.loads(request.data)
        # Validate parsed request data
        result = ivt.validate_users(request.method, data)

        # If result is None, continue
        if result is None: 
            # Make insert query against database
            result = query.post('users', data)
            # Determine success based on presence of 'user_id' key
            try: 
                if result['user_id']:
                    status_code = 200 

                    # TODO: Implement PUT to update signature path with user_id
            except KeyError:
                status_code = 400
        else:
            status_code = 400       

    # PUT /users/<user_id>
    elif request.method == 'PUT' and user_id is not None:   
        # Parse JSON request data
        data = json.loads(request.data)

        # Validate parsed request data
        result = ivt.validate_users(request.method, data)

        # If valid data, continue
        if result is None:
            # Add user_id into body & query database to update this user's information
            data['user_id'] = int(user_id)
            result = query.put_by_id('users', data)

            # Determine success based on presence of 'user_id' key
            try: 
                if result['user_id']:
                    status_code = 200
            except KeyError:
                status_code = 400
        else: 
            status_code = 400

    # DELETE /users/<user_id>
    elif request.method == 'DELETE' and user_id is not None:
        # Make deletion query against database
        result = query.delete_by_id('users',  { 
            'user_id': user_id
        })

        # Define success based on lack of 'errors' key
        try: 
            if result['errors']:
                status_code = 400 
        except KeyError:
            status_code = 200

    query.disconnect()
    logging.info('users_api: returning result {}'.format(result))
    logging.info('users_api: returning status code {}'.format(status_code))
    return Response(json.dumps(result), status=status_code, mimetype='application/json')

@users_api.route('/users/<int:user_id>/login', methods=['GET', 'PUT'])
def users_login(user_id): 
    """ Handle GET /users/<user_id>/login request
    
    Arguments: 
        user_id: int. Default is None. URL Parameter. 
    
    Returns: see README for results expected for each endpoint 
    """
    # Initial tool classes
    query = QueryTool(connection_data)
    ivt = InputValidatorTool()
    
    # GET /users/<user_id>/login
    if request.method == 'GET' and user_id is not None: 
        # Make select query against database for password 
        result = query.get_login_by_id('users', {
                    'user_id': user_id
                })
        # Determine success based on presnce of 'password' key
        try: 
            if result['password']:
                status_code = 200 
        except KeyError:
            status_code = 400

    # PUT /users/<user_id>/login
    elif request.method == 'PUT' and user_id is not None: 
        # Parse JSON data into dictionary
        data = json.loads(request.data)

        # Validate request data
        result = ivt.validate_login(data)

        # Add user_id to request body
        data['user_id'] = int(user_id)

        # Query database
        result = query.put_login_by_id('users', data)

        # Error if result doesn't have the key 'user_id'
        try: 
            if result['user_id']: 
                status_code = 200
        except KeyError:
            status_code = 400


    query.disconnect()
    logging.info('users_api (users_login()): returning result {}'.format(result))
    logging.info('users_api (users_login()): returning status code {}'.format(status_code))
    return Response(json.dumps(result), status=status_code, mimetype='application/json')
