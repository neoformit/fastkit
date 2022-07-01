#!/usr/bin/env python3

"""Reformat FASTA files in preparation for tool execution.

Available filters:
- Strip spaces from FASTA headers
- Convert sequence characters to uppercase

# TODO: filter escaped chars from Galaxy text input

"""

import sys
import argparse
from Bio import SeqIO

BULK_FILTERS = [
    'parse_galaxy_text',
]


def main():
    """Reformat file as specified.

    This is structured so that additional filters can easily be added in
    future. Files are processed on a per-sequence basis.

    To create a new filter, add a "parser.add_argument" line, an entry to
    FUNC_MAP and a function to handle the filtering.
    """
    args = parse_args()
    with open(args.filename) as f:
        fas = SeqIO.parse(f, 'fasta')
        filters = {
            k: v
            for k, v in args.__dict__.items()
            if k != 'filename' and v
        }
        for seq in fas:
            for f in filters:
                # Pass seq through formatting function
                seq = FUNC_MAP[f](seq)
            sys.stdout.write(seq.format('fasta'))


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
    # Probably unnecessary:
    # parser.add_argument(
    #     '--parse_galaxy_text',
    #     action='store_true',
    #     help=(
    #         "Parse escaped characters obtained from text inputs"
    #         " (e.g. newline -> __cn__)"
    #     ),
    # )
    parser.add_argument(
        '--uppercase',
        action='store_true',
        help="Transform all sequence characters to uppercase",
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

def parse_galaxy_text(text):
    """Restore characters that have been escaped by Galaxy.

    THIS MAY BE UNNECESSARY
    - see https://docs.galaxyproject.org/en/latest/dev/schema.html#id63

    """
    return text


# Map argparse option name to format functions
# The order that these are applied might need to be managed in future
FUNC_MAP = {
    'parse_galaxy_text': parse_galaxy_text,
    'strip_header_space': strip_header_space,
    'uppercase': uppercase,
}


if __name__ == '__main__':
    main()
