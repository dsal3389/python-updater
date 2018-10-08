import asyncio

class BASE_FILE:

    @asyncio.coroutine
    def _write(self, file, content):
            """overwrite to a file the given content as a list"""
            with open(self.file, 'w', encoding='utf-8')as f:
                    f.writelines(content)

    @asyncio.coroutine
    def _read_file(self, file_to_read):
            """read all from the given file"""
            with open(file_to_read, 'r', encoding='utf-8')as f:
                    lines = f.readlines()
            return lines # asyncio dosent support files yet
    
    @asyncio.coroutine
    def Fversion(self):
            """returns the version of the file if there is any to let you see if the file is older or newer"""
            lines = yield from self._read_file(self.file)
            for line in lines:
                    match = re.search('__version__(.*)', line)
                    if match:
                            return match.group(1).strip(" =''").strip('""')
            return False
