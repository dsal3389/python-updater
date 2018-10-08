import asyncio
from pyupdate import update_from_file

async def _update_file_thread(file, update_file, sleep):
	update = update_from_file(file, update_file)
	await update.update(sleep=sleep)

async def update_files(files:dict, sleep=0.3):
	"""to update more then 1 file use this command and pass arguments as a dict
	x = {fileName: updateFileName} for argument in the dict it takes the file name
	and thats the script you want to update and the updateFileName is the file to update from"""
	_tasks = [_update_file_thread(file, update, sleep) for file, update in files.items()]
	await asyncio.wait(_tasks)

async def new_lines_count(file:str, update_file:str):
        with open(file, 'r', encoding='utf-8')as _file:
                file_lines = _file.readlines()

        with open(update_file, 'r', encoding='utf-8')as _update:
                update_lines = _update.readlines()

        new_lines_counter = 0
        for place, line in reversed(list(enumerate(file_lines))):
                try:
                        if line == update_lines[place]:
                                continue
                        else:
                                new_lines_counter+=1
                except IndexError:
                        new_lines_counter+=1
        return new_lines_counter
        
