import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description="""Baz is a wrapper around Bazel that provides a GUI interface for \
setting build configuration options. If you need help with Bazel, run `bazel --help`.""", allow_abbrev=False)

    parser.add_argument(
        "-e", "--emit-build-script",
        action="store_true",
        default=False,
        help="""Emit a shell script to containing the raw Bazel build command, rather than executing it. This is
useful for exporting vanilla Bazel build commands to people who do not have baz.""",
    )
    parser.add_argument(
        "-p", "--print-build-settings",
        action="store_true",
        default=False,
        help="Prints the build settings configured for Baz.",
    )
    parser.add_argument(
        "-q", "--configure",
        action="store_true",
        default=False,
        help="Run the Baz configuration TUI."
    )
    parser.add_argument(
        "-d", "--delete-configuration",
        action="store_true",
        default=False,
        help="Permenently delete the persistent configuration file."
    )

    return parser.parse_known_args()
