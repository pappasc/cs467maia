from google.appengine.api import mail, mail_errors
from ..db_interface.query_bucket_tool import QueryBucketTool

class Distributer:

    def __init__(self, award_id): 
        logging.info('Distributer.__init__(): initializing Distributer class')
        self.file_name = 'award_{}.pdf'.format(award_id)

    def email_receiving_user(self, email_address, type_string):
        logging.info('Distributer.email_receiving_user(): sending email to the receiving_user at {}'.format(email_address))
        try: 
            mail.send_mail(
                sender='<Maia Group> kvavlen@oregonstate.edu',
                to=email_address,
                subject='Congratulations! You are Emloyee of the {}!'.format(capitalize(type_string)), 
                attachments=[(self.file_name, self.file_contents)]
            )
            return True 

        # Capture BadRequestError, it's unlikely any other exceptions will occur
        except mail_errors.BadRequestError as e:
            logging.info('Distributer.email_receiving_user(): something went wrong, email was not successful')
            logging.exception(e)
            return False

    def delete_award_from_bucket(self):
        logging.info('Distributer.delete_award_from_bucket(): deleting {} from storage bucket'.format(self.file_name))
        query_bucket_tool = QueryBucketTool()
        
        success_bool = query_bucket_tool.delete('awards/{}'.format(self.file_name))

        if success_bool is False: 
            logging.info('Distributer.query_bucket_for_award(): an error occurred, file was not deleted from bucket. \
                            Continuing, but manual cleanup is required.')
        
        return success_bool 

# References
# [1] https://cloud.google.com/appengine/docs/standard/python/mail/sending-mail-with-mail-api                                                        re: google app engine mail library
# [2] https://github.com/GoogleCloudPlatform/python-docs-samples/blob/6f5f3bcb81779679a24e0964a6c57c0c7deabfac/appengine/standard/mail/attachment.py re: example on how to send attachment in mail    
# [3] https://www.google.com/search?client=firefox-b-1-d&q=up+case+first+letter+python                                                               re: capitalize()
# [4] https://cloud.google.com/appengine/docs/standard/python/refdocs/modules/google/appengine/api/mail_errors#BadRequestError                       re: mail API exceptions/errors