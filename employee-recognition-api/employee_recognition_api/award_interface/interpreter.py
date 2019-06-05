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
        logging.debug('Interpreter.__init__(): do nothing')

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
            logging.debug('Interpeter.save_image_to_disk(): saving image to AWS instance')
            # POST image to AWS instance
            # Not using chunks because file sizes are relatively small
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
                if result.status_code == 200: 
                    logging.debug('Interpreter.save_image_to_disk(): POST /image was successful')
                    return True       
                else:
                    logging.info('Interpreter.save_image_to_disk(): POST /image was not successful')
                    return False
            except urlfetch.Error as e:
                logging.info('Interpreter.save_image_to_disk(): POST /image was not successful')
                logging.exception(e)
                return False
        else: 
            logging.info('Interpreter.save_image_to_disk(): could not POST /image - nothing to POST')
            return False

    def delete_image_from_disk(self, signature_path):
        """Delete signature image to disk from AWS instance 

        Arguments: 
            self
            signature_path: string. name of signature file, not full path.

        Returns: 
            True on success, False on failure
        """
        logging.debug('Interpeter.delete_image_from_disk(): deleting image from AWS instance')
        # DELETE image to AWS instance
        url = 'http://54.203.128.106:80/image/{}'.format(signature_path)
        try: 
            result = urlfetch.fetch(
                url=url,
                method=urlfetch.DELETE
            )
            
            # Log the result of the DELETE request, return True only if successful
            if result.status_code == 200: 
                logging.debug('Interpeter.delete_image_from_disk(): DELETE /image was successful')
                return True       
            else:
                logging.info('Interpeter.delete_image_from_disk(): DELETE /image was not successful')
                return False
        except urlfetch.Error as e:
            logging.info('Interpeter.delete_image_from_disk(): DELETE /image was not successful')
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
            logging.debug('Interpeter.interpret(): Rendering PDF on AWS instance')
            
            # POST tex to AWS instance, get PDF
            # Use 'application/octet-stream' as we're sending bytes of tex file
            # Not using chunks because file sizes are relatively small
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
                if result.status_code == 200: 
                    logging.debug('Interpeter.delete_image_from_disk(): POST /pdf was successful')
                    self.delete_image_from_disk(signature_path)
                    # Don't change what is returned based on success of clean-up efforts
                    return result.content 
                else:
                    logging.info('Interpeter.delete_image_from_disk(): POST /pdf was not successful')
                    return None
            except urlfetch.Error as e:
                logging.info('Interpeter.delete_image_from_disk(): POST /pdf was not successful')
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
        logging.debug('Interpeter.write_award_to_bucket(): writing to cloud storage')
        
        # Make file name based on award id
        filename = 'award_{}.pdf'.format(award_id)
        
        # Write file to storage bucket & return resulting boolean
        query_bucket_tool = QueryBucketTool()
        write_result = query_bucket_tool.post('awards/{}'.format(filename), pdf, 'application/pdf')
        if write_result is False: 
            logging.info('Interpreter.write_award_to_bucket(): writing to cloud storage failed')
        return write_result
