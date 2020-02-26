import os
import json

from baz.constants import GeneratedConstants


class Filesystem:
    '''This class abstracts and simplifies handling baz configs'''

    def delete_configuration(self):
        file_was_deleted = False
        if os.path.exists(self.generated_constants.baz_config_file_location):
            os.remove(self.generated_constants.baz_config_file_location)
            print("{} was deleted.".format(self.generated_constants.baz_config_file_location))
            file_was_deleted = True
        else:
            print("No configuration found, expected: {}".format(self.generated_constants.baz_config_file_location))

        return file_was_deleted


    def read_configuration(self):
        """Returns a configuration JSON struct from the filesystem. Returns None is no file exists."""
        persistent_data = None
        try:
            with open(self.generated_constants.baz_config_file_location, 'r') as f:
                persistent_data = json.load(f)
        except FileNotFoundError:
            pass

        return persistent_data


    def write_configuration(self, config_dictionary):
        success = False,
        # Create directory for config if it does not exist
        if not os.path.exists(os.path.dirname(self.generated_constants.baz_config_file_location)):
            try:
                os.makedirs(os.path.dirname(self.generated_constants.baz_config_file_location))
            except OSError:
                pass

        with open(self.generated_constants.baz_config_file_location, 'w') as f:
            json.dump(config_dictionary, f)
            success = True

        return success

    generated_constants = GeneratedConstants()
