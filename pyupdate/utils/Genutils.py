import re
import asyncio
from pyupdate import BASE_FILE
from pyupdate import update_from_file
from ._anonymous_class import ANONYMOUS

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
        """count the new lines to update (broken)"""
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

async def Fversion(file):
        """returns the version of the file if there is any to let you see if the file is older or newer"""
        lines = await BASE_FILE._read_file(ANONYMOUS(), file)
        for line in lines:
            match = re.search('__version__(.*)', line)
            if match:
                return match.group(1).strip(" =''").strip('""')
        return False

async def compare_versions(version1, version2):
        """take two versions with a 3 decimal points and return the higher one"""
        v1 = version1.split('.')
        v2 = version2.split('.')

        if int(v1[0]) > int(v2[0]):
                return version1
        if int(v1[0]) < int(v2[0]):
                return version2
        
        _v1_float = int(v1[1]) +float('0.%s' %v1[2])
        _v2_float = int(v2[1]) +float('0.%s' %v2[2])
        return version1 if _v1_float > _v2_float else version2
