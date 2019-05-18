from flask import Blueprint, request, Response
import os 
import json
from ..db_interface.query_tool import QueryTool
from ..db_interface.input_validator_tool import InputValidatorTool

# Allow admin_api to be accessible to main.py
admins_api = Blueprint('admins_api', __name__)

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

@admins_api.route('/admins', methods=['GET', 'POST'])
@admins_api.route('/admins/<int:admin_id>', methods=['GET', 'PUT', 'DELETE'])
def admins(admin_id=None):
    """ Handle GET, POST /admins; GET, PUT, DELETE /admins/<admin_id>
    
    Arguments: 
        admin_id: int. Default is None. URL Parameter. 
    
    Returns: see README for results expected for each endpoint 
    """
    query = QueryTool(connection_data)
    ivt = InputValidatorTool()

    # GET /admins
    if request.method == 'GET' and admin_id is None:
        # Get all admins db entries
        result = query.get('admins')

        # Define success based on presence of 'admin_ids' key in result
        try: 
            if result['admin_ids']: 
                status_code = 200
        except KeyError:
            status_code = 400

    # GET /admins/<admin_id>
    elif request.method == 'GET' and admin_id is not None:
        # Query database for a particular admin_id's information
        result = query.get_by_id('admins', {
            'admin_id': admin_id
        })    

        # Define success based on precense of 'admin_id' key in result
        try: 
            if result['admin_id']: 
                status_code = 200
        except KeyError as e:
            status_code = 400

    # POST /admins
    elif request.method == 'POST' and admin_id is None: 
        # Parse JSON data into dictionary
        data = json.loads(request.data)

        # Validate request data
        result = ivt.validate_admins(request.method, data)

        # If request data is valid, continue
        if result is None: 
            # Make INSERT query into database with request data
            result = query.post('admins', data)

            # Define success based on presence of 'admin_id' key in result
            try: 
                if result['admin_id']: 
                    status_code = 200
            except KeyError: 
                status_code = 400 
        else:
            status_code = 400         

    # PUT /admins/<admin_id>
    elif request.method == 'PUT' and admin_id is not None:  
        # Parse JSON data into dictionary
        data = json.loads(request.data)

        # Validate request data
        result = ivt.validate_admins(request.method, data)

        # If request data is valid, continue
        if result is None:
            # Add admin_id to request body
            data['admin_id'] = int(admin_id)
            # Make an UPDATE query against database using body
            result = query.put_by_id('admins', data)
            
            # Define success based on presence of 'admin_id' key in result
            try: 
                if result['admin_id']: 
                    status_code = 200 
            except KeyError:
                status_code = 400
        else: 
            status_code = 400 

    # DELETE /admins/<admin_id>
    elif request.method == 'DELETE' and admin_id is not None:
        # Make a delete query for admin_id against database
        result = query.delete_by_id('admins',  { 
            'admin_id': admin_id
        })
        # Define success based on lack of 'errors' key in result
        try: 
            if result['errors']:
                status_code = 400 
        except KeyError:
            status_code = 200

    query.disconnect() 
    return Response(json.dumps(result), status=status_code, mimetype='application/json')

@admins_api.route('/admins/<int:admin_id>/login', methods=['GET', 'PUT'])
def admins_login(admin_id): 
    """Handle GET /admins/<admin_id>/login
    
    Arguments: 
        admin_id: int. URL Parameter. 
    
    Returns: see README for results expected for each endpoint 
    """
    query = QueryTool(connection_data)
    ivt = InputValidatorTool()

    # GET /admins/<admin_id>/login
    if request.method == 'GET' and admin_id is not None: 
        # Make a select query for particular admin_id's password information
        result = query.get_login_by_id('admins', {
                    'admin_id': admin_id
                })

        # Error if result doesn't have the key 'password'
        try: 
            if result['password']: 
                status_code = 200
        except KeyError:
            status_code = 400

    # PUT /admins/<admin_id>/login
    elif request.method == 'PUT' and admin_id is not None: 
        # Parse JSON data into dictionary
        data = json.loads(request.data)

        # Validate request data
        result = ivt.validate_login(data)

        # Add user_id to request body
        data['admin_id'] = int(admin_id)
        
        # Query database
        result = query.put_login_by_id('admins', data)
        # Error if result doesn't have the key 'admin_id'
        try: 
            if result['admin_id']: 
                status_code = 200
        except KeyError:
            status_code = 400
        
    query.disconnect()
    return Response(json.dumps(result), status=status_code, mimetype='application/json')
