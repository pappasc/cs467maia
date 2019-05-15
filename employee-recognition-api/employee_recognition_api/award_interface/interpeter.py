from latex import build_pdf 

class Interpreter:

	def __init__(self):
		print('do nothing')

	def interpret(self, tex_file):
		f = open(tex_file, 'r')
		min_latex = (r"\documentclass{article}"
             r"\begin{document}"
             r"Hello, world!"
             r"\end{document}")

		pdf = build_pdf(min_latex)
		p = open('award.pdf', 'w')
		p.write(bytes(pdf))


# References
# [1] https://pypi.org/project/latex/
# [2] https://stackoverflow.com/questions/38431066/runtime-error-in-build-pdf-module-of-latex-python re: host to get latex binaries