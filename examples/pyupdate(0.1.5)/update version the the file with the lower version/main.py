import os
import asyncio
from pyupdate import update_from_lines
from pyupdate.utils import Fversion, compare_versions


async def main(loop):
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    file1 = os.path.join(CURRENT_DIR, 'file1.py')
    file2 = os.path.join(CURRENT_DIR, 'file2.py')
    
    v1, v2 = await asyncio.gather(Fversion(file1), # getting the file version
                                  Fversion(file2), loop=loop)
    compare = await compare_versions(v1, v2) # returns the higher version
    print("file1: " +v1,"file2: " +v2,'compared: ' +compare, sep=' | ')

    obj = update_from_lines(file2) if compare == v1 else update_from_lines(file1)
    await obj.log_text('__version__="%s"' %compare, 0) # change the version to the higher one
    await obj.commit() #                    note: line 
    

if __name__=='__main__':
    loop=asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
