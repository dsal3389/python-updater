import re
import asyncio
from os import path


__version__='0.0.2'
__auth__='Daniel Sonbolian'


class UPDATE:
	def __init__(self, file, *, loop=None):
		if not path.isfile(file):
			raise FileNotFoundError('(%s) was not found' %file)
		self.file = file
		self._loop = loop or asyncio.get_event_loop()

	def __str__(self):
		return str(self.file)

	@asyncio.coroutine
	def Fversion(self):
		"""returns the version of the file if there is any to let you see if the file is older or newer"""
		lines = yield from self._read_file(self.file)
		for line in lines:
			match = re.search('__version__(.*)', line)
			if match:
				return match.group(1).strip(" =''").strip('""')
		return False

	@asyncio.coroutine
	def update_from_file(self, update_file):
		"""get a file name as argument and update the file with the given file"""
		if not path.isfile(update_file):
			raise FileNotFoundError('given file to update from not found (%s)' %update_file)
		self.update_file = update_file

	@asyncio.coroutine
	def update(self, *, sleep=0.3):
		"""executing the update from a file only for now"""
		(file, update) = yield from asyncio.gather(
						self._read_file(self.file),
						self._read_file(self.update_file),
						loop=self._loop
					)

		for place,line in enumerate(update):
			try:
				if line == file[place]: continue
			except IndexError:
				file.append(line)
			else:
				file[place] = line
			finally:
				yield from asyncio.sleep(sleep)

		if len(file) > len(update): # deletes the deleted files at the end if there is any
			file = file[:len(update)]

		yield from self._write(self.file, file) # a func that overwrite
		return

	@asyncio.coroutine
	def _write(self, file, content):
		"""overwrite to a file the given content as a list"""
		with open(self.file, 'w')as f:
			f.writelines(content)
		return

	@asyncio.coroutine
	def _read_file(self, file_to_read):
		"""read all from the given file"""
		with open(file_to_read, 'r')as f:
			lines = f.readlines()
		return lines # asyncio dosent support files yet


async def _update_file_thread(file, update_file, sleep):
	update = UPDATE(file)
	await update.update_from_file(update_file)
	await update.update(sleep=sleep)

async def update_files(files:dict, sleep=0.3):
	"""to update more then 1 file use this command and pass arguments as a dict
	x = {fileName: updateFileName} for argument in the dict it takes the file name
	and thats the script you want to update and the updateFileName is the file to update from"""
	_tasks = [_update_file_thread(file, update, sleep) for file, update in files.items()]
	await asyncio.wait(_tasks)
