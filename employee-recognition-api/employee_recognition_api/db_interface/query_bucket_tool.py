import os
if os.environ.get('ENV') != 'local':
    import cloudstorage 

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

        # Catch and log any exception - cloudstorage seems less predictable
        except Exception as e: 
            logging.exception(e)
            return None

#    def post(self, file_path):
#        logging.info('do something')


    def delete(self, file_path):
        logging.info('do something')