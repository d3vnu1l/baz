import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="baz-pkg-d3vnu1l",
    version="0.1.0",
    author="Ryan Deushane",
    author_email="radeushane@gmail.com",
    description="A curses GUI for Bazel",
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
)
