# users_signature.py
# Note: Originally separated out signature endpoint from other endpoints
#       as a workaround to errors surrounding importing cloudstorage package. 
#       Now only keeping separate since functionality is considerably different 
#       from other /users endpoints (since cloudstorage dependencies were moved elsewhere)

from flask import Blueprint, request, Response
from werkzeug.datastructures import Headers
from werkzeug.datastructures import FileStorage

import os 
from ..db_interface.query_bucket_tool import QueryBucketTool 

# Allow users_sig_api to be accessible from main.py
users_sig_api = Blueprint('users_sig_api', __name__)

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

# POST /users/<user_id>/signature
@users_sig_api.route('/users/<int:user_id>/signature', methods=['POST'])
def users_signature(user_id): 
    """ Handle PUT /users/<user_id>/signature
    
    Arguments: 
        user_id: int. Default is None. URL Parameter. 
    
    Returns: see README for results expected for each endpoint 
    """
    if request.method == 'POST' and user_id is not None: 
        logging.info('users.py: POST endpoint /users/<int:user_id>/signature')
        
        # Set headers 
        headers = Headers()
        headers.add('Access-Control-Allow-Origin', 'https://cs467maia-site.appspot.com')
        headers.add('Access-Control-Allow-Methods', 'POST')
        headers.add('Access-Control-Allow-Headers', 'Content-Type')
        headers.add('X-Content-Type-Options', 'nosniff')

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
                logging.info('users.py: returning result {}'.format(result))
                logging.info('users.py: returning status code {}'.format(status_code))
                return Response(json.dumps(result), headers=headers, status=status_code, mimetype='application/json')

        # Write image to Google Cloud Storage
        query_bucket_tool = QueryBucketTool()
        logging.info('DATA: {}'.format(request.files['sigFile']))
        image = request.files['sigFile'].read()

        write_result = query_bucket_tool.post('signatures/{}'.format(filename), image, 'image/jpeg')
        
        # If write is successful, return user_id; otherwise return errors
        if write_result == True:
            status_code = 200
            logging.info('users.py: returning result {}'.format(result))
            logging.info('users.py: returning status code {}'.format(status_code))
            return Response(json.dumps({'user_id': '{}'.format(user_id)}), headers=headers, status=status_code, mimetype='application/json')
        else: 
            status_code = 400
            logging.info('users.py: returning result {}'.format(result))
            logging.info('users.py: returning status code {}'.format(status_code))
            return Response(json.dumps({'errors': [ {'field': 'n/a', 'message': 'upload error'}]}), headers=headers, status=status_code, mimetype='application/json')

# References re: dealing with CORS
# [1] https://werkzeug.palletsprojects.com/en/0.15.x/datastructures/                                              re: headers, filestorage
# [2] https://stackoverflow.com/questions/31212992/how-to-enable-cors-on-google-app-engine-python-server/31213095 re: need for headers
# [3] https://flask-cors.corydolphin.com/en/latest/api.html#extension                                             re: headers to use
# [4] https://stackoverflow.com/questions/11933626/access-control-allow-origin-header-not-working-what-am-i-doing-wrong
# [5] https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS                                                      re: use of POST, multipart/form-data
# [6] https://stackoverflow.com/questions/40414526/how-to-read-multipart-form-data-in-flask                       re: to_dict()
# [7] http://flask.pocoo.org/docs/0.12/patterns/fileuploads/                                                      re: use of request.files
# [8] https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Type                                      re: set nosniff