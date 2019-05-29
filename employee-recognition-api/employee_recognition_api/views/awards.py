from flask import Blueprint, request, Response
import datetime 
import logging
import os 
import pymysql
import json
from ..db_interface.query_tool import QueryTool
from ..db_interface.input_validator_tool import InputValidatorTool
from ..award_interface.award_driver import AwardDriver

# Allow awards_api to be accessible from main.py 
awards_api = Blueprint('awards_api', __name__)

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



@awards_api.route('/awards', methods=['GET'])
@awards_api.route('/awards/<int:award_id>', methods=['GET', 'DELETE'])
def awards(award_id=None):
    """ Handle  GET, DELETE /awards/<award_id> & GET /awards
    
    Arguments: 
        award_id: int. Default is None. URL Parameter. 
    
    Returns: see README for results expected for each endpoint 
    """
    # Create Tool class instances
    query = QueryTool(connection_data)
    ivt = InputValidatorTool()

    # GET /awards/<award_id>
    if request.method == 'GET' and award_id is not None: 
        # Query database for award based on ID
        result = query.get_by_id('awards', {
            'award_id': award_id
        })

        # Determine success on presence of award_id
        try: 
            if result['award_id']: 
                status_code = 200
        except KeyError:
            status_code = 400

    # GET /awards
    elif request.method == 'GET' and award_id is None: 
        # Query database for award based on ID
        result = query.get('awards')

        # Determine success on presence of award_id
        try: 
            if type(result['award_ids']) == list:  
                status_code = 200
        except KeyError:
            status_code = 400

    # DELETE /awards/<award_id>
    elif request.method == 'DELETE' and award_id is not None:
        # Deletion query against database given award_id
        result = query.delete_by_id('awards',  { 
            'award_id': award_id
        })
        # Determine success based on lack of 'errors' key in result
        try: 
            if result['errors']:
                status_code = 400 
        except KeyError:
            status_code = 200

    query.disconnect()
    logging.info('awards_api: returning result {}'.format(result))
    logging.info('awards_api: returning status code {}'.format(status_code))
    return Response(json.dumps(result), status=status_code, mimetype='application/json')

# POST /awards
@awards_api.route('/awards', methods=['POST'])
def awards_post():
    """ Handle POST /awards
    
    Returns: see README for results expected for each endpoint 
    """
    # Parse JSON request.data
    data = json.loads(request.data)
    ivt = InputValidatorTool()
    query = QueryTool(connection_data)
    driver = AwardDriver(connection_data, True)

    # Validate the data provided
    result = ivt.validate_awards(data)
    if result is not None:
        query.disconnect() 
        return Response(json.dumps(result), status=400, mimetype='application/json')
    
    # Check both users exist
    users_exists = ivt.check_users_exist(data['authorizing_user_id'], data['receiving_user_id'])
    if users_exists is not True: 
        return Response(json.dumps(users_exists), status=400, mimetype='application/json')

    # Check the award is the first of it's kind in it's respective time range
    award_dne = ivt.check_award_does_not_exist(data['type'], data['awarded_datetime'])
    if award_dne is not True:
        query.disconnect() 
        return Response(json.dumps(award_dne), status=400, mimetype='application/json')
    
    # Continue with award POST 
    # Insert query against database based on request data
    data['distributed'] = False
    post_result = query.post('awards', data)
    
    # If the post was successful and we have an award_id, save pdf to google storage bucket
    try: 
        if post_result['award_id']: 
            data['award_id'] = post_result['award_id']
            if driver.create_pdf(data) is not True: 
                logging.info('awards_api: Failed to make and email PDF')
                status_code = 200 # status code should be 200 regardless of the result of create_pdf, only based on POST to DB result
            else: 
                status_code = 200 
    except KeyError as e:
        logging.exception(e)
        status_code = 400

    query.disconnect()
    logging.info('awards_api: returning result {}'.format(post_result))
    logging.info('awards_api: returning status code {}'.format(status_code))
    return Response(json.dumps(post_result), status=status_code, mimetype='application/json')

# POST /awards
@awards_api.route('/awards/no-email', methods=['POST'])
def awards_post_no_email():
    """ Handle POST /awards
    
    Returns: see README for results expected for each endpoint 
    """
    # Parse JSON request.data
    data = json.loads(request.data)
    ivt = InputValidatorTool()
    query = QueryTool(connection_data)
    driver = AwardDriver(connection_data, False)

    # Validate the data provided
    result = ivt.validate_awards(data)
    if result is not None:
        return Response(json.dumps(result), status=400, mimetype='application/json')
    
    # Check both users exist
    users_exists = ivt.check_users_exist(data['authorizing_user_id'], data['receiving_user_id'])
    if users_exists is not True: 
        return Response(json.dumps(users_exists), status=400, mimetype='application/json')

    # Check the award is the first of it's kind in it's respective time range
    award_dne = ivt.check_award_does_not_exist(data['type'], data['awarded_datetime'])
    if award_dne is not True:
        query.disconnect() 
        return Response(json.dumps(award_dne), status=400, mimetype='application/json')
    
    # Continue with award POST 
    # Insert query against database based on request data
    data['distributed'] = False
    post_result = query.post('awards', data)
    
    # If the post was successful and we have an award_id, save pdf to google storage bucket
    try: 
        if post_result['award_id']: 
            data['award_id'] = post_result['award_id']
            if driver.create_pdf(data) is not True: 
                logging.info('awards_api: Failed to make and email PDF')
                status_code = 200 # TODO: This should change 
            else: 
                status_code = 200 
    except KeyError as e:
        logging.exception(e)
        status_code = 400

    query.disconnect()
    logging.info('awards_api: returning result {}'.format(post_result))
    logging.info('awards_api: returning status code {}'.format(status_code))
    return Response(json.dumps(post_result), status=status_code, mimetype='application/json')


@awards_api.route('/awards/authorize/<int:authorizing_user_id>', methods=['GET'])
def awards_authorize(authorizing_user_id): 
    """ Handle GET /awards/authorize/<authorizing_user_id>
    
    Arguments: 
        authorizing_user_id: int. Default is None. URL Parameter. 
    
    Returns: see README for results expected for each endpoint 
    """
    query = QueryTool(connection_data)

    # GET /awards/authorize/<authorizing_user_id>
    if request.method == 'GET' and authorizing_user_id is not None: 
        # Make select query against database for all awards authorized by user_id
        result = query.get_awards_by_filter('authorizing_user_id', {'authorizing_user_id': authorizing_user_id})

        # Determine success based on presence of 'award_ids' key in result
        try: 
            if type(result['award_ids']) == list: 
                status_code = 200
        except KeyError:
            status_code = 400

    query.disconnect()
    logging.info('awards_api: returning result {}'.format(result))
    logging.info('awards_api: returning status code {}'.format(status_code))
    return Response(json.dumps(result), status=status_code, mimetype='application/json')

@awards_api.route('/awards/receive/<int:receiving_user_id>', methods=['GET'])
def awards_receive(receiving_user_id):
    """ Handle GET /awards/receove/<receiving_user_id>
    
    Arguments: 
        receiving_user_id: int. Default is None. URL Parameter. 
    
    Returns: see README for results expected for each endpoint 
    """
    query = QueryTool(connection_data)

    # GET /awards/receive/<receiving_user_id>
    if request.method == 'GET' and receiving_user_id is not None:
        # Query database for awards received by user_id 
        result = query.get_awards_by_filter('receiving_user_id', {'receiving_user_id': receiving_user_id})
        # Determine success based on presence of 'award_ids' key in result
        try: 
            if type(result['award_ids']) == list: 
                status_code = 200
        except KeyError:
            status_code = 400

    query.disconnect()
    logging.info('awards_api: returning result {}'.format(result))
    logging.info('awards_api: returning status code {}'.format(status_code))
    return Response(json.dumps(result), status=status_code, mimetype='application/json')

@awards_api.route('/awards/type/<type_string>', methods=['GET'])
def awards_type(type_string):
    """ Handle GET /awards/type/<type_string>
    
    Arguments: 
        type: string. URL Parameter. 
    
    Returns: see README for results expected for each endpoint 
    """
    query = QueryTool(connection_data)

    # GET /awards/receive/<receiving_user_id>
    if request.method == 'GET' and type_string is not None: 
        # Query database for awards of given type
        result = query.get_awards_by_filter('type', {'type': type_string})
        
        # Determine success based on presence of 'award_ids' key in result
        try: 
            if type(result['award_ids']) == list: 
                status_code = 200
        except KeyError:
            status_code = 400

    query.disconnect()
    logging.info('awards_api: returning result {}'.format(result))
    logging.info('awards_api: returning status code {}'.format(status_code))
    return Response(json.dumps(result), status=status_code, mimetype='application/json')


@awards_api.route('/awards/datetime/<date>', methods=['GET'])
def awards_datetime(date):
    """ Handle GET /awards/datetime/<date>
    
    Arguments: 
        date: string. YYY-MM-DD. URL Parameter. 
    
    Returns: see README for results expected for each endpoint 
    """
    query = QueryTool(connection_data)
     
    # GET /awards/datetime/<date>
    if request.method == 'GET' and date is not None: 
        # Query database for awards created after time period specified
        result = query.get_awards_by_filter('awarded_datetime', {'awarded_datetime': '{} 00:00:00'.format(date)})

        # Determine success based on presence of 'award_ids' key in result
        try: 
            if type(result['award_ids']) == list:  
                status_code = 200
        except KeyError:
            status_code = 400

    query.disconnect()
    logging.info('award_api: returning result {}'.format(result))
    logging.info('award_api: returning status code {}'.format(status_code))
    return Response(json.dumps(result), status=status_code, mimetype='application/json')
    
@awards_api.route('/awards/distributed/<distributed>', methods=['GET'])
def awards_distributed(distributed):
    """ Handle GET /awards/distributed/<distributed>
    
    Arguments: 
        distributed: bool - true, false. URL Parameter. 
    
    Returns: see README for results expected for each endpoint 
    """
    query = QueryTool(connection_data)

    # GET /awards/receive/<receiving_user_id>
    if request.method == 'GET' and distributed is not None:
        # Ensure booleans are created from strings 
        if distributed == 'false':
            distributed_bool = False
        elif distributed == 'true':
            distributed_bool = True

        # Query database for awards with distributed value provided
        result = query.get_awards_by_filter('distributed', {'distributed': distributed_bool})
        
        # Determine success based on presence of 'award_ids' key in result
        try: 
            if type(result['award_ids']) == list: 
                status_code = 200
        except KeyError:
            status_code = 400

    query.disconnect()
    logging.info('awards_api: returning result {}'.format(result))
    logging.info('awards_api: returning status code {}'.format(status_code))
    return Response(json.dumps(result), status=status_code, mimetype='application/json')

