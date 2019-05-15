class Builder: 

    def __init__(self, type_string): 
        """Reads LaTeX file into memory based on type provided

        Arguments: 
            self
            type_string: string. type of award - 'month' or 'week'
        """

        # Open file for reading and save in memory
        f = open('{}.tex'.format(type_string), 'r')
        self.file = f.read() 


    def replace_all(self, block):
        self.file = self.file.replace('authorizeFirstName', block['authorizeFirstName'])
        self.file = self.file.replace('authorizeLastName', block['authorizeLastName'])
        self.file = self.file.replace('receiveFirstName', block['receiveFirstName'])
        self.file = self.file.replace('receiveLastName', block['receiveLastName'])
        self.file = self.file.replace('signaturePath', block['signaturePath'])
        self.file = self.file.replace('month', block['month'])
        self.file = self.file.replace('day', block['day'])
        self.file = self.file.replace('year', block['year'])

    def rewrite_file(self):
        f = open('award.tex', 'w')
        print(self.file)
        f.write(self.file)

    def worker(self, block):
        self.replace_all(block)
        self.rewrite_file()

    def cleanup(self):
        print('delete the award file')

        



# References
# [1]  https://docs.python.org/2/tutorial/inputoutput.html#reading-and-writing-files    # re: file I/O
# [2] https://www.tutorialspoint.com/python/string_replace.htm                          # re: replace()     
