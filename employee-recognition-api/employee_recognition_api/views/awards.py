from flask import Blueprint, request, Response
import datetime 
import logging
import os 
import pymysql
import json
from ..db_interface.query_tool import QueryTool
from ..db_interface.input_validator_tool import InputValidatorTool
from ..award_interface.builder import Builder
from ..award_interface.interpreter import Interpreter
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

def check_users_exist(authorizing_user_id, receiving_user_id):
    # Query database to determine if user ids exist, and continue if so; otherwise, return errors
    logging.info('awards_api: checking if user_ids {} and {} exist'.format(receiving_user_id, authorizing_user_id))
    query = QueryTool(connection_data)
    result1 = query.get_by_id('users', {
        'user_id': authorizing_user_id 
    })    
    result2 = query.get_by_id('users', {
        'user_id': receiving_user_id
    })
    
    try: 
        if result1['errors'] is not None:
            status_code = 400
            logging.info('awards_api.check_users_exist(): {}'.format(result1))
            result = result1
    except KeyError:
        try: 
            if result2['errors'] is not None: 
                logging.info('awards_api.check_users_exist(): returning {}'.format(result2))
                result = result2
        except KeyError:
            logging.info('awards_api: user_ids found')
            result = True

    query.disconnect()
    return result 

def check_award_does_not_exist(type_string, awarded_datetime): 
    query = QueryTool(connection_data)
    # Check if more awards are acceptable during time period 
    result = True # default is to accept the award
    if type_string == 'month': 
        # Identify date range for month to compare against
        month = datetime.datetime.strptime(awarded_datetime, '%Y-%m-%d %H:%M:%S').month
        year = datetime.datetime.strptime(awarded_datetime, '%Y-%m-%d %H:%M:%S').year

        # Find existing awards during month range identified. If found, return errors and do not continue
        greater = str(datetime.datetime(year, month, 1, 0, 0, 0, 0))
        lesser = str(datetime.datetime(year, month + 1, 1, 0, 0, 0))
        blob = { 
            'awarded_datetime': {
                'greater': greater, 
                'lesser': lesser 
            }, 
            'type': 'month'
        }
        existing_awards = query.get_awards_by_filter('awarded_datetime', blob, True)

        logging.info('awards_api.check_award_does_not_exist(): existing_awards: {}'.format(existing_awards))
        if len(existing_awards['award_ids']) != 0:
            logging.info('awards_api.check_award_does_not_exist(): Awards found during time period')
            result = {'errors': [{'field': 'type', 'message': 'too many awards of month type in time period'}]}
        else: 
            logging.info('awards_api.check_award_does_not_exist(): No awards found during time period')

    elif type_string == 'week':
        # Determine what day of the week our day is 
        # 1 2 3 4 5 6 7
        # M T W T F S S
        weekday_number = datetime.datetime.strptime(awarded_datetime, '%Y-%m-%d %H:%M:%S').isoweekday()
        logging.info('awards_api.check_award_does_not_exist(): weekday_number is {}'.format(weekday_number))

        # Get the beginning and end of week based on this
        beg_of_week = datetime.datetime.strptime(awarded_datetime, '%Y-%m-%d %H:%M:%S') - datetime.timedelta(days=weekday_number - 1)
        end_of_week = datetime.datetime.strptime(awarded_datetime, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(days=7 - weekday_number)
        logging.info('awards_api.check_award_does_not_exist(): beginning of week: {}'.format(beg_of_week))
        logging.info('awards_api.check_award_does_not_exist(): end of week: {}'.format(end_of_week))

        # Query database for awards that exist in this week time period
        greater = str(beg_of_week)
        lesser = str(end_of_week)
        blob = { 
            'awarded_datetime': {
                'greater': greater, 
                'lesser': lesser 
            }, 
            'type': 'week'
        }
        logging.info('blob: {}'.format(blob))
        existing_awards = query.get_awards_by_filter('awarded_datetime', blob, True)

        logging.info('awards_api.check_award_does_not_exist(): existing_awards: {}'.format(existing_awards))
        if len(existing_awards['award_ids']) != 0:
            logging.info('awards_api.check_award_does_not_exist(): Awards found during time period')
            result = {'errors': [{'field': 'type', 'message': 'too many awards of month type in time period'}]}
        else: 
            logging.info('awards_api.check_award_does_not_exist(): No awards found during time period')

    query.disconnect()
    return result

def create_pdf(data): 
    success_bool = False
    builder_tool = Builder(connection_data, data['type'])
    award_data = builder_tool.query_database_for_data(data)
    modified_award_tex = builder_tool.generate_award_tex(award_data)
    image = builder_tool.query_bucket_for_image(award_data['SignaturePath'])    
    if image is not None: 
        interpreter_tool = Interpreter()
        pdf = interpreter_tool.interpret(award_data['SignaturePath'], modified_award_tex, image)
        if pdf is not None:
            success_bool = interpreter_tool.write_award_to_bucket(data['award_id'], pdf)
        
    return success_bool  

@awards_api.route('/awards', methods=['GET'])
@awards_api.route('/awards/<int:award_id>', methods=['GET', 'DELETE'])
def awards(award_id=None):
    """ Handle POST /awards, GET, DELETE /awards/<award_id> 
    
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
    # Parse JSON request.data
    data = json.loads(request.data)
    ivt = InputValidatorTool()
    query = QueryTool(connection_data)

    # Check both users exist
    users_exists = check_users_exist(data['authorizing_user_id'], data['receiving_user_id'])
    if users_exists is not True: 
        return Response(json.dumps(users_exists), status=400, mimetype='application/json')

    # Check the award is the first of it's kind in it's respective time range
    award_dne = check_award_does_not_exist(data['type'], data['awarded_datetime'])
    if award_dne is not True:
        query.disconnect() 
        return Response(json.dumps(award_dne), status=400, mimetype='application/json')
    
    # Continue with award POST 
    # Validate the data provided
    result = ivt.validate_awards(data)
    if result is not None:
        query.disconnect() 
        return Response(json.dumps(result), status=400, mimetype='application/json')
    
    # Insert query against database based on request data
    data['distributed'] = False
    post_result = query.post('awards', data)
    try: 
        if post_result['award_id']: 
            data['award_id'] = post_result['award_id']
            if create_pdf(data) is not True: 
                logging.info('awards_api: Failed to post PDF to google storage bucket')
                query.disconnect()
                return Response(json.dumps(post_result), status=400, mimetype='application/json')
            else: 
                query.disconnect()
                return Response(json.dumps(post_result), status=200, mimetype='application/json')

    except KeyError as e:
        logging.exception(e)
        query.disconnect()
        return Response(json.dumps(post_result), status=400, mimetype='application/json')

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

@awards_api.route('/awards/test', methods=['GET'])
def test_awards():

    builder_tool = Builder(connection_data, 'month')
    test_block = {
        'AuthorizeFirstName': 'Natasha',
        'AuthorizeLastName': 'Kvavle',
        'ReceiveFirstName': 'Patrick',
        'ReceiveLastName': 'DeLeon',
        'SignaturePath': 'kvavlen_sig.jpg', 
        'Month': 'May', 
        'Day': '5',
        'Year': '2019'
    }    

    try: 
        modified_award_tex = builder_tool.generate_award_tex(test_block)
        image = builder_tool.query_bucket_for_image(test_block['SignaturePath'])    
        interpreter_tool = Interpreter()
        pdf = interpreter_tool.interpret(test_block['SignaturePath'], modified_award_tex, image)
        
        interpreter_tool.write_award_to_bucket(1, pdf)
        return Response(json.dumps({'result': 'success'}), status=200, mimetype='application/json')
    # TODO: Failing
    except Exception as e: 
        logging.exception(e)
        return Response(json.dumps({'result': 'failure'}), status=400, mimetype='application/json')

# References 
# [1] https://www.programiz.com/python-programming/methods/string/replace                                       re: python string replace()
# [2] https://docs.python.org/2/library/datetime.html                                                           re: datetime obj
# [3] https://stackoverflow.com/questions/19480028/attributeerror-datetime-module-has-no-attribute-strptime     re: use of strptime
# [4] https://stackoverflow.com/questions/2600775/how-to-get-week-number-in-python                              re: isocalendar
# [5] https://stackoverflow.com/questions/6871016/adding-5-days-to-a-date-in-python?rq=1                        re: using timedelta
# [6] https://stackoverflow.com/questions/19216334/python-give-start-and-end-of-week-data-from-a-given-date     re: ideas on how to accomplish getting first and last day of a week
