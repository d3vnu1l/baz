from unittest import TestCase

import subprocess
import os


# cd to repo root
REPO_ROOT_ABS_PATH = os.path.dirname(os.path.abspath(__file__)) + "/../../"
os.chdir(REPO_ROOT_ABS_PATH)
# Set up PYTHONPATH to mimic pip installed environment
os.environ['PYTHONPATH'] = REPO_ROOT_ABS_PATH # visible in this process + all children

BAZ_SCRIPT_PATH='bin/baz'


class TestBaz(TestCase):
    def test_help(self):
        help_return = subprocess.run([BAZ_SCRIPT_PATH, '--help'], stdout=subprocess.PIPE, encoding="utf-8")

        # Output should begin with `usage:` if we have reached the help menu successfully
        self.assertTrue(str(help_return.stdout).startswith('usage:'))

    def test_print(self):
        help_return = subprocess.run([BAZ_SCRIPT_PATH, '--print-settings'], stdout=subprocess.PIPE, encoding="utf-8")

        # Output should begin with `Tool: ` if we have reached the print menu successfully
        self.assertTrue(str(help_return.stdout).startswith('Tool: '))

