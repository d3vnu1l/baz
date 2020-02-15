import os
import sys

from baz.constants import get_repo_root


class BazelProber:
    # Find all bazelrc, convert all lines to a list, and extract config names
    def get_config_keys():
        repo_root = get_repo_root()
        if repo_root is None:
            sys.exit()  # Just quit if we are not in a valid repo
        rc_lines_list = []
        config_list = []

        # Grab all bazelrc lines that contain a config
        for root, _, files in os.walk(repo_root):
            if "third_party" not in root:   # Todo: ignorefile
                for file in files:
                    if file == ".bazelrc":
                        with open(os.path.join(root, file)) as f:
                            for line in f:
                                # Enforce first contiguous strig contains ':' and does not start with a comment
                                if ':' in line.split(' ')[0] and not line.startswith('#'):
                                    rc_lines_list.append(line)

        # Extract the configuration names
        for line in rc_lines_list:
            # Configs will be in the form of 'command:config_name --arg(s)', this just extracts 'config_name'
            config_list.append(line.split(':')[1].split(' ')[0])

        # Convert to a dict and back to remove duplicates
        return(list(dict.fromkeys(config_list)))

    def get_compilation_mode_keyvalues():
        keys = ["compilation_mode"]
        values = ["fastbuild", "debug", "opt"]
        return (keys, values)

    def get_troubleshooting_keydict():
        return {
            "verbose_failures": "If a command fails, print out the full command line.",
            "subcommands": "Display the subcommands executed during a build.",
            "keep_going": "Build as much as possible even in the face of errors.",
        }

    def get_defines():
        print("Not yet")
