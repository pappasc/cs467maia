# distributer.py
import logging
from ..db_interface.query_bucket_tool import QueryBucketTool
from ..db_interface.query_tool import QueryTool 
import os 

if os.environ.get('ENV') != 'local':
    from google.appengine.api import mail, mail_errors

class Distributer:
    """Distributes award via email to receiving_user
    """
    
    def __init__(self, award_id): 
        """Initializes Distributer class' file_name and award_id variables
    
        Arguments:
            self
            award_id: int. ID of award to be distributed.

        Returns: N/A
        """
        logging.debug('Distributer.__init__(): initializing Distributer class')
        self.file_name = 'award_{}.pdf'.format(award_id)
        self.award_id = award_id

    def email_receiving_user(self, attachment_bytes, email_address, type_string):
        """Emails award to receiving user

        Arguments: 
            self
            attachment_bytes:   bytes. PDF contents to be attached / sent via email.
            email_address:      string. Email address of receiving user to send award to
            type_string:        string. Type of award ('month' or 'week')

        Returns: 
            True on success, False on failure
        """

        # Send email
        logging.debug('Distributer.email_receiving_user(): sending email to the receiving_user at {}'.format(email_address))
        try: 
            mail.send_mail(
                sender='<Maia Group> kvavlen@oregonstate.edu',
                to=email_address,
                subject='Congratulations! You are Employee of the {}!'.format(type_string.capitalize()), 
                body="""Congratulations! 

                Your award is attached to this email. Keep up the good work!
                """,
                attachments=[('EmployeeOfThe{}.pdf'.format(type_string.capitalize()), attachment_bytes)]
            )
            logging.debug('Distributer.email_receiving_user(): email was successful')
            # Return True on success
            return True 

        # Capture BadRequestError, it's unlikely any other exceptions will occur
        except mail_errors.BadRequestError as e:
            logging.info('Distributer.email_receiving_user(): email was not successful')
            logging.exception(e)
            # Return False on failure
            return False

    def delete_award_from_bucket(self):
        """Delete award from Google App Engine storage bucket

        Arguments: self
        Returns: True if successful, False is failure
        """
        logging.debug('Distributer.delete_award_from_bucket(): deleting {} from storage bucket'.format(self.file_name))
        
        # Call helper function to delete the award (named with award_id) from storage bucket
        query_bucket_tool = QueryBucketTool()
        success_bool = query_bucket_tool.delete('awards/{}'.format(self.file_name))

        if success_bool is False: 
            logging.info('Distributer.delete_award_from_bucket(): an error occurred, file was not deleted from bucket. \
                            Continuing, but manual cleanup is required.')

        # Return True if successful, False if not        
        return success_bool 

    def update_distributed_in_database(self, connection_data):
        """Update 'distributed' field in award entry (in SQL database) to true to 
            indicate that award has been distributed
            
        Arguments: 
            self
            connection_data: dictionary with connection data for database
                keys:   environment, username, password, conenction_name 
        Returns:
            True if successful, False if failure
        """

        # Update entry distributed column to 'true' based on award_id
        logging.debug('Distributer.update_award_distributed(): updating distributed boolean in awards database')
        query_tool = QueryTool(connection_data)
        data = {
            'award_id': self.award_id
        }
        result = query_tool.put_by_id('awards', data)

        # Determine success based on presence of 'award_id' in result
        try: 
            # If successful, return True
            if int(result['award_id']) == self.award_id:
                logging.debug('Distributer.update_award_distributed(): updating distributed boolean was successful')
                return True 

        # If unsuccessful, return False
        except KeyError as e:
            logging.info('Distributer.update_award_distributed(): updating distributed boolean was not successful')
            logging.exception(e)
            return False

# References
# [1] https://cloud.google.com/appengine/docs/standard/python/mail/sending-mail-with-mail-api                                                        re: google app engine mail library
# [2] https://github.com/GoogleCloudPlatform/python-docs-samples/blob/6f5f3bcb81779679a24e0964a6c57c0c7deabfac/appengine/standard/mail/attachment.py re: example on how to send attachment in mail    
# [3] https://www.google.com/search?client=firefox-b-1-d&q=up+case+first+letter+python                                                               re: capitalize()
# [4] https://cloud.google.com/appengine/docs/standard/python/refdocs/modules/google/appengine/api/mail_errors#BadRequestError                       re: mail API exceptions/errors