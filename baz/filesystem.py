import os
import json

from baz.constants import BAZ_PERSISTANT_DATA_FILE_LOCATION


def delete_configuration():
    file_was_deleted = False
    if os.path.exists(BAZ_PERSISTANT_DATA_FILE_LOCATION):
        os.remove(BAZ_PERSISTANT_DATA_FILE_LOCATION)
        file_was_deleted = True

    return file_was_deleted


def read_configuration():
    """Returns a configuration JSON struct from the filesystem. Returns None is no file exists."""
    persistent_data = None
    try:
        with open(BAZ_PERSISTANT_DATA_FILE_LOCATION, 'r') as f:
            persistent_data = json.load(f)
    except FileNotFoundError:
        pass

    return persistent_data


def write_configuration(config_dictionary):
    success = False,
    # Create directory for config if it does not exist
    if not os.path.exists(os.path.dirname(BAZ_PERSISTANT_DATA_FILE_LOCATION)):
        try:
            os.makedirs(os.path.dirname(BAZ_PERSISTANT_DATA_FILE_LOCATION))
        except OSError:
            pass

    with open(BAZ_PERSISTANT_DATA_FILE_LOCATION, 'w') as f:
        json.dump(config_dictionary, f)
        success = True

    return success
