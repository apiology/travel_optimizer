#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages
import distutils
from distutils.cmd import Command
import distutils.command.clean
from distutils.dir_util import remove_tree
import subprocess
import os
from typing import List, Tuple, Optional

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements: List[str] = ['Click>=6.0']

setup_requirements: List[str] = []

test_requirements: List[str] = []


class MypyCleanCommand(Command):
    """Regular clean plus mypy cache"""

    description = 'Run mypy on source code'
    user_options: List[Tuple[str, Optional[str], str]] = []

    def initialize_options(self) -> None:
        pass

    def finalize_options(self) -> None:
        pass

    def run(self) -> None:
        if os.path.exists('.mypy_cache'):
            remove_tree('.mypy_cache')


class MypyCommand(Command):
    description = 'Run mypy on source code'
    user_options: List[Tuple[str, Optional[str], str]] = []

    def initialize_options(self) -> None:
        pass

    def finalize_options(self) -> None:
        pass

    def run(self) -> None:
        """Run command."""
        command = ['mypy', '--html-report', 'types/coverage', '.']
        self.announce(
            'Running command: %s' % str(command),
            level=distutils.log.INFO)  # type: ignore
        subprocess.check_call(command)


class QualityCommand(Command):
    quality_target: Optional[str]

    description = 'Run quality gem on source code'
    user_options = [
        # The format is (long option, short option, description).
        ('quality-target=',
         None,
         'particular quality tool to run (default: all)')
    ]

    def initialize_options(self) -> None:
        """Set default values for options."""
        # Each user option must be listed here with their default value.
        self.quality_target = None

    def finalize_options(self) -> None:
        pass

    def run(self) -> None:
        """Run command."""
        command = ['./quality.sh']
        if self.quality_target:
            command.append(self.quality_target)
        self.announce(
            'Running command: %s' % str(command),
            level=distutils.log.INFO)  # type: ignore
        subprocess.check_call(command)


setup(
    author="Vince Broz",
    author_email='vince@broz.cc',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Finds cheap travel fares",
    entry_points={
        'console_scripts': [
            'travel_optimizer=travel_optimizer.cli:main',
        ],
    },
    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='travel_optimizer',
    name='travel_optimizer',
    packages=find_packages(include=['travel_optimizer']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/apiology/travel_optimizer',
    version='0.1.0',
    zip_safe=False,
    cmdclass={
        'quality': QualityCommand,
        'typesclean': MypyCleanCommand,
        'types': MypyCommand,
    },
)
