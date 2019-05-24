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

@awards_api.route('/awards', methods=['POST'])
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

    # POST /awards
    elif request.method == 'POST' and award_id is None: 
        
        # Parse JSON request.data
        data = json.loads(request.data)
        skip = False

        # Query database to determine if user ids exist, and continue if so; otherwise, return errors
        logging.info('awards_api: checking if user_ids {} and {} exist'.format(data['receiving_user_id'], data['authorizing_user_id']))
        query = QueryTool(connection_data)
        result1 = query.get_by_id('users', {
            'user_id': data['authorizing_user_id'] 
        })    
        result2 = query.get_by_id('users', {
            'user_id': data['receiving_user_id']
        })
        
        try: 
            if result1['errors'] is not None:
                status_code = 400
                logging.info('awards.py: returning {}'.format(result1))
                logging.info('awards.py: status code {}'.format(status_code))
                result = result1 
                skip = True 
        except KeyError:
            try: 
                if result2['errors'] is not None: 
                    status_code = 400 
                    logging.info('awards.py: returning {}'.format(result2))
                    logging.info('awards.py: status code {}'.format(status_code))
                    result = result2 
                    skip = True 
            except KeyError:
                logging.info('awards_api: user_ids found')

        # Check if more awards are acceptable during time period 
        if data['type'] == 'month': 
            try: 
                # Identify date range for month to compare against
                month = datetime.datetime.strptime(data['awarded_datetime'], '%Y-%m-%d %H:%M:%S').month
                year = datetime.datetime.strptime(data['awarded_datetime'], '%Y-%m-%d %H:%M:%S').year

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

                # Determine success based on lack of 'errors' key
                try: 
                    if len(existing_awards['errors']) != 0:
                        logging.info('No awards found during time period')
                except KeyError: 
                    status_code = 400 
                    result = {'errors': [{'field': 'type', 'message': 'too many awards of month type in time period'}]}
                    skip = True
            except Exception as e: 
                logging.exception(e) 
    
        elif data['type'] == 'week':
            try: 
                # Roundabout way of doing this, but works.
                # Identify date range for week
                # Get the week number that the awarded_datetime belongs to & save the year
                week_number = datetime.datetime.strptime(data['awarded_datetime'], '%Y-%m-%d %H:%M:%S').isocalendar()[1]
                logging.info('week number: {}'.format(week_number))
                year = datetime.datetime.strptime(data['awarded_datetime'], '%Y-%m-%d %H:%M:%S').year
                logging.info('year: {}'.format(year))

                # Determine what day was the "beginning" of the week at the start of the year
                jan1_weekday_number = datetime.datetime(year, 1, 1, 0, 0, 0, 0).isocalendar()[2]
                logging.info('weekday number jan 1: {}'.format(jan1_weekday_number))
                beg_of_year = datetime.datetime(year, 1, 1, 0, 0, 0, 0) - datetime.timedelta(days=jan1_weekday_number)
                logging.info('beginning of year: {}'.format(beg_of_year))

                # Calculate beginning of week by adding the week_number to the first day of the first week of the year
                # Then add 7 days to get end of week
                beg_of_week = beg_of_year + datetime.timedelta(weeks=week_number - 1) + datetime.timedelta(days=1)
                end_of_week = beg_of_year + datetime.timedelta(weeks=week_number - 1) + datetime.timedelta(days=7)

                logging.info('beginning of week: {}'.format(beg_of_week))
                logging.info('end of week: {}'.format(end_of_week))

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

                # Determine success based on lack of 'errors' key
                try: 
                    if len(existing_awards['errors']) != 0:
                        logging.info('No awards found during time period')
                except KeyError: 
                    status_code = 400 
                    result = {'errors': [{'field': 'type', 'message': 'too many awards of week type in time period'}]}
                    skip = True
            except Exception as e:
                logging.exception(e) 

        # Continue with award POST 
        if skip == False: 
            # Validate the data provided
            result = ivt.validate_awards(data)
            # Continue if validation was successful
            if result is None: 
                # Add distributed = false to the body of request
                data['distributed'] = False
                # Insert query against database based on request data
                result = query.post('awards', data)
                
                # Determine success based on presence of 'award_id' key
                try: 
                    if result['award_id']:
                        status_code = 200 
                except KeyError:
                    status_code = 400
            else:
                status_code = 400         

        logging.info('awards_api: returning {}'.format(result))
        logging.info('awards_api: status code {}'.format(status_code))

        # TODO: Award Distribution
        # award_driver = Driver()
        # award_driver.run()

        return Response(json.dumps(result), status=status_code, mimetype='application/json')

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
            if result['award_ids']: 
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
            if result['award_ids']: 
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
            if result['award_ids']: 
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
            if result['award_ids']: 
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
            if result['award_ids']: 
                status_code = 200
        except KeyError:
            status_code = 400

    query.disconnect()
    logging.info('awards_api: returning result {}'.format(result))
    logging.info('awards_api: returning status code {}'.format(status_code))
    return Response(json.dumps(result), status=status_code, mimetype='application/json')

@awards_api.route('/awards/test', methods=['GET'])
def test_awards():
    try: 
        builder_tool = Builder(connection_data, 'month')
        test_block = {
            'AuthorizeFirstName': 'Natasha',
            'AuthorizeLastName': 'Kvavle',
            'ReceiveFirstName': 'Patrick',
            'ReceiveLastName': 'DeLeon',
            'SignaturePath': '/app/kvavlen_sig.jpg', 
            'Month': 'May', 
            'Day': '5',
            'Year': '2019'
        }    
        # NOTE: Signature path is within context of docker container
        try: 
            #award_tex = builder_tool.generate_award_tex(test_block)
            #image = builder_tool.query_bucket_for_image(test_block['SignaturePath'])    
        
            interpeter_tool = Interpreter()
            result = interpeter_tool.interpret('kvavlen_sig.jpg')
        
        except Exception as e: 
            logging.exception(e)

        return result

    except Exception as e:
        logging.exception(e)

    


# References 
# [1] https://www.programiz.com/python-programming/methods/string/replace                                       re: python string replace()
# [2] https://docs.python.org/2/library/datetime.html                                                           re: datetime obj
# [3] https://stackoverflow.com/questions/19480028/attributeerror-datetime-module-has-no-attribute-strptime     re: use of strptime
# [4] https://stackoverflow.com/questions/2600775/how-to-get-week-number-in-python                              re: isocalendar
# [5] https://stackoverflow.com/questions/6871016/adding-5-days-to-a-date-in-python?rq=1                        re: using timedelta
# [6] https://stackoverflow.com/questions/19216334/python-give-start-and-end-of-week-data-from-a-given-date     re: ideas on how to accomplish getting first and last day of a week