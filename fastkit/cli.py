#!/usr/bin/env python3

"""CLI interface for fastkit functions."""

import sys
import fastkit

SUBCOMMANDS = [
    'format',
    'validate',
]


def main():
    """Execute from command line."""
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
