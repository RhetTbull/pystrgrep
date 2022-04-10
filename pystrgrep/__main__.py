"""grep/search for pattern in python strings

Searches through python files and extracts all string constants searching for pattern.
"""

import ast
import re
from pathlib import Path
from typing import List, Optional

from rich.console import Console
from rich.text import Text
import typer

from ._version import __version__


def get_str_value(node: ast.AST) -> str:
    """Return string value of ast node if it is a string constant

    Args:
        node: ast node
    """
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
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
    """Print match from grep"""
    filename_str = f"{filename}:{node.lineno}:" if line_number else f"{filename}:"
    line = line[:-1] if line.endswith("\n") else line

    line_pre = line[: node.col_offset]
    line_post = line[node.end_col_offset :]
    line_pre = escape_brackets(line_pre)
    line_post = escape_brackets(line_post)

    flags = re.IGNORECASE if ignore_case else 0
    line_value = line[node.col_offset : node.end_col_offset]
    line_values = re.split(pattern, line_value, flags=flags)
    line_values = [escape_brackets(v) for v in line_values]
    line_value = f"[bold red]{pattern}[/]".join(line_values)

    console = Console(highlight=False)
    console.print(f"{filename_str}{line_pre}{line_value}{line_post}")


def escape_brackets(value: str) -> str:
    """Escape opening brackets in value for use with rich print"""
    return value.replace("[", r"\[")


def version_callback(value: bool):
    """Print version and exit"""
    if value:
        typer.echo(f"pystrgrep: {__version__}")
        raise typer.Exit()


def grep(
    version: Optional[bool] = typer.Option(
        None, "--version", callback=version_callback, is_eager=True
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

    pattern = pattern.replace("\\\\", "\\")
    for f in files:
        with open(f, "r") as fh:
            lines = fh.readlines()
        contents = "".join(lines)

        for node in ast.walk(ast.parse(contents)):
            if value := get_str_value(node):
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
