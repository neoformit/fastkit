#!/usr/bin/env python3

"""Reformat FASTA files in preparation for tool execution.

Available filters:
- Strip spaces from FASTA headers
- Convert sequence characters to uppercase
- Create FASTA from headless sequence

**Escape Galaxy text input** - THIS IS LIKELY UNNECESSARY
  - see https://docs.galaxyproject.org/en/latest/dev/schema.html#id63

"""

import os
import sys
import argparse
from Bio import SeqIO

TEMP_SUFFIX = '.fktmp'
BULK_FILTERS = [
    # These are applied to the entire file before item filters and rely on
    # content being passed through a temporary file
    'headless',
]


def main():
    """Reformat file as specified.

    This is structured so that additional filters can easily be added in
    future. Files are processed on a per-sequence basis.

    To create a new filter, add a "parser.add_argument" line, an entry to
    FUNC_MAP and a function to handle the filtering.
    """
    args = parse_args()

    for f in BULK_FILTERS:
        if args.__dict__[f] not in (False, None):
            args.filename = FUNC_MAP[f](args.filename)

    with open(args.filename) as f:
        fas = SeqIO.parse(f, 'fasta')

        # Collect requested sequence filters from CLI args
        filters = {
            k: v
            for k, v in args.__dict__.items()
            if k != 'filename' and v and k not in BULK_FILTERS
        }

        # Pass each sequence through each filter function
        for seq in fas:
            for f in filters:
                seq = FUNC_MAP[f](seq)
            sys.stdout.write(seq.format('fasta'))

    # Remove temp file if exists
    if args.filename.endswith(TEMP_SUFFIX):
        os.remove(args.filename)


def parse_args():
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(
        prog="fastkit format",
        description=__doc__,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "filename",
        type=str,
        help="A filename to parse and correct.",
    )
    parser.add_argument(
        '--strip-header-space',
        action='store_true',
        help="Strip spaces from title and replace with underscore",
    )
    parser.add_argument(
        '--uppercase',
        action='store_true',
        help="Transform all sequence characters to uppercase",
    )
    parser.add_argument(
        '--headless',
        action='store_true',
        help="Create a single FASTA sequence from a headless FASTA file",
    )
    if __name__ == "__main__":
        # For running directly in dev
        return parser.parse_args()

    return parser.parse_args(sys.argv[2:])


# Item filters - applied to a single Bio.SeqIO record
# ------------------------------------------------------------------------------


def strip_header_space(seq):
    """Replace header spaces with underscores."""
    seq.id = seq.description.replace(' ', '_').replace('\t', '_')
    seq.name = ''
    seq.description = ''
    return seq


def uppercase(seq):
    """Transform sequence to uppercase characters."""
    seq.seq = seq.seq.upper()
    return seq


# Bulk filters - applied to text before parsing to FASTA
# ------------------------------------------------------------------------------

def headless(filename):
    """Create a legitimate FASTA file from a headless sequence."""
    temp = filename + TEMP_SUFFIX
    with open(filename) as f:
        with open(temp, 'w') as fw:
            fw.write('>unknown_sequence\n')
            while True:
                # Read 1MB at a time
                data = f.read(1048576)
                if not data:
                    break
                fw.write(data)
    if filename.endswith(TEMP_SUFFIX):
        os.rename(temp, filename)
        return filename

    return temp


# Map argparse option name to format functions
# The order that these are applied might need to be managed in future
FUNC_MAP = {
    'strip_header_space': strip_header_space,
    'uppercase': uppercase,
    'headless': headless,
}


if __name__ == '__main__':
    main()
