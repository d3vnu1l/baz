from dataclasses import dataclass
from pathlib import Path
import subprocess
import hashlib
import sys
import os


# Bazel commands that we will decorate, all other commands are a direct pass through.
COMMANDS_TO_DECORATE = ["build", "run", "test", "coverage"]

BUILD_SCRIPT_TEMPLATE = """\
#!/usr/bin/env bash
{command}
"""


def get_repo_root():
    repo_root = None
    try:
        repo_root = subprocess.check_output(['git', 'rev-parse', '--show-toplevel']).strip().decode('utf-8')
    except subprocess.CalledProcessError:
        pass    # The callee should handle None return if we are not in a valid repo

    return repo_root


@dataclass
class GeneratedConstants:
    '''This is for storing constants that require some computation'''

    def __init__(self):
        self.repo_root = get_repo_root()
        self.baz_config_file_location = str(Path.home()) + "/.config/baz/{unique_name}.json".format(
            unique_name = hashlib.sha1(self.repo_root.encode('utf-8')).hexdigest()
        )

    repo_root = None
    baz_config_file_location = None # This is where we store the persistant configuration file

