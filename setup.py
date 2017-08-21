#! /usr/bin/env python
"""Setup script for installing as a module."""
import re
import ast
import os

from setuptools import setup, find_packages


def read(*names):
    with open(os.path.join(os.path.dirname(__file__), *names)) as f:
        return f.read()


special_members = {}
for line in ast.parse(read("sx_saber", "__init__.py")).body:
    if (not isinstance(line, ast.Assign) or len(line.targets) != 1 or
            not isinstance(line.targets[0], ast.Name) or
            not re.match(r"__.*?__", line.targets[0].id) or
            not isinstance(line.value, ast.Str)):
        continue
    special_members[line.targets[0].id] = line.value.s

setup(
    # Metadata
    name=special_members["__pkg_name__"],
    version=special_members["__version__"],
    maintainer=special_members["__maintainer__"],
    maintainer_email=special_members["__maintainer_email__"],
    url=special_members["__git_url__"],
    description=special_members["__description__"],
    long_description=read('README.md') + '\n\n\n' + read('COPYRIGHT.txt'),
    license=special_members["__license__"],
    packages=find_packages(exclude=["tests", "docs"]),
    install_requires=[x.strip() for x in read("requirements.txt").splitlines()],
    tests_require=[x.strip() for x in read("test-requirements.txt").splitlines()],
    zip_safe=False
)
