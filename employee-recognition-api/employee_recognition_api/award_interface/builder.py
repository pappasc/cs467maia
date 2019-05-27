import os 
import logging
import datetime
from ..db_interface.query_tool import QueryTool

if os.environ.get('ENV') != 'local':
    import cloudstorage 

class Builder: 
    """Build and retrieve the stuff (award tex data, image)
        required to create a PDF award
    """

    def __init__(self, connxn_data, type_string): 
        """Reads template LaTeX file into memory based on type provided

        Arguments: 
            self
            type_string: string. type of award - 'month' or 'week'
        """
        # Open file for reading and save in memory
        path = os.path.dirname(os.path.abspath(__file__))
        f = open('{}/award.tex'.format(path), 'r')
        self.file = f.read() 
        self.type_string = type_string
        self.connxn_data = connxn_data

    def query_database_for_data(self, data):
        """Queries database for data required for the award

        Arguments: 
            self
            data:   dict. POST request data, as well as data from the result of the post request
                keys = award_id, authorizing_user_id, receiving_user_id
        Returns: dict for use in generate_award_tex()
        """

        #  Retrieve authorizing user id's information
        query_tool = QueryTool(self.connxn_data)
        result = query_tool.get_by_id('users', {'user_id': int(data['authorizing_user_id'])})
        authorizing_first_name = result['first_name']
        authorizing_last_name = result['last_name']
        signature_path = result['signature_path']

        # Retrieve receiving user id's information
        result = query_tool.get_by_id('users', {'user_id': int(data['receiving_user_id'])})
        receiving_first_name = result['first_name']
        receiving_last_name = result['last_name']
        email_address = result['email_address']

        # Retrieve award information
        # TODO: Determine if this can be removed and replaced with data dict.
        result = query_tool.get_by_id('awards', {'award_id': int(data['award_id'])})
        awarded_datetime = result['awarded_datetime']
        
        # Parse awarded_datetime to find year, month (in words) and day
        parsed_datetime = datetime.datetime.strptime(awarded_datetime, '%Y-%m-%d %H:%M:%S')
        year = parsed_datetime.year

        if int(parsed_datetime.month) == 1: 
            month = 'January'
        elif int(parsed_datetime.month) == 2:
            month = 'February'
        elif int(parsed_datetime.month) == 3:
            month = 'March'
        elif int(parsed_datetime.month) == 4:
            month = 'April'
        elif int(parsed_datetime.month) == 5:
            month = 'May'
        elif int(parsed_datetime.month) == 6:
            month = 'June'
        elif int(parsed_datetime.month) == 7:
            month = 'July'
        elif int(parsed_datetime.month) == 8:
            month = 'August'
        elif int(parsed_datetime.month) == 9:
            month = 'September'
        elif int(parsed_datetime.month) == 10:
            month = 'October'
        elif int(parsed_datetime.month) == 11:
            month = 'November'
        elif int(parsed_datetime.month) == 12:
            month = 'December'
        day = parsed_datetime.day

        # Return a dict required for award tex generation from template
        return {
            'AuthorizeFirstName': authorizing_first_name, 
            'AuthorizeLastName': authorizing_last_name, 
            'ReceiveFirstName': receiving_first_name, 
            'ReceiveLastName': receiving_last_name,
            'SignaturePath': signature_path, 
            'Month': month, 
            'Year': str(year), 
            'Day': str(day),
            'email_address': email_address
        }

    
    def query_bucket_for_image(self, signature_path):
        """Queries Google Storage Bucket for image

        Based off of code from views/users_signature.py 
        
        Arguments: 
            self
            signature_path: string. signature file name to query for

        Returns:
            bytes of image or None if unsuccessful
        """
        # Connect to the Cloud Storage bucket, read image contents, and close connection 
        try:      
            connection = cloudstorage.open('/cs467maia-backend.appspot.com/signatures/{}'.format(signature_path))              
            image = connection.read()
            connection.close()

            # Return bytes of image if successful
            return bytes(image)

        # Catch and log any exception - cloudstorage seems less predictable
        except Exception as e: 
            logging.exception(e)
            return None

    def generate_award_tex(self, data):
        """Replaces values within the .tex template

        Arguments: 
            self
            data: dict. Contains all information to input into template
                'AuthorizeFirstName': First name of authorizing user
                'AuthorizeLastName': Last name of authorizing user
                'ReceiveFirstName': First name of receiving user
                'ReceiveLastName': Last name of receiving user
                'SignaturePath': Name of file to include as signature
                'Month': Month of awarded_datetime, i.e. 'May', 'June'
                'Day': Day of awarded_datetime
                'Year': Year of awarded_datetime

        Returns tex contents of generated award
        """
        self.file = self.file.replace('AuthorizeFirstName', data['AuthorizeFirstName'])
        self.file = self.file.replace('AuthorizeLastName', data['AuthorizeLastName'])
        self.file = self.file.replace('ReceiveFirstName', data['ReceiveFirstName'])
        self.file = self.file.replace('ReceiveLastName', data['ReceiveLastName'])
        self.file = self.file.replace('SignaturePath', data['SignaturePath'])
        self.file = self.file.replace('Month', data['Month'])
        self.file = self.file.replace('Day', data['Day'])
        self.file = self.file.replace('Year', data['Year'])
        self.file = self.file.replace('Type', self.type_string.capitalize())
        return bytes(self.file)

# References
# [1] https://docs.python.org/2/tutorial/inputoutput.html#reading-and-writing-files                             re: file I/O
# [2] https://www.tutorialspoint.com/python/string_replace.htm                                                  re: replace()     
# [3] https://stackoverflow.com/questions/3430372/how-to-get-full-path-of-current-files-directory-in-python     re: running pwd in python
# [4] See references in views/users_signature.py re: uploading to bucket
# [5] https://docs.python.org/2/library/datetime.html re: datetime
# [6] https://groups.google.com/forum/#!topic/google-appengine/LiwVqZvlO8A                                      re: can't run in dev w/o access token