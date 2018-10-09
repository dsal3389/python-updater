import asyncio
from pyupdate import BASE_FILE


class UPDATE(BASE_FILE):
	def __init__(self, file_to_update):
		self.file = file_to_update
		self._logged_text = {}

	@asyncio.coroutine
	def log_text(self, text, line_place=None, *, overwrite=True):
		if line_place is None:
			line_place = len(self._logged_text)
		else:
			if not isinstance(line_place, int):
				raise ValueError('line_place must be integer')
		self._logged_text[line_place] = [overwrite, str(text)]

	@asyncio.coroutine
	def commit(self):
		if len(self._logged_text) <= 0:
			return
		file_lines = yield from self._read_file(self.file)
		
		for key, value in self._logged_text.items():
			if value[0]: # if to overwrite True or False
				try:
					file_lines[key] = value[1] +'\n'
				except IndexError:
					for _ in range(len(file_lines), key+1):
						file_lines.append('\n')
					file_lines[key] = value[1] +'\n'
				continue

			elif len(file_lines) < key:
				for i in range(len(file_lines), key):
					file_lines.insert(i, '\n')	
			file_lines.insert(key, value[1])

		yield from self._write(self.file, file_lines)
				
