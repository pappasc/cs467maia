from flask import Blueprint, request, Response
import os 
import logging
import json
from ..award_interface.builder import Builder
from ..award_interface.interpreter import Interpreter
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
def test_awards_create_pdf(self):
    try: 
        logging.info('tests_api: Setting up test data')
        test_results = []
        data = { 
            'happy_path': [{
                'authorizing_user_id': 1,
                'receiving_user_id': 2, 
                'award_id': 1,
                'type': 'week' 
            }], 
            'sad_path': [{
                'authorizing_user_id': 2,
                'receiving_user_id': 1, 
                'award_id': 2,
                'type': 'week'      
            }]
        }
        # Based on users_signature.py: 
        
        for tc in data['happy_path']:
            logging.info('tests_api: Testing create_pdf() Happy Path')
            result = create_pdf(tc)
            if result.keys != ['award_id']:
                test_result.push({'happy_path': 'failure'})
            else:

                # Open read connection to cloud storage bucket & read file
                connection = cloudstorage.open('/cs467maia-backend.appspot.com/awards/award_1.pdf', mode='r')
                pdf = connection.read()
                connection.close()
                
                if b'\x25\x50\x44\x46' in bytearray(pdf):
                    test_result.push({'happy_path': 'success'})

        for tc in data['sad_path']:
            logging.info('tests_api: Testing create_pdf() Sad Path')
            result = create_pdf(tc)
            if result.keys != ['award_id']:
                test_result.push({'sad_path': 'failure'})
            else:
                connection = cloudstorage.open('/cs467maia-backend.appspot.com/awards/award_1.pdf', mode='r')
                pdf = connection.read()
                connection.close()
                
                if pdf is None: 
                    test_result.push({'sad_path': 'success'})
    except Exception as e:
        logging.exception(e)

@tests_api.route('/test/awards/distribute', methods=['GET'])
def test_distributer(self): 
    print('do nothing ... yet')

# References
# [1] References re: cloudstorage from users_signature.py
# [2] https://stackoverflow.com/questions/6186980/determine-if-a-byte-is-a-pdf-file re: determine if a file is PDF
# [3] https://www.geeksforgeeks.org/python-bytearray-function/                      re: Dealing with bytes