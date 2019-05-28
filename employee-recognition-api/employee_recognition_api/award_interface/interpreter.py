import json
import logging
import os 
from ..db_interface.query_bucket_tool import QueryBucketTool

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
            logging.info('Interpeter.save_image_to_disk(): saving image to AWS instance')
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
                
                # Log the result of the POST request, return True only if successful -- otherwise return False
                logging.info('Interpreter.save_image_to_disk(): POST /image result was {}'.format(result.content))
                if result.status_code == 200: 
                    return True       
                else:
                    return False
            except urlfetch.Error as e:
                logging.exception(e)
                return False
        else: 
            return False

    def delete_image_from_disk(self, signature_path):
        """Delete signature image to disk from AWS instance 

        Arguments: 
            self
            signature_path: string. name of signature file, not full path.

        Returns: 
            True on success, False on failure
        """
        logging.info('Interpeter.delete_image_from_disk(): deleting image from AWS instance')
        # POST image to AWS instance
        url = 'http://54.203.128.106:80/image/{}'.format(signature_path)
        try: 
            result = urlfetch.fetch(
                url=url,
                method=urlfetch.DELETE
            )
            
            # Log the result of the DELETE request, return True only if successful
            logging.info('Interpreter.delete_image_from_disk(): POST /image result was {}'.format(result.content))
            if result.status_code == 200: 
                return True       
            else:
                return False
        except urlfetch.Error as e:
            logging.exception(e)
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

                # Return PDF contents if successful, otherwise return None
                logging.info('Interpreter.interpret(): POST /pdf result was {}'.format(result.content))
                if result.status_code == 200: 
                    self.delete_image_from_disk(signature_path)
                    # Don't change what is returned based on success of clean-up efforts
                    return result.content 
                else:
                    return None
            except urlfetch.Error as e:
                logging.exception(e)
                return None        

    def write_award_to_bucket(self, award_id, pdf):
        """Write PDF award to Google App Engine Storage Bucket for cs467maia-backend

        Based off of code from views/users_signature.py

        Arguments: 
            self
            award_id:   int. award id for the award, to be used in the pdf file name
            pdf:        bytes. content of PDF file.
    
        Returns: 
            Returns True on success, False on failure
        """   
        logging.info('Interpeter.write_award_to_bucket(): writing to cloud storage')
        
        # Make file name based on award id
        filename = 'award_{}.pdf'.format(award_id)
        
        # Write file to storage bucket & return resulting boolean
        query_bucket_tool = QueryBucketTool()
        write_result = query_bucket_tool.post('awards/{}'.format(filename), pdf, 'application/pdf')
        return write_result

# References
# [1] https://cloud.google.com/appengine/docs/standard/python/issue-requests            re: code example for using urlfetch
# [2] https://www.programiz.com/python-programming/methods/built-in/bytes               re: use of bytes()
# [3] See references in views/users_signature.py re: uploading to bucket