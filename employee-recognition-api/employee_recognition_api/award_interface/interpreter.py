import json
import logging
import os 

if os.environ.get('ENV') != 'local':
    from google.appengine.api import urlfetch
    import cloudstorage 

class Interpreter:
    """ Communicates with interpeter-api to render PDF award & pushes to 
        the cs467maia-backend storage bucket 
    """
    def __init__(self):
        logging.info('Interpreter.__init__(): do nothing')

    def save_image_to_disk(self, signature_path, image):
        """Save signature image to disk on AWS instance 

        Arguments: 
            self
            signature_path: string. name of signature file, not full path.
            image:          bytes. contents of image/jpeg file, pulled down from Google Storage Bucket
        
        Returns: 
            True on success, False on failure
        """

        # If image is not None, then we can continue (not an empty image)
        if image is not None: 
            logging.info('Interpeter.save_image_to_disk(): Saving image to AWS instance')
            # POST image to AWS instance
            url = 'http://54.203.128.106:80/image/{}'.format(signature_path)
            try: 
                result = urlfetch.fetch(
                    url=url,
                    payload=image,
                    method=urlfetch.POST,
                    headers={
                        'Content-Type': 'image/jpeg'
                    })
                
                # Log the result of the POST request
                logging.info('Interpreter.save_image_to_disk(): POST result was {}'.format(result.content))
                if result.status_code == 200: 
                    return True       
                else:
                    return False
            except urlfetch.Error as e:
                logging.exception(e)
                return False
        else: 
            return False

    def interpret(self, signature_path, modified_award_tex, image):
        """Render PDF award using AWS instance

        Arguments: 
            self
            signature_path:         string. name of signature file, not full path.
            image:                  bytes. contents of image/jpeg file, pulled down from Google Storage Bucket
            modified_award_tex:     bytes. contents of tex file modified with user information
        Returns: 
            Returns bytes of PDF on success, None on failure
        """
        # Only continue if we could appropriately save our signature file to AWS instance
        if self.save_image_to_disk(signature_path, image) is True: 
            logging.info('Interpeter.interpret(): Rendering PDF on AWS instance')
            # POST tex to AWS instance, get PDF
            url = 'http://54.203.128.106:80/pdf'
            try: 
                result = urlfetch.fetch(
                    url=url,
                    payload=modified_award_tex,
                    method=urlfetch.POST,
                    headers={
                        'Content-Type': 'application/octet-stream'
                    })

                # Return PDF contents if successful
                logging.info('Interpreter.interpret(): POST result was {}'.format(result.content))
                if result.status_code == 200: 
                    return result.content 
                else:
                    return None
            except urlfetch.Error as e:
                logging.exception(e)
                return None        

    def write_award_to_bucket(self, award_id, pdf):

        # Based off of code from views/users_signature.py  
        logging.info('Interpeter.write_award_to_bucket(): writing to cloud storage')
        try:        
            # Make file name based on award id
            filename = 'award_{}.pdf'.format(award_id)

            # Open write connection to cloud storage bucket
            connection = cloudstorage.open('/cs467maia-backend.appspot.com/awards/{}'.format(filename), mode='w', content_type='application/pdf')
                
            # Write raw image data & close connection to bucket
            connection.write(pdf)
            connection.close()
            return True # success

        except Exception as e:
            # Don't raise any exception, but log exception and return error to user
            logging.exception(e)
            return False # failure
        

# References
# [1] https://cloud.google.com/appengine/docs/standard/python/issue-requests            re: code example for using urlfetch
# [2] https://www.programiz.com/python-programming/methods/built-in/bytes               re: use of bytes()
# See references in views/users_signature.py re: uploading to bucket