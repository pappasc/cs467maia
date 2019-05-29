# query_bucket_tool.py
import os
if os.environ.get('ENV') != 'local':
    import cloudstorage 
    from cloudstorage import NotFoundError

import logging

class QueryBucketTool:

    def __init__(self):
        self.bucket_path = '/cs467maia-backend.appspot.com'

    def get(self, file_path):
        """Connect to Google App Engine Storage bucket & read contents of file

        Arguments: 
            self
            file_path:   string. path in cloud storage bucket to file

        Returns: 
            None if unsuccessful/ hits exception
            Content (bytes) of file if successful
        """

        # Attempt connection
        try:      
            logging.info('QueryBucketTool.get(): retrieving file from storage bucket')
            connection = cloudstorage.open('{}/{}'.format(self.bucket_path, file_path))              
            file_contents = connection.read()
            connection.close()

            # Return bytes of image if successful
            logging.debug('QueryBucketTool.get(): retrieving file from storage bucket was successful')
            return bytes(file_contents)
        except NotFoundError as e: 
            logging.info('QueryBucketTool.get(): retrieving file from storage bucket was not successful')
            logging.exception(e)
            return None

    def post(self, file_path, content, content_type):
        """Write file to Google App Engine storage bucket

        Arguments:
            self
            file_path:      string. '{folder}/{filename}'. no leading slash
            content:        bytes. content of file to write
            content_type:   string. 'application/pdf' or 'image/jpeg'

        Returns: 
            True if successful, False if unsuccessful
        """
        try: 
            logging.info('QueryBucketTool.post(): writing file to storage bucket')

            # Open write connection to cloud storage bucket
            connection = cloudstorage.open('/cs467maia-backend.appspot.com/{}'.format(file_path), mode='w', content_type='{}'.format(content_type))
            
            # Write raw file data & close connection to bucket
            connection.write(content)
            connection.close()

            # Return True if successful
            logging.debug('QueryBucketTool.delete(): writing file to storage bucket was successful')
            return True

        # Return False if any exceptions raised / unsuccessful
        except Exception as e:
            logging.info('QueryBucketTool.post(): writing file to storage bucket was not successful')
            logging.exception(e) 
            return False

    def delete(self, file_path):
        """Delete file from Google App Engine storage bucket

        Arguments:
            self
            file_path:      string. '{folder}/{filename}'. no leading slash
        
        Returns: 
            True if successful, False if unsuccessful
        """
        # Attempt deletion of file_path
        try:      
            logging.debug('QueryBucketTool.delete(): deleting file from storage bucket')
            cloudstorage.delete('{}/{}'.format(self.bucket_path, file_path))
            logging.debug('QueryBucketTool.delete(): deleting file from storage bucket was successful')
            # Return True if successful
            return True

        # Return False if no file to delete in the first place / unsuccessful
        except NotFoundError as e: 
            logging.info('QueryBucketTool.delete(): deleting file from storage bucket was not successful')
            logging.exception(e)
            return False
        except Exception as e:
            logging.info('QueryBucketTool.delete(): deleting file from storage bucket was not successful')
            logging.exception(e)
            return False

# References
# Includes references that are no longer in use (for using URLfetch and JSON API)
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
