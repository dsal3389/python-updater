import sys
import asyncio
from updaters import update_from_file

"""not in use right now"""

async def main(file, update):
	_update = update_from_file(file, update)
	await _update.update()
	print('the file (%s) was updated from (%s)' %(file, update))


if __name__=='__main__':
	if allowed_to_use:
		files = sys.argv[1:]
		try:
			file_to_update = files[0]
			update_from_file = files[1]
		except IndexError:
			raise NotImplementedError('missing index\n>>> python3 -m pyup fileToUpdate UpdateFormThisFile')
		else:
			loop = asyncio.get_event_loop()
			loop.run_until_complete(main(file_to_update, update_from_file))
	else:
		print('not allowed to use atm')
