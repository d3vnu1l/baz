import sys
import os

import baz.bazel_helpers as bazel_helpers
import baz.filesystem as filesystem
from baz.baz_args import parse_arguments
from baz.constants import COMMANDS_TO_DECORATE, BAZ_PERSISTANT_DATA_FILE_LOCATION, BUILD_SCRIPT_TEMPLATE
from baz.tui import run_tui
from baz.inventory import BazConfigInventory


def get_arguments_from_inventory(inventory):
    baz_arguments = []
    if inventory is not None:
        # Compilation Modes
        baz_arguments.append('--compilation_mode=' + inventory.persistent_data["compilation_mode"])
        for key in inventory.config_keys:
            # Config keys
            if inventory.persistent_data[key] == True:
                baz_arguments.append('--config=' + key)
        for key in inventory.troubleshooting_keydict.keys():
            # Troubleshooting keys
            if inventory.persistent_data[key] == True:
                baz_arguments.append('--' + key)
        # Add user bazel flags
        if inventory.persistent_data['bazelopts'] != '':
            baz_arguments.append(inventory.persistent_data['bazelopts'])

    return baz_arguments

def run_baz():
    result = -1
    (args, extra_arguments) = parse_arguments()

    if args.configure:  # TUI
        inventory = BazConfigInventory()    # Gets or Creates inventory
        result = run_tui(inventory)
    elif args.delete_configuration:  # DELETE CONFIG
        if filesystem.delete_configuration():
            print("{} was deleted.".format(BAZ_PERSISTANT_DATA_FILE_LOCATION))
        else:
            print("No configuration found in: {}".format(BAZ_PERSISTANT_DATA_FILE_LOCATION))
    else:
        command_line = None

        # Only one supported request should be present, otherwise pass through to Bazel immediately
        supported_request = list(set(extra_arguments).intersection(COMMANDS_TO_DECORATE))
        if len(supported_request) == 1:
            inventory = BazConfigInventory()    # Gets or Creates inventory
            baz_arguments = get_arguments_from_inventory(inventory)
            tool = inventory.persistent_data['tool']

            # Form command
            command_line = bazel_helpers.form_command_line(
                tool,
                baz_arguments,
                extra_arguments,
            )
            if args.print_build_settings:   # PRINT
                inventory = BazConfigInventory()    # Gets or Creates inventory
                baz_arguments = get_arguments_from_inventory(inventory)
                print("Tool: {}".format(tool))
                print("Arguments: {}".format(baz_arguments))
            elif args.emit_build_script:    # EMIT
                script_path = os.path.join(os.getcwd(), "baz_command.sh")
                with open(script_path, "w") as script:
                    script.write(BUILD_SCRIPT_TEMPLATE.format(command=" ".join(str(item) for item in command_line)))
                    print("Wrote file: {}".format(script_path))

            else:
                # Execute real command
                print(command_line)
                result = bazel_helpers.execute_command(command_line, shell=True)

        else:
            # Pass through directly to tool
            command_line = ["bazel"] + extra_arguments
            result = bazel_helpers.execute_command(command_line)

    sys.exit(result)

if __name__ == "__main__":
    run_baz()

