from google.appengine.api import mail

class Distributer:

    def __init__(self): 


    def query_bucket_for_award(self, award_id):

    def email_receiving_user(self, data):
        mail.send_mail(
            sender='<Maia Group> kvavlen@oregonstate.edu',
            to=data['email_address'],
            subject='Congratulations! You are Emloyee of the {}!'.format(capitalize(data['type'])), 
            attachments=[(self.pdf_name, self.pdf_contents)]
        )
            


# References
# [1] https://cloud.google.com/appengine/docs/standard/python/mail/sending-mail-with-mail-api                                                        re: google app engine mail library
# [2] https://github.com/GoogleCloudPlatform/python-docs-samples/blob/6f5f3bcb81779679a24e0964a6c57c0c7deabfac/appengine/standard/mail/attachment.py re: example on how to send attachment in mail    re: attachments
# [3] https://www.google.com/search?client=firefox-b-1-d&q=up+case+first+letter+python                                                               re: capitalize()