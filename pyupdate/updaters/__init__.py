try:
    from pyupdate.updaters.update_from_file import UPDATE as update_from_file
except ModuleNotFoundError:
    from .update_from_file import UPDATE as update_from_file


__all__=['update_from_file']
