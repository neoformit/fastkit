#!/usr/bin/env python3

"""Validate FASTA files in preparation for tool execution.

These functions should not alter contents but only raise exceptions or return
boolean values to communicate validity of data.

Available validators:
- dna
- protein
- no-unknown
- sequence-count

"""

import sys
import argparse
from Bio import SeqIO
if __name__ == '__main__':
    from exceptions import ValidationError
else:
    from fastkit.exceptions import ValidationError


def main():
    """Validate file content."""
    # Get filters specified in CLI arguments
    args = parse_args()
    filters = {
        k: v for k, v in args.__dict__.items()
        if k != 'filename' and v not in (False, None)
    }
    try:
        seq = Fasta(args.filename, get_dtype(args))
        seq.validate(filters)
    finally:
        try:
            seq.close()
        except UnboundLocalError:
            pass
    sys.stderr.write("File content validated\n")


def get_dtype(args):
    """Return datatype specified by CLI arguments."""
    if args.dna:
        return 'dna'
    if args.protein:
        return 'protein'


def parse_args():
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(
        prog="fastkit validate",
        description=__doc__,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "filename",
        type=str,
        help="A filename to parse and correct.",
    )
    parser.add_argument(
        '--protein',
        action='store_true',
        help="Validate as IUPAC protein sequence",
    )
    parser.add_argument(
        '--dna',
        action='store_true',
        help="Validate as IUPAC DNA sequence",
    )
    parser.add_argument(
        '--no-unknown',
        action='store_true',
        help=(
            "Prohibit unknown IUPAC characters (X/N)"
            " - requires --dna or --protein"
        ),
    )
    parser.add_argument(
        '--sequence-count',
        type=int,
        help=(
            "[int] Maximum number of sequences that are permitted"
        ),
    )
    if __name__ == "__main__":
        # For running validate.py directly in dev
        return parser.parse_args()

    return parser.parse_args(sys.argv[2:])


class Fasta:
    """A sequence to be validated."""

    IUPAC = {
        'DNA': {
            'A', 'T', 'G', 'C', 'N',
        },
        'protein': {
            'A', 'B', 'C', 'D', 'E',
            'F', 'G', 'H', 'I', 'K',
            'L', 'M', 'N', 'P', 'Q',
            'R', 'S', 'T', 'U', 'V',
            'W', 'Y', 'Z', 'X',
        }
    }
    DNA_UNKNOWN = 'N'
    AA_UNKNOWN = 'X'

    def __init__(self, filename, dtype):
        """Read in sequence."""
        self.dtype = dtype
        self.ix = 0
        self.filename = filename
        self.file = open(filename)
        self.fas = SeqIO.parse(self.file, 'fasta')

    def close(self):
        """Close input file."""
        self.file.close()

    def validate(self, filters):
        """Validate file as specified.

        This is structured so that additional filters can easily be added in
        future. Files are processed on a per-sequence basis.

        To create a new filter, add a "parser.add_argument" line, an entry to
        FUNC_MAP and a function to handle the validation.
        """
        self.filters = filters
        for seq in self.fas:
            for f in filters:
                # Pass sequence through validator function
                getattr(self, f)(seq)

    def dna(self, seq):
        """Validate as IUPAC DNA sequence."""
        self._validate_iupac(seq, stype='DNA')

    def protein(self, seq):
        """Validate as IUPAC protein sequence."""
        self._validate_iupac(seq, stype='protein')

    def _validate_iupac(self, seq, stype='dna'):
        """Validate for IUPAC characters."""
        invalid = set(str(seq.seq).upper()) - self.IUPAC[stype]
        if invalid:
            pos = list(str(seq.seq)).index(list(invalid)[0])
            raise ValidationError(
                f'Sequence is not valid {stype}.'
                f' Invalid residue at position: {pos}.')

    def no_unknown(self, seq):
        """Validate characters not null."""
        if self.dtype == 'dna':
            if self.DNA_UNKNOWN in seq.seq:
                pos = list(str(seq.seq)).index(self.DNA_UNKNOWN)
                raise ValidationError(
                    f'Unknown DNA residues are not permitted.'
                    f' Invalid residue at position: {pos}.')
        elif self.dtype == 'protein':
            if self.AA_UNKNOWN in seq.seq:
                pos = list(str(seq.seq)).index(self.AA_UNKNOWN)
                raise ValidationError(
                    f'Unknown amino acid residues are not permitted.'
                    f' Invalid residue at position: {pos}.')
        else:
            sys.stderr.write(
                "WARNING: cannot validate not-null if no sequence type"
                " inferred (requires --dna or --protein flag).")

    def sequence_count(self, seq):
        """Assert number of sequences submitted is less than max allowed."""
        self.ix += 1
        sequence_count = self.filters['sequence_count']
        if self.ix <= sequence_count:
            return
        with open(self.filename) as f:
            count = len([0 for i in SeqIO.parse(f, 'fasta')])
        raise ValidationError(
            f"A maximum of {sequence_count} sequences is"
            f" permitted ({count} sequences were read from the input file).")


if __name__ == '__main__':
    main()
