import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="baz",
    version="0.2.2",
    author="Ryan Deushane",
    author_email="radeushane@gmail.com",
    description="A wrapper for the Bazel build system that provides a curses GUI for persistent configuration.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/d3vnu1l/baz",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    install_requires=[
        'asciimatics>=1.11.0',
        'dataclasses>=0.6',
    ],
    scripts=['bin/baz'],
)
