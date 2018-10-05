from time import time
from os import path
from threading import Thread


__version__ = '0.0.1' # alpha
__auth__ = 'Daniel Sonbolian'


class UPDATE:
	def __init__(self, file):
		self.file = file

	def update_from_file(self, file):
		if not path.isfile(file):
			raise FileNotFoundError('File not found %s' %file)
		self.file_to_update = file
		return self

	def update(self):
		if hasattr(self, 'file_to_update'):
			with open(self.file_to_update, 'r')as _update:
				_update_lines = _update.readlines()
			with open(self.file, 'r')as _file:
				_file_lines =_file.readlines()

			for place, line in enumerate(_update_lines):
				try:
					if line == _file_lines[place]: continue # if the lines are the same continue the loop
				except IndexError:
					_file_lines.append(line)
				else:
					_file_lines[place] = line

			if len(_file_lines) > len(_update_lines):
				_file_lines = _file_lines[:len(_update_lines)] # mean that the updatefile deleted some lines at the end

			with open(self.file, 'w')as _file: # to overwrite the old content
				_file.writelines(_file_lines)
