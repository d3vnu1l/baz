from pathlib import Path
import subprocess
import hashlib
import sys
import os


def get_repo_root():
    repo_root = None
    try:
        repo_root = subprocess.check_output(['git', 'rev-parse', '--show-toplevel']).strip().decode('utf-8')
    except subprocess.CalledProcessError:
        pass    # The callee should handle None return if we are not in a valid repo

    return repo_root


# This is where we store the persistant configuration file
BAZ_PERSISTANT_DATA_FILE_LOCATION = str(Path.home()) + "/.config/baz/{unique_name}.json".format(
    unique_name = hashlib.sha1(get_repo_root().encode('utf-8')).hexdigest()
)

# Bazel commands that we will decorate, all other commands are a direct pass through.
COMMANDS_TO_DECORATE = ["build", "run", "test", "coverage"]

BUILD_SCRIPT_TEMPLATE = """\
#!/usr/bin/env bash
{command}
"""
