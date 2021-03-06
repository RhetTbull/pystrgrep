# pystrgrep

grep/search for pattern in string constants contained in a python file

Searches through python files and extracts all string constants searching for pattern.

Optionally also searches through docstrings.

## Installation

Use [pipx](https://pypa.github.io/pipx/):

`pipx install git+https://github.com/RhetTbull/pystrgrep.git`

## Example

![Example image](https://raw.githubusercontent.com/RhetTbull/pystrgrep/main/docs/images/example1.png)

## Usage

```
Usage: pystrgrep [OPTIONS] PATTERN FILE ...

  grep for PATTERN in python string constants inside FILE(s)

Arguments:
  PATTERN   [required]
  FILE ...  [required]

Options:
  --version
  -i, --ignore-case               Ignore case
  -n, --line-number               Show line numbers
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.
```
