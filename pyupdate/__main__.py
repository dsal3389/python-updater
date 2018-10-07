import sys
import asyncio
from UPDATE import UPDATE


async def main(file, update):
	_update = UPDATE(file)
	await _update.update_from_file(update)
	await _update.update()
	print('the file (%s) was updated from (%s)' %(file, update))


if __name__=='__main__':
	files = sys.argv[1:]
	try:
		file_to_update = files[0]
		update_from_file = files[1]
	except IndexError:
		raise NotImplementedError('missing index\n>>> python3 -m pyup fileToUpdate UpdateFormThisFile')
	else:
		loop = asyncio.get_event_loop()
		loop.run_until_complete(main(file_to_update, update_from_file))
