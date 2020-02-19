# Baz
A wrapper for bazel with a GUI for configuring arguments. Running `baz -q` opens a configuration gui where you can set persistent bazel settings by choosing from detected `.bazelrc` configs, and other bazel flags.

![image](https://i.imgur.com/g0eoEIt.png)

Baz stores persistent information in `~/.config/baz/`. You can delete your configuration and start over at any time with `baz -d`.

Add baz to your path and use baz as you would use bazel.

## Installation
### Pypi
```
python3 -m pip install baz --user
```
If you haven't already, make sure scripts from your user site are accesible from PATH.
```
import site
site.USER_BASE # Prints something like `/home/username/.local/`
```
Take this path, and add to your `~/.bashrc` as: `export PATH='$PATH:/home/username/.local/bin/`

## Usage
baz --help
```
usage: baz.py [-h] [-e] [-p] [-q] [-d]

optional arguments:
  -h, --help            show this help message and exit
  -e, --emit-build-script
                        Emit a shell script to containing the raw Bazel build command, rather than executing it. This is useful for exporting vanilla Bazel build commands to people who do not have baz.
  -p, --print-build-settings
                        Prints the build settings configured for Baz.
  -q, --configure       Run the Baz configuration TUI.
  -d, --delete-configuration
                        Permenently delete the persistent configuration file.
```
## Testing
Unit tests can be run with `nosetests`.
