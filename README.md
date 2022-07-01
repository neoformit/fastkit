# FastKit

Fastkit is primarily written to perform routine/repetitive operations on
FASTA and FASTQ files, most notably formatting. Its purpose is
pre-processing of files for use in other bioinformatics tools.

- FastKit seeks to wrap established libraries (such as Biopython,
  SeqTK, FASTX-toolkit, etc) rather than re-invent the wheel!
- Write output to `stdout` so that the consumer can control file names
  transparently and pipe between fastkit subcommands to the target tool/file.
- Each subcommand should infer datatypes from filenames and process
  accordingly, rather than having a tool for each datatype.

---

**Example usage**

```sh
fastkit format input.raw.fasta --strip-header-space > input.fasta
```

**Running tests**
```sh
python -m unittest tests/*.py
```

---

## Available datatypes
- FASTA

## Available subcommands
- `format`
- `validate`


### Format

```
usage: fastkit format [-h] [--strip-header-space] [--uppercase] filename

Reformat FASTA files in preparation for tool execution.

Available filters:
- Strip spaces from FASTA headers
- Convert sequence characters to uppercase

# TODO: filter escaped chars from Galaxy text input

positional arguments:
  filename              A filename to parse and correct.

options:
  -h, --help            show this help message and exit
  --strip-header-space  Strip spaces from title and replace with underscore
  --uppercase           Transform all sequence characters to uppercase
```


### Validate

```
usage: fastkit validate [-h] [--protein] [--dna] [--no-unknown] [--sequence-count SEQUENCE_COUNT] filename

Validate FASTA files in preparation for tool execution.

These functions should not alter contents but only raise exceptions or return
boolean values to communicate validity of data.

Available validators:
- dna
- protein
- no-unknown
- sequence-count

positional arguments:
  filename              A filename to parse and correct.

options:
  -h, --help            show this help message and exit
  --protein             Validate as IUPAC protein sequence
  --dna                 Validate as IUPAC DNA sequence
  --no-unknown          Prohibit unknown IUPAC characters (X/N) - requires --dna or --protein
  --sequence-count SEQUENCE_COUNT
                        [int] Maximum number of sequences that are permitted
```


---

## Adding a subcommand

- Create new function(s) in `fastkit/<new_command>.py`
- `<new_command>.py` must have a `main` callable - use `format.py` as an example
- Import `new_command` in `fastkit.__init__.py`
- Add `new_command` to `fastkit.cli.SUBCOMMANDS`


## Testing in development

Run a script directly using the `if __name__ == 'main'` clause:

```sh
python fastkit/format.py --strip-header-space test/data/spaces.fas
```

`conda-build` will package the above to run as:

```sh
fastkit filter --strip-header-space test/data/spaces.fas
```

## Pushing changes to bioconda

- Publish a new release on GitHub
- Fork `bioconda/bioconda-recipes` and make a branch for the new version
- Update the version and sha256 in `recipes/fastkit/meta.yaml` to match the new release
- Commit, push and make a pull request to `bioconda/bioconda-recipes`
- Wait for it to be merged (you may need to ask bioconda-bot to add a label once it's been approved)
