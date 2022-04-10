# pystrgrep

grep/search for pattern in string constants contained in a python file

Searches through python files and extracts all string constants searching for pattern.

Optionally also searches through docstrings.

## Installation

`pipx install git+https://github.com/RhetTbull/pystrgrep.git`

## Usage

```
Usage: pystrgrep [OPTIONS] PATTERN FILE ...

  grep for PATTERN in python string constants inside FILE(s)

Arguments:
  PATTERN   [required]
  FILE ...  [required]

Options:
  -d, --docstring                 Search in docstrings
  -i, --ignore-case               Ignore case
  -n, --line-number               Show line numbers
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.
  ```