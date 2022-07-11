#!/usr/bin/env python3

"""CLI interface for fastkit functions."""

import sys
import fastkit
import argparse

SUBCOMMANDS = [
    'format',
    'validate',
]

VERSION = '1.0.2'


def main():
    """Execute from command line."""
    if root_entry():
        return
    module = get_module()
    if module:
        try:
            module.main()
        except Exception as exc:
            # Print err message before traceback for more readable
            # Galaxy history output
            sys.stderr.write(exc.__class__.__name__ + ': ')
            sys.stderr.write(str(exc) + '\n\n')
            raise exc


def root_entry():
    """If args passed directly, run fastkit root entrypoint.

    Only useful for help and version flags.
    """
    if len(sys.argv) > 1 and sys.argv[1].startswith('-'):
        parse_args()
        return True


def parse_args():
    """Return CLI arguments."""
    parser = argparse.ArgumentParser(
        prog="fastkit",
        description=fastkit.__doc__,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        '--version',
        action='version',
        version=f"FastKit v{VERSION}",
    )
    return parser.parse_args()


def get_module():
    """Parse CLI arguments and return requested module."""
    if len(sys.argv) > 1:
        m = sys.argv[1]
        if m in SUBCOMMANDS:
            return getattr(fastkit, m, None)
        else:
            print(f"Invalid subcommand: {sys.argv[1]}")

    print('Please specify a FastKit subcommand:')
    print('\n'.join([
        f'  - {x}'
        for x in SUBCOMMANDS
    ]))


if __name__ == '__main__':
    main()
