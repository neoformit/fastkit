"""FastKit: routine pre-processing of FASTA/FASTQ files.

FastKit exposes multiple sub-commands for pre-processing biological sequence
files:

- Format: apply formatting to a file, with formatted content written to stdout
- Validate: run validation functions against a file

Type ``fastkit <subcommand> -h`` to get help for a specific subcommand.

"""

# Exposed modules must be imported here.
from . import format, validate
