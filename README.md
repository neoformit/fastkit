# FastKit

Fastkit is primarily written to perform routine/repetitive operations on
FASTA and FASTQ files, most notably formatting. Its purpose is
pre-processing of files for use in other bioinformatics tools.

- FastKit should seek to wrap established libraries (such as Biopython,
  SeqTK, FASTX-toolkit, etc) rather than re-invent the wheel!
- Write output to `stdout` so that the consumer can control file names
  transparently and pipe from one subcommand to the next.
- Each subcommand should infer datatypes from filenames and process
  accordingly, rather than having a tool for each datatype.

---

**Example usage**

```sh
fastkit format input.raw.fasta --strip-header-space > input.fasta
```

---

## Available datatypes
- FASTA

## Available subcommands
- `format`


### Format

```
usage: fastkit format [-h] [--strip-header-space] filename

Reformat FASTA files in preparation for tool execution.

Available filters:
- Strip spaces from headers

positional arguments:
  filename              A filename to parse and correct.

options:
  -h, --help            show this help message and exit
  --strip-header-space  Strip spaces from title and replace with underscore
```


---

## Adding a subcommand

- Create new function(s) in `fastkit/<new_command>.py`
- Import `new_command` in `fastkit.__init__.py`
- Add `new_command` to `fastkit.cli.SUBCOMMANDS` (must have a `main` callable)
