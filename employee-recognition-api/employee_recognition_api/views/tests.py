from flask import Blueprint, request, Response
import os 
import logging
import json
from ..award_interface.builder import Builder
from ..award_interface.interpreter import Interpreter
from ..db_interface.query_tool import QueryTool 
from awards import create_pdf

if os.environ.get('ENV') != 'local':
    from google.appengine.api import urlfetch
    import cloudstorage 


# This API is for integration testing on things I cannot test locally (i.e. Google AppEngine specific libraries)
# Specifically, testing functions that integration interpreter + builder functionality, or distributer functionality

# Allow admin_api to be accessible to main.py
tests_api = Blueprint('tests_api', __name__)

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

@tests_api.route('/test/awards/create_pdf', methods=['GET'])
def test_awards_create_pdf():
    """Test create_pdf(), used in POST /awards
    Effectively tests integration of builder + interpreter + distributer

    """
    query_tool = QueryTool(connection_data)
    try:
        # Setup test 
        logging.info('tests_api: Setting up test data')
        test_results = []
        data = { 
            'happy_path': [{
                'test': 1,
                'authorizing_user_id': 1,
                'receiving_user_id': 2, 
                'award_id': 1,
                'type': 'week',
            }]
        }
        # Sad path doesn't make sense to test, because the create_pdf function is already given good data.

        # Based on users_signature.py: 
        # For each test case in happy path
        for tc in data['happy_path']:
            logging.debug('tests_api: Testing create_pdf() Happy Path')

            # Run create_pdf() with email off
            result = create_pdf(tc, False)

            # If create_pdf() failed, then the test failed
            if result is not True:
                test_results.append({'test': tc['test'], 'result' : 'failure'})
            
            # If create_pdf() was successful, check end state is expected
            else:
                # Keep track of checks that pass
                checks_passed = 0

                # Perform checks
                logging.debug('tests_api: Checking distributed == True')
                get_result = query_tool.get_by_id('awards', {'award_id': tc['award_id']})
                if bool(get_result['distributed']) == False: 
                    test_results.append({'test': tc['test'], 'result' : 'failure: distributed bool not flipped'})
                else: 
                    logging.debug('tests_api: distributed == True')
                    checks_passed += 1

                logging.debug('tests_api: Checking award removed from storage bucket')                
                try: 
                    connection = cloudstorage.open('/cs467maia-backend.appspot.com/awards/award_1.pdf', mode='r')
                    test_results.append({'test': tc['test'], 'result' : 'failure: award was not deleted'})
                except Exception as e: 
                    logging.debug('tests_api: award removed successfully from storage bucket')
                    checks_passed += 1

                logging.debug('tests_api: Checking signature file deleted from Amazon AWS instance')
                url = 'http://54.203.128.106:80/image/kvavlen_sig.jpg'
                
                result = urlfetch.fetch(
                    url=url,
                    method=urlfetch.GET
                )
                if result.status_code != 400: 
                    test_results.append({'test': tc['test'], 'result' : 'failure: signature image was not deleted'})
                else: 
                    logging.debug('tests_api: signature image removed successfully from Amazon AWS instance')
                    checks_passed += 1

                if checks_passed == 3: 
                    test_results.append({'test': tc['test'], 'result' : 'success'})

    # Capture and return any exception
    except Exception as e:
        logging.exception(e)
        return Response(json.dumps({'errors': [ {'message': 'an error occurred: {}'.format(e)}]}), status=400, mimetype='application/json')

    return Response(json.dumps(test_results), status=200, mimetype='application/json')

# References
# [1] References re: cloudstorage from users_signature.py
# [2] https://stackoverflow.com/questions/6186980/determine-if-a-byte-is-a-pdf-file re: determine if a file is PDF
# [3] https://www.geeksforgeeks.org/python-bytearray-function/                      re: Dealing with bytes