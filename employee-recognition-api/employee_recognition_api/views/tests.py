# tests.py
from flask import Blueprint, request, Response
import os 
import logging
import json
from ..db_interface.query_tool import QueryTool 
from ..db_interface.query_bucket_tool import QueryBucketTool
from ..award_interface.award_driver import AwardDriver

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
                'awarded_datetime': '2019-04-27 10:00:00',
                'award_id': 1,
                'type': 'week',
            }]
        }
        # Sad path doesn't make sense to test, because the driver.create_pdf function expects to get vetted data.

        # For each test case in happy path
        for tc in data['happy_path']:
            logging.debug('tests_api: Testing create_pdf() Happy Path')

            driver = AwardDriver(connection_data, False)
            # Run create_pdf() with email off
            result = driver.create_pdf(tc)

            # If create_pdf() failed, then the test failed
            if result is not True:
                test_results.append({'test': tc['test'], 'result' : 'failure'})
            
            # If create_pdf() was successful, check end state is expected
            else:
                # Keep track of checks that pass
                checks_passed = 0

                # Perform checks
                # Check: distribution == True
                logging.debug('tests_api: Checking distributed == True')
                get_result = query_tool.get_by_id('awards', {'award_id': tc['award_id']})
                if bool(get_result['distributed']) == False: 
                    test_results.append({'test': tc['test'], 'result' : 'failure: distributed bool not flipped'})
                else: 
                    logging.debug('tests_api: distributed == True')
                    checks_passed += 1

                # Check: No award in storage bucket
                logging.debug('tests_api: Checking award removed from storage bucket')                
                query_bucket_tool = QueryBucketTool()
                result = query_bucket_tool.get('awards/award_1.pdf')

                if result == True: 
                    test_results.append({'test': tc['test'], 'result' : 'failure: award was not deleted'})
                else: 
                    logging.debug('tests_api: award removed successfully from storage bucket')
                    checks_passed += 1

                # Check: No image in AWS instance
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

                # If all checks passed, success
                if checks_passed == 3: 
                    test_results.append({'test': tc['test'], 'result' : 'success'})

    # Capture and return any exception
    except Exception as e:
        logging.exception(e)
        return Response(json.dumps({'errors': [ {'message': 'an error occurred: {}'.format(e)}]}), status=400, mimetype='application/json')

    return Response(json.dumps(test_results), status=200, mimetype='application/json')

# References
# [1] https://www.geeksforgeeks.org/python-bytearray-function/                      re: Dealing with bytes