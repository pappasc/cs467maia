from latex import build_pdf
import logging
import os 

class Interpreter:

    def __init__(self):
        print('do nothing')

    def test_this(self): 
        min_latex = ( # from the example on pypi
            r"\documentclass{article}"
            r"\begin{document}"
            r"Hello, world!"
            r"\end{document}"
        )        
        pdf = build_pdf(min_latex, builder='pdflatex')

    def interpret(self, variable):
        #f = open(tex_file, 'r')
        min_latex = ( # from the example on pypi
            r"\documentclass{article}"
            r"\begin{document}"
            r"Hello, world!"
            r"\end{document}"
        )
        #pdf = build_pdf(f.read())
        #path = os.environ.get('PATH')
        #os.environ['PATH'] = '/home/nkvavle/cs467maia/employee-recognition-api/employee_recognition_api/views/texlive/bin/x86_64-linux/pdflatex'
        pdf = build_pdf(min_latex, builder='pdflatex')
        #p = open('award.pdf', 'w')
     #   print(bytes(pdf))

# References
# [1] https://pypi.org/project/latex/
# [2] https://stackoverflow.com/questions/38431066/runtime-error-in-build-pdf-module-of-latex-python            re: host to get latex binaries
# [3] https://github.com/mbr/latex/blob/master/latex/build.py                                                   re: specifying texinputs in build_pdf()
# [4] https://stackoverflow.com/questions/3430372/how-to-get-full-path-of-current-files-directory-in-python     re: running pwd in python
# [5] https://tex.stackexchange.com/questions/265688/how-can-i-add-the-latex-on-python-path re: adding to path
# [6] https://stackoverflow.com/questions/5971312/how-to-set-environment-variables-in-python re: effectively adding to os var