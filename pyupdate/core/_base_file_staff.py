import asyncio

class BASE_FILE:

    @asyncio.coroutine
    def _write(self, file:str, content:list) -> None:
            """overwrite to a file the given content as a list"""
            with open(self.file, 'w', encoding='utf-8')as f:
                    f.writelines(content)

    @asyncio.coroutine
    def _read_file(self, file_to_read:str) -> list:
            """read all from the given file"""
            with open(file_to_read, 'r', encoding='utf-8')as f:
                    lines = f.readlines()
            return lines # asyncio dosent support files yet
