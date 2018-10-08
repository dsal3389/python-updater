import re
import asyncio
from os import path
from pyupdate import BASE_FILE


class UPDATE(BASE_FILE):
	def __init__(self, file, update_file, *, loop=None):
		if not path.isfile(file) or not path.isfile(update_file):
			raise FileNotFoundError('One of the given files hasent found')
		self.file = file
		self._update = update_file
		self._loop = loop or asyncio.get_event_loop()

	def __str__(self):
		return str(self.file)

	@asyncio.coroutine
	def update(self, *, sleep=0.3):
		"""executing the update from a file only for now"""
		(file, update) = yield from asyncio.gather(
						self._read_file(self.file),
						self._read_file(self._update),
						loop=self._loop
					)

		_need_update = False
		for place,line in enumerate(update):
			try:
				if line == file[place]: continue
			except IndexError:
				file.append(line)
				_need_update = True
			else:
				file[place] = line
				_need_update = True
			finally:
				yield from asyncio.sleep(sleep)

		if len(file) > len(update): # deletes the deleted lines at the end if there is any
			file = file[:len(update)]

		if _need_update:
			yield from self._write(self.file, file) # a func that overwrite
