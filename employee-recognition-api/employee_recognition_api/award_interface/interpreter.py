#from latex import build_pdf 
import os
import logging

class Interpreter:

	def __init__(self):
		print('do nothing')

	def interpret(self):

		path = os.path.dirname(os.path.abspath(__file__))
		

	   f = open(tex_file, 'r')
		min_latex = ( # from the example on pypi
        	r"\documentclass{article}"
            r"\begin{document}"
            r"Hello, world!"
            r"\end{document}"
        )

		pdf = build_pdf(f.read())
		pdf = build_pdf(min_latex, '../../{}'.format(path))
		p = open('award.pdf', 'w')
		p.write(bytes(pdf))

		# latex lib requires tex binary -- do other libraries?

# References
# [1] https://pypi.org/project/latex/
# [2] https://stackoverflow.com/questions/38431066/runtime-error-in-build-pdf-module-of-latex-python 			re: host to get latex binaries
# [3] https://stackoverflow.com/questions/3430372/how-to-get-full-path-of-current-files-directory-in-python 	re: running pwd in python
# [4] https://github.com/mbr/latex/blob/master/latex/build.py 													re: specifying texinputs in build_pdf()