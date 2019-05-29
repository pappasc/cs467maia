
from builder import Builder
from interpreter import Interpreter
from distributer import Distributer

class AwardDriver:
    """Integrates all Builder, Interpreter, and Distributer functionality to 
        create PDF award & email out to receiving user
    """

    def __init__(self, email_on=True):
        """Initializes AwardDriver by setting email_on variable

        Arguments:
            self
            email_on: boolean. default is True. True = emails sent. False = emails not sent.
        """
        self.email_on = True 

    def create_pdf(self, connection_data, request_data): 
        """Build, interpret, and distribute PDF award

        Arguments: 
            self
            connection_data: dictionary. connection data to interact with database.
            request_data:    dictionary. POST award request data.

        Returns: 
            True if email was successful. False if unsuccessful.
        """
        # Set up instances of helper classes
        builder = Builder(connection_data, data['type'])
        interpreter = Interpreter()
        distributer = Distributer(data['award_id'])

        # Build the Award Contents
        award_data = builder.query_database_for_data(data)
        modified_award_tex = builder.generate_award_tex(award_data)
        image = builder.query_bucket_for_image(award_data['SignaturePath'])

        # Build PDF from TEX + JPG 
        # Initialize variables to None
        pdf, write_successful = (None, None)
        email_successful, deletion_successful = (False, False) 

        if image is not None and modified_award_tex is not None: 
            pdf = interpreter.interpret(award_data['SignaturePath'], modified_award_tex, image)
        if pdf is not None:
            # Technically don't NEED to write to bucket, but it allows for 
            # us to not lose award data if something goes wrong in this function
            # Writing to bucket instead of a SQL database because 
            #   1) this is transient / temporary data 
            #   2) it is not best practice to store files in a SQL database.
            write_successful = interpreter.write_award_to_bucket(data['award_id'], pdf)

            # Send email if we have a PDF
            if self.email_on is True: 
                email_successful = distributer.email_receiving_user(pdf, award_data['email_address'], data['type'])
            else: 
                email_successful = True

            # Show we sent email in database -- even if we're using no-email
            if email_successful is True: 
                distributed_updated = distributer.update_distributed_in_database(connection_data)

        # Clean-up PDF from bucket
        if email_successful is True: 
            deletion_successful = distributer.delete_award_from_bucket()

        # Only returns true if email sent
        return email_successful

# References
# [1] https://stackoverflow.com/questions/16348815/python-assigning-multiple-variables-to-same-value-list-behavior  re: assigning multiple variables in one line in python
