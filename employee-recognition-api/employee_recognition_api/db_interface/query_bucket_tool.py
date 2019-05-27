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
            logging.info('QueryBucketTool.get_from_bucket(): Retrieving file from storage bucket')
            connection = cloudstorage.open('{}/{}'.format(self.bucket_path, file_path))              
            file_contents = connection.read()
            connection.close()

            # Return bytes of image if successful
            return bytes(file_contents)
        except NotFoundError as e: 
            logging.exception(e)
            return None

#    def post(self, file_path):
#        logging.info('do something')


    def delete(self, file_path):
        # Attempt deletion of file_path
        try:      
            logging.info('QueryBucketTool.delete_from_bucket(): Deleting file from storage bucket')
            cloudstorage.delete('{}/{}'.format(self.bucket_path, file_path))
            logging.info('QueryBucketTool.delete_from_bucket(): Deleting file from storage bucket was successful')
            # Return True if successful
            return True

        # Return False if no file to delete in the first place / unsuccessful
        except NotFoundError as e: 
            logging.exception(e)
            return False
        except Exception as e:
            logging.exception(e)
            return False

# References
# [1] https://cloud.google.com/appengine/docs/standard/python/googlecloudstorageclient/read-write-to-cloud-storage
# [2] TODO: References from users_signature.py