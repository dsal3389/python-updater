import asyncio
from pyupdate import UPDATE

"""update updateText.txt version to this file version"""

__version__ = '0.0.1'

async def main(o):
	await o.update_from_file(__file__) # this file
	await o.update(sleep=0)

if __name__=='__main__':
	x = UPDATE('updateText.txt')
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main(x))

