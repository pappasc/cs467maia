from flask import Flask 
from latex import build_pdf
import os
import logging

interpreter_api = Flask(__name__)

# Does not work
@interpreter_api.route('/pdf', methods=['GET'])
def pdf():	
	""" This does not work, but was meant to build a pdf from latex file using
		a given texlive distribution.
	"""
	try: 
		tex_file = open('test.tex', 'r')
		tex_data = tex_file.read()
		pdf = build_pdf(min_latex, texinputs='/home/nkvavle/cs467maia/texlive/bin/x86_64-linux', builder='pdflatex')
		return bytes(pdf)
	except Exception as e: 
		logging.exception(e) 

if __name__ == '__main__': 
	interpreter_api.run(host='0.0.0.0', port=8080)

# [1] https://cloud.google.com/appengine/docs/standard/python/tools/using-local-server re: pdb
# [2] https://guides.lib.wayne.edu/latex/compiling 														re: bypassing latex lib
# [3] https://stackoverflow.com/questions/2559076/how-do-i-redirect-output-to-a-variable-in-shell 			re: redirecting file to var
# [4] https://stackoverflow.com/questions/2152114/google-app-engine-to-run-executable-files 				re: can't run binary files
# [5] https://pypi.org/project/latex/
# [6] https://stackoverflow.com/questions/38431066/runtime-error-in-build-pdf-module-of-latex-python            re: host to get latex binaries
# [7] https://github.com/mbr/latex/blob/master/latex/build.py                                                   re: specifying texinputs in build_pdf()
# [8] https://tex.stackexchange.com/questions/265688/how-can-i-add-the-latex-on-python-path 					 re: adding to path
# [9] https://stackoverflow.com/questions/5971312/how-to-set-environment-variables-in-python 					 re: effectively adding to os var
# [10] https://pythonhow.com/how-a-flask-app-works/ re: use of main
# [11] https://codefresh.io/docker-tutorial/hello-whale-getting-started-docker-flask/ re: flask & docker - use of host 0.0.0.0