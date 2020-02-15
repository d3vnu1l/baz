import subprocess
from pathlib import Path
import sys


# This is where we store the persistant configuration file
BAZ_PERSISTANT_DATA_FILE_LOCATION = str(Path.home()) + '/.config/baz/config.json'

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
