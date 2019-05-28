# Note: Separating out signature endpoint from other endpoints
#       as a workaround to errors surrounding importing cloudstorage package. 
#       This issue only arises locally when trying to create modules, and is well-documented 
#       as a common issue online and may actually be expected when running locally. 

from flask import Blueprint, request, Response
import os 
from ..db_interface.query_bucket_tool import QueryBucketTool 

# Allow users_sig_api to be accessible from main.py
users_sig_api = Blueprint('users_sig_api', __name__)

if os.environ.get('ENV') != 'local':
    import cloudstorage 

import logging
import pymysql
import json
from ..db_interface.query_tool import QueryTool
 
# Define connection data
connection_name = 'cs467maia-backend:us-west1:employee-recognition-database'
if os.environ.get('ENV') == 'dev': 
    connection_name = '127.0.0.1'
connection_data = { 
    'environment': os.environ.get('ENV'),
    'username': 'api_user', 
    'password': 'tj348$', 
    'database': 'maia',
    'connection_name': '{}'.format(connection_name) 
}

@users_sig_api.route('/users/<int:user_id>/signature', methods=['PUT'])
def users_signature(user_id): 
    """ Handle GET /users/<user_id>/signature
    
    Arguments: 
        user_id: int. Default is None. URL Parameter. 
    
    Returns: see README for results expected for each endpoint 
    """
    if request.method == 'PUT' and user_id is not None: 
        logging.info('users.py: PUT endpoint /users/<int:user_id>/signature')
        
        # If user exists, continue; otherwise, return errors
        logging.info('users.py: checking if user_id {} exists'.format(user_id))
        query = QueryTool(connection_data)
        result = query.get_by_id('users', {
            'user_id': user_id
        })  
        query.disconnect()
        try: 
            filename = result['signature_path']
        except KeyError:
            if result['errors']:
                status_code = 400 
                logging.info('users.py: returning {}'.format(result))
                logging.info('users.py: status code {}'.format(status_code))
                return Response(json.dumps(result), status=status_code, mimetype='application/json')

        # Write image to Google Cloud Storage
        logging.info('users_signature.py (users_signature()): writing to cloud storage')

        query_bucket_tool = QueryBucketTool()
        write_result = query_bucket_tool.post('signatures/{}'.format(filename), request.data, 'image/jpeg')
        
        # If write is successful, return user_id; otherwise return errors
        if write_result == True:
            return Response(json.dumps({'user_id': '{}'.format(user_id)}), status=200, mimetype='application/json')
        else: 
            return Response(json.dumps({'errors': [ {'field': 'n/a', 'message': 'upload error: {}'.format(e)}]}), status=400, mimetype='application/json')

# References
# [1] http://flask.pocoo.org/docs/1.0/patterns/fileuploads/                                                                 re: file upload
# [2] https://stackoverflow.com/questions/22351254/python-script-to-convert-image-into-byte-array                           re: code example for reading image into byte array 
