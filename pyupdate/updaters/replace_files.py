import os
import asyncio
from shutil import move as shutilMove
from shutil import Error as shutilError


class UPDATE(object):
	def __init__(self, files:dict, *, loop=None):
		self.files = files
		self._settings ={
			'directory':{
				'create_if_not_exists': True, # if the path dosent exists to the replace file
				'raise_errors': True
			},
			'file':{
				'overwrite_if_exists': True, # in case there is already a file with the same name 
				'raise_errors': True
			}
		}

		self.loop = loop or asyncio.get_event_loop()

	def __repr__(self):
		return 'this mostly for update image fils staff like that if you want to update file\n\
			use update_from_line or update_from_lines'

	def __str__(self):
		return self.settings

	@asyncio.coroutine
	def start(self) -> bool:
		""""start to replace/create/move files and return true if files are replaced with no probloms
		or false (this is in case you muted the error rasing and you still want to know if everything wend as needed)"""
		_tasks = [self._start(file, to_replace) for file, to_replace in self.files.items()]
		is_failed = yield from asyncio.wait(_tasks, loop=self.loop)
		return is_failed

	@asyncio.coroutine
	def _start(self, file, to_replace):
		_file, _dir = yield from asyncio.gather(self._replace_file_with(file),
						        self._to_replace_file(to_replace)
						        , loop=self.loop)
		if any(i==False for i in [_file, _dir]):
			return False
		
		try:
			os.remove(_dir[0])
		except FileNotFoundError:
			pass
		try:
			shutilMove(_file[0], _dir[1])
		except Exception as e:
			if self.settings['file']['overwrite_if_exists']:
				try:
					os.remove(_dir[0])
				except FileNotFoundError:
					pass
				shutilMove(_file[0], _dir[1])
			if self.settings['directory']['raise_errors']:
				raise e
			
	@asyncio.coroutine
	def _replace_file_with(self, file):
		_file = self.settings['file']
		file_dir = os.path.dirname(os.path.abspath(file))
		if not os.path.isfile(os.path.join(file_dir, file)):
			if not _file['raise_errors']:
				return False
			raise FileNotFoundError('file (%s) hasent found' %(os.path.join(file_dir, file)))
		return os.path.join(file_dir, file), file_dir

	@asyncio.coroutine
	def _to_replace_file(self, file):
		_dir = self.settings['directory']
		to_replace_in_dir = os.path.dirname(os.path.abspath(file))
		if not os.path.exists(to_replace_in_dir):
			if not _dir['create_if_not_exists']:
				if _dir['raise_erros']:
					raise SystemError('(%s) not found' %to_replace_in_dir)
				return False
			os.mkdir(to_replace_in_dir)
		return os.path.join(to_replace_in_dir, file), to_replace_in_dir
	
	@property
	def settings(self) -> dict:
		return self._settings

	@settings.setter
	def settings(self, value:dict) -> None:
		if not isinstance(value, dict):
			raise ValueError('settings must be dict')
		
		value['directory']
		value['file'] # this will raise KeyError by itself
		self._settings=value
