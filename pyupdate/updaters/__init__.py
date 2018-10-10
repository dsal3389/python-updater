try:
    from pyupdate.updaters.update_from_file import UPDATE as update_from_file
    from pyupdate.updaters.update_from_lines import UPDATE as update_from_lines
    from pyupdate.updaters.replace_files import UPDATE as replace_files
except ModuleNotFoundError:
    from .update_from_file import UPDATE as update_from_file


__all__=['update_from_file', 'update_from_lines', 'replace_files']
