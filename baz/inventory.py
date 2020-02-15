from dataclasses import dataclass
from baz.bazel_prober import BazelProber
import baz.filesystem as filesystem


@dataclass
class BazConfigInventory:
    '''Class for managing the use configuration inventory'''

    def __init__(self):
        self.config_keys = BazelProber.get_config_keys()
        self.troubleshooting_keydict = BazelProber.get_troubleshooting_keydict()
        self.persistent_data = filesystem.read_configuration()
        if self.persistent_data is None:
            # Generate a config
            self.persistent_data = self.get_default_data()
            # Write to filesystem
            filesystem.write_configuration(self.persistent_data)

    def get_default_data(self):
        default_config = dict()
        """Form a 1-d dictionary containing all deafult values."""
        # Configs
        default_config.update(dict.fromkeys(self.config_keys, False))

        # Compilation Mode
        (compilation_mode_key,
         compilation_mode_values) = BazelProber.get_compilation_mode_keyvalues()
        default_config.update({
            compilation_mode_key[0]: compilation_mode_values[0],
        })

        # Toubleshooting
        default_config.update(dict.fromkeys(
            self.troubleshooting_keydict.keys(), False))

        # Default Bazel Path
        default_config.update({"tool": "bazel"})

        # Default bazel flags
        default_config.update({"bazelopts": None})

        return default_config

    def save_to_file(self, data):
        filesystem.write_configuration(data)
        self.persistent_data = data

    persistent_data = None
    config_keys = None
    troubleshooting_keydict = None
