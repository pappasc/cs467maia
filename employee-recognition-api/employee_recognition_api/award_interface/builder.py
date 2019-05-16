class Builder: 

    def __init__(self, type_string): 
        """Reads template LaTeX file into memory based on type provided

        Arguments: 
            self
            type_string: string. type of award - 'month' or 'week'
        """

        # Open file for reading and save in memory
        f = open('{}.tex'.format(type_string), 'r')
        self.file = f.read() 

    def replace_template(self, block):
        """Replaces values within the .tex template

        Arguments: 
            self
            block: dict. Contains all information to input into template
                'authorizeFirstName': First name of authorizing user
                'authorizeLastName': Last name of authorizing user
                'receiveFirstName': First name of receiving user
                'receiveLastName': Last name of receiving user
                'signaturePath': Name of file to include as signature
                'month': Month of awarded_datetime, i.e. 'May', 'June'
                'day': Day of awarded_datetime
                'year': Year of awarded_datetime

        Returns self.file for testing purposes
        """
        self.file = self.file.replace('authorizeFirstName', block['authorizeFirstName'])
        self.file = self.file.replace('authorizeLastName', block['authorizeLastName'])
        self.file = self.file.replace('receiveFirstName', block['receiveFirstName'])
        self.file = self.file.replace('receiveLastName', block['receiveLastName'])
        self.file = self.file.replace('signaturePath', block['signaturePath'])
        self.file = self.file.replace('month', block['month'])
        self.file = self.file.replace('day', block['day'])
        self.file = self.file.replace('year', block['year'])
        return self.file

    def create_award_tex(self):
        """Creates award.tex file modified from month.tex or week.tex template.

        Arguments: self

        Returns: None, but creates the award.tex file
        """
        f = open('award.tex', 'w')
        print(self.file)
        f.write(self.file)

    def cleanup(self):
        """Deletes award.tex file
        
        Arguments: self

        Returns: none
        """
        print('delete the award file')

        



# References
# [1] https://docs.python.org/2/tutorial/inputoutput.html#reading-and-writing-files    # re: file I/O
# [2] https://www.tutorialspoint.com/python/string_replace.htm                          # re: replace()     
