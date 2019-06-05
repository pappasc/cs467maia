# award_driver.py
from builder import Builder
from interpreter import Interpreter
from distributer import Distributer
import logging

class AwardDriver:
    """Integrates all Builder, Interpreter, and Distributer functionality to 
        create PDF award & email out to receiving user
    """

    def __init__(self, connection_data, email_on=True):
        """Initializes AwardDriver by setting email_on & connection_data variables

        Arguments:
            self
            connection_data:    dictionary. connection data to interact with database.
                                keys = environment, username, password, database, connection_name
            email_on:           boolean. default is True. True = emails sent. False = emails not sent.
        """
        logging.info('AwardDriver.__init__(): initializing AwardDriver class')
        self.email_on = email_on 
        self.connection_data = connection_data

    def create_pdf(self, data): 
        """Build, interpret, and distribute PDF award

        Arguments: 
            self
            data:   dictionary. POST request data, as well as data from the result of the post request
                    keys = award_id, authorizing_user_id, receiving_user_id, awarded_datetime, type
        Returns: 
            True if email was POST to database successful. False if unsuccessful.
            Does NOT Return the result of following handling of PDF. 
            This is designed so that an admin could manually generate award & send out if there was an issue with PDF creation -- 
            the user isn't prevented from creating the award if there IS a problem.
        """
        # Set up instances of helper classes
        builder = Builder(self.connection_data, data['type'])
        interpreter = Interpreter()
        distributer = Distributer(data['award_id'])

        # Build the Award Contents
        logging.info('AwardDriver.create_pdf(): building award contents')
        award_data = builder.query_database_for_data(data)
        modified_award_tex = builder.generate_award_tex(award_data)
        image = builder.query_bucket_for_image(award_data['SignaturePath'])

        # Initialize boolean success/failure variables to None
        pdf, write_successful = (None, None)
        email_successful, deletion_successful, distributed_updated = (False, False, False) 

        # Build PDF from TEX + JPG if building award contents was successful
        if image is not None and modified_award_tex is not None: 
            logging.info('AwardDriver.create_pdf(): building PDF')
            pdf = interpreter.interpret(award_data['SignaturePath'], modified_award_tex, image)

        # Send email if we have a PDF generated, or just say we did if email_on is False (for testing)
        if pdf is not None:
            # Technically don't NEED to additionally write to storage bucket, but it allows for 
            # us to not lose award PDF if something goes wrong in this function
            # Writing to storage bucket instead of a SQL database because 
            #   1) this is transient / temporary data 
            #   2) it is not best practice to store files in a SQL database.
            logging.info('AwardDriver.create_pdf(): saving PDF to storage bucket')
            write_successful = interpreter.write_award_to_bucket(data['award_id'], pdf)
            if self.email_on is True: 
                logging.info('AwardDriver.create_pdf(): distributing email')
                email_successful = distributer.email_receiving_user(pdf, award_data['email_address'], data['type'])
            else: 
                email_successful = True

            # Show we sent email in database -- even if we're using no-email
            if email_successful is True: 
                logging.info('AwardDriver.create_pdf(): updating distributed in database')
                distributed_updated = distributer.update_distributed_in_database(self.connection_data)

        # Clean-up PDF from storage bucket
        if email_successful is True and write_successful is True: 
            logging.info('AwardDriver.create_pdf(): deleting PDF from storage bucket')
            deletion_successful = distributer.delete_award_from_bucket()

        # Only returns true if email sent
        logging.info('AwardDriver.create_pdf(): returning {}'.format(email_successful))
        return email_successful

# References
# [1] https://stackoverflow.com/questions/16348815/python-assigning-multiple-variables-to-same-value-list-behavior      re: assigning multiple variables in one line in python
