# Note: Separating out signature endpoint from other endpoints
#       as a workaround to errors surrounding importing cloudstorage package. 
#       This issue only arises locally when trying to create modules, and is well-documented 
#       as a common issue online and may actually be expected when running locally. 

from flask import Blueprint, request, Response
import os 

# Allow users_sig_api to be accessible from main.py
users_sig_api = Blueprint('users_sig_api', __name__)

if os.environ.get('ENV') != 'local':
    import cloudstorage 
    import logging
    import pymysql
    import json
    from ..db_interface.query_tool import QueryTool
     
    # Define connection data
    connection_name = 'maia-backend:us-west1:employee-recognition-db'
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


            # Write image to Google Cloud Storage.
            # Two paths are available to us. Keeping both in place (one commented out) for posterity.

            # CURRENT PATH (using cloudstorage package)
            # =========================================================
            logging.info('users_signature.py (users_signature()): writing to cloud storage')

            try:        
                # Get image from raw request.data
                image = str(request.data)

                # Open write connection to cloud storage bucket
                connection = cloudstorage.open('/maia-backend.appspot.com/signatures/{}'.format(filename), mode='w', content_type='image/jpeg')
                
                # Write raw image data & close connection to bucket
                connection.write(request.data)
                connection.close()

                # If no exception occurs, consider this a success
                return Response(json.dumps({'user_id': '{}'.format(user_id)}), status=200, mimetype='application/json')
            except Exception as e:
                # Don't raise any exception, bug log exception and return error to user
                logging.exception(e)
                return Response(json.dumps({'errors': [ {'field': 'n/a', 'message': 'upload error: {}'.format(e)}]}), status=400, mimetype='application/json')

            # OLD PATH (using JSON API)
            # ===========================
            # This path doesn't work because we aren't refreshing token systematically.

            # Define API parameters
            # token = 'ya29.GlwAB_3k8a_MRfpYkos12hj6viafjBb1G30xgIK7IlJ2Atdaxc0ZUuranxzv81sxChjXcrMnkLVr5n0EJvyG0FYHTuvpkJDHzuXPLTpqOfk8bhUBgh7mEU9wKCE-gA'
            # headers = {
            #   'Content-Type': 'image/jpeg',
            #   'Content-Length': '{}'.format(len(request.data)),
            #   'Authorization': 'Bearer {}'.format(token),
            # }

            # upload_url = 'https://www.googleapis.com/upload/storage/v1/b/maia-backend.appspot.com/o?uploadType=media&name=signatures/{}'.format(filename)

            # Read binary image into array of bytes for transfer [6]
            # payload = bytearray(request.data)

            # Treat as POST even though the route is a PUT
            # We're updating an existing entry from perspective of admin, 
            # but adding signature for first time
            # result = urlfetch.fetch(
            #   url=upload_url,
            #   payload=payload, 
            #   method=urlfetch.POST, 
            #   headers=headers
            #)

            # if result.status_code == 200: 
            #   return Response(json.dumps({'user_id': '{}'.format(user_id)}), status=200, mimetype='application/json')
            # else: 
            #   return Response(json.dumps({'errors': [ {'field': 'n/a', 'message': 'upload error'}]}), status=400, mimetype='application/json')


# References
# Included references for "OLD" path as well. 
# [1] http://flask.pocoo.org/docs/1.0/patterns/fileuploads/                                                                 re: file upload
# [2] https://cloud.google.com/storage/docs/uploading-objects 
# [3] https://cloud.google.com/storage/docs/json_api/v1/how-tos/simple-upload
# [4] https://cloud.google.com/appengine/docs/standard/python/issue-requests                                                re: urlfetch
# [5] https://developers.google.com/apps-script/reference/url-fetch/url-fetch-app                                           re: urlfetch
# [6] https://stackoverflow.com/questions/22351254/python-script-to-convert-image-into-byte-array                           re: code example for reading image into byte array 
# [7] https://cloud.google.com/appengine/docs/standard/python/issue-requests                                                re: getting attributes of urlfetch response
# [8] https://cloud.google.com/docs/authentication/production?hl=en_US                                                      re: how to use application default credentials to access cloud storage upload json api
# [9] https://cloud.google.com/appengine/docs/standard/python/googlecloudstorageclient/read-write-to-cloud-storage          re: uploading to cloud storage
# [10] https://cloud.google.com/appengine/docs/standard/python/googlecloudstorageclient/setting-up-cloud-storage            re: how to run dev_appserver with default bucket name
# [11] https://cloud.google.com/appengine/docs/standard/python/googlecloudstorageclient/functions#open                      re: leading / before bucket name
# [12] https://stackoverflow.com/questions/51179455/issue-with-using-cloudstorage-module-in-python                          re: help finding correct lib
# [13] https://github.com/GoogleCloudPlatform/python-docs-samples/issues/853                                                re: some google tools are not expected to run locally, so cloudstorage may be one of those