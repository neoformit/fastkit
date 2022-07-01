"""CLI interface for fastkit functions."""

import sys
import fastkit

SUBCOMMANDS = [
    'format',
]


def main():
    """Execute from command line."""
    module = get_module()
    if module:
        module.main()


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
