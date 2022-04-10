"""grep/search for pattern in python strings

Searches through python files and extracts all string constants searching for pattern.

Optionally also searches through docstrings.
"""

import ast
import re
from pathlib import Path
from typing import List, Optional

import rich.console
import typer

from ._version import __version__


def get_str_value(node: ast.AST, docstring: bool) -> str:
    """Return string value of ast node if it is a string constant or docstring

    Args:
        node: ast node
        docstring: search in docstrings
    """
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    elif docstring and isinstance(node, ast.FunctionDef):
        return ast.get_docstring(node) or ""
    else:
        return None


def print_match(
    filename: str,
    node: ast.AST,
    line: str,
    line_number: bool,
    pattern: str,
    ignore_case: bool,
):
    filename_str = f"{filename}:{node.lineno}:" if line_number else f"{filename}:"
    line = line[:-1] if line.endswith("\n") else line
    line_pre = line[: node.col_offset]
    line_value = line[node.col_offset : node.end_col_offset]
    line_post = line[node.end_col_offset :]
    flags = re.IGNORECASE if ignore_case else 0
    regex = re.compile(f"({pattern})", flags=flags)
    line_pre = escape_brackets(line_pre)
    line_value = escape_brackets(line_value)
    line_post = escape_brackets(line_post)
    line_value = regex.sub(r"[bold red]\1[/]", line_value)
    console = rich.console.Console(highlight=False)
    console.print(f"{filename_str}{line_pre}{line_value}{line_post}")


def escape_brackets(value: str) -> str:
    """Escape opening brackets in value for use with rich print"""
    return value.replace("[", r"\[")


def version_callback(value: bool):
    if value:
        typer.echo(f"pystrgrep: {__version__}")
        raise typer.Exit()


def grep(
    version: Optional[bool] = typer.Option(
        None, "--version", callback=version_callback, is_eager=True
    ),
    docstring: bool = typer.Option(
        False, "--docstring", "-d", is_flag=True, help="Search in docstrings"
    ),
    ignore_case: bool = typer.Option(
        False, "--ignore-case", "-i", is_flag=True, help="Ignore case"
    ),
    line_number: bool = typer.Option(
        False, "--line-number", "-n", is_flag=True, help="Show line numbers"
    ),
    pattern: str = typer.Argument(..., metavar="PATTERN"),
    files: List[Path] = typer.Argument(
        ...,
        metavar="FILE ...",
        exists=True,
        file_okay=True,
        dir_okay=False,
    ),
):
    """grep for PATTERN in python string constants inside FILE(s)"""
    for f in files:
        with open(f, "r") as fh:
            lines = fh.readlines()
        contents = "".join(lines)

        for node in ast.walk(ast.parse(contents)):
            if value := get_str_value(node, docstring):
                if re.search(
                    pattern,
                    value,
                    flags=re.IGNORECASE if ignore_case else 0,
                ):
                    print_match(
                        f,
                        node,
                        lines[node.lineno - 1],
                        line_number,
                        pattern,
                        ignore_case,
                    )


def main():
    typer.run(grep)


if __name__ == "__main__":
    main()
