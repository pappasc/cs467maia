import os 

class Builder: 
    """Creates award tex data, based on month.tex or week.tex"""

    def __init__(self, type_string): 
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

    def generate_award_tex(self, block):
        """Replaces values within the .tex template

        Arguments: 
            self
            block: dict. Contains all information to input into template
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
        self.file = self.file.replace('AuthorizeFirstName', block['AuthorizeFirstName'])
        self.file = self.file.replace('AuthorizeLastName', block['AuthorizeLastName'])
        self.file = self.file.replace('ReceiveFirstName', block['ReceiveFirstName'])
        self.file = self.file.replace('ReceiveLastName', block['ReceiveLastName'])
        self.file = self.file.replace('SignaturePath', block['SignaturePath'])
        self.file = self.file.replace('Month', block['Month'])
        self.file = self.file.replace('Day', block['Day'])
        self.file = self.file.replace('Year', block['Year'])
        self.file = self.file.replace('Type', self.type_string)
        return self.file

# References
# [1] https://docs.python.org/2/tutorial/inputoutput.html#reading-and-writing-files                             re: file I/O
# [2] https://www.tutorialspoint.com/python/string_replace.htm                                                  re: replace()     
# [3] https://stackoverflow.com/questions/3430372/how-to-get-full-path-of-current-files-directory-in-python     re: running pwd in python