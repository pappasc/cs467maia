import json
import logging
import os 

if os.environ.get('ENV') != 'local':
    from google.appengine.api import urlfetch
    import cloudstorage 

class Interpreter:
    """ Communicates with interpeter-api to gather PDF award & pushes to 
        the cs467maia-backend storage bucket 
    """
    def __init__(self):
        logging.info('Interpreter.__init__(): do nothing')

    def interpret(self, signature_path, tex, jpg):

        # Make POST request to interpreter-api /pdf endpoint
        url = 'http://54.203.128.106:80/pdf'
        try: 
            result = urlfetch.fetch(
                url=url,
                payload=json.dumps({
                    'signature_path': signature_path,
                    'tex_data': tex,
                    'jpg_data': jpg
                }),
                method=urlfetch.POST,
                headers={
                    'Content-Type': 'application/json'
                })
            
            logging.info(result)
            # If result is successful, return binary to calling function
            # Otherwise, return None
            if result.status_code == 200: 
                return result.content       
            else:
                return None
        except urlfetch.Error as e:
            logging.exception(e)
            return None

    def write_award_to_bucket(self, award_id, pdf_bytes):

        # Based off of code from views/users_signature.py  
        logging.info('Interpeter.write_award_to_bucket(): writing to cloud storage')
        try:        
            # Make file name based on award id
            filename = 'award_{}.pdf'.format(award_id)

            # Open write connection to cloud storage bucket
            connection = cloudstorage.open('/cs467maia-backend.appspot.com/awards/{}'.format(filename), mode='w', content_type='pdf')
                
            # Write raw image data & close connection to bucket
            connection.write(pdf_bytes)
            connection.close()
            return 0 # success

        except Exception as e:
            # Don't raise any exception, bug log exception and return error to user
            logging.exception(e)
            return 1 # failure
        

# References
# [1] https://cloud.google.com/appengine/docs/standard/python/issue-requests            re: code example for using urlfetch
# [2] https://www.programiz.com/python-programming/methods/built-in/bytes               re: use of bytes()
# See references in views/users_signature.py re: uploading to bucket