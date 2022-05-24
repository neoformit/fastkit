#!/usr/bin/env python3

"""Setup packages."""

from distutils.core import setup

PACKAGES = [
    'fastkit',
]

with open('requirements.txt') as f:
    REQUIREMENTS = [
        x.strip(' \n')
        for x in f
    ]

setup(
    name='fastkit',
    version='0.1.0',
    description='Biological data preprocessing facility',
    author='Cameron Hyde',
    author_email='chyde@neoformit.com',
    url='https://github.com/neoformit/fastkit',
    packages=PACKAGES,
    install_requires=REQUIREMENTS,
    entry_points={
        'console_scripts': ['fastkit=fastkit.cli:main'],
    }
)
