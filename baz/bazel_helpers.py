import subprocess
import os


def parse_bazel_arguments(extra_arguments, verbose=False):
    pre_arguments = []
    targets = []
    post_arguments = []
    request_type = None

    for argument in extra_arguments:
        # Bazel allows pre-arguments, so we must find the first argument that doesn't begin with `-`
        if argument.startswith('-'):
            if request_type is None:
                pre_arguments.append(argument)
            else:
                post_arguments.append(argument)
        elif argument.startswith(('//', ':')):
            targets.append(argument)
        elif request_type is None:
            request_type = argument
        elif post_arguments is not None:  # Catch --define asdf=asdf in post arguments
            post_arguments.append(argument)
        else:
            raise Exception('Could not process argument: {}'.format(argument))

    if verbose:
        print("Request_type = {}".format(request_type))
        print("Targets = {}".format(targets))
        print("Pre_arguments = {}".format(pre_arguments))
        print("Post_arguments = {}".format(post_arguments))

    return (request_type, pre_arguments, targets, post_arguments)


def form_command_line(tool, baz_arguments, extra_arguments):
    (request_type, pre_arguments, targets, post_arguments) = parse_bazel_arguments(extra_arguments)
    return [tool] + pre_arguments + [request_type] + targets + baz_arguments + ["--tool_tag=baz"] + post_arguments


def execute_command(command_line, shell=False):
    result = -1
    try:
        if shell:
            command = [os.environ["SHELL"], "-i", "-c"] + [" ".join(command_line)]
            result = subprocess.run(command, check=True).returncode
        else:
            result = subprocess.run(command_line, check=True).returncode
    except subprocess.CalledProcessError as status:
        result = status.returncode
    except KeyboardInterrupt:
        pass    # Gracefully allow the user to cancel the build

    return result
