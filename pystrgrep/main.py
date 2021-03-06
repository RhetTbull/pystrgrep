"""grep/search for pattern in python strings

Searches through python files and extracts all string constants searching for pattern.
"""

import ast
import re
from pathlib import Path
from typing import List, Optional

import rich.traceback
import typer
from rich.console import Console
from rich.text import Text
from rich.table import Table

from ._version import __version__

rich.traceback.install()

HIGHLIGHT_STYLE = "bold red"

app = typer.Typer()


def get_str_value(node: ast.AST) -> str:
    """Return string value of ast node if it is a string constant, otherwise None

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

    # print the entire line, breaking it into three parts:
    # line_pre (before the node), line_value (the node), and line_post (after the node)
    line_pre = line[: node.col_offset]
    line_post = line[node.end_col_offset :]
    line_pre = Text(escape_brackets(line_pre), style="")
    line_post = Text(escape_brackets(line_post), style="")

    # build up the value to print while escaping brackets (for rich)
    # and highlighting the match
    line_value = line[node.col_offset : node.end_col_offset]

    # find all matches in the line_value
    flags = re.IGNORECASE if ignore_case else 0
    match_spans = [
        match.span() for match in re.finditer(pattern, line_value, flags=flags)
    ]
    new_line_values = []
    last_end = 0
    for start, end in match_spans:
        new_line_values.extend(
            (
                Text(escape_brackets(line_value[last_end:start]), style=""),
                Text(escape_brackets(line_value[start:end]), style=HIGHLIGHT_STYLE),
            )
        )
        last_end = end
    if last_end != len(line_value):
        new_line_values.append(Text(escape_brackets(line_value[last_end:]), style=""))

    table = Table("", box=None, padding=(0, 0), show_header=False)
    table.add_row(filename_str, line_pre, *new_line_values, line_post)
    console = Console(highlight=False, emoji=False)
    console.print(table)


def escape_brackets(value: str) -> str:
    """Escape opening brackets in value for use with rich print"""
    return value.replace("[", r"\[")


def version_callback(value: bool):
    """Print version and exit"""
    if value:
        typer.echo(f"pystrgrep: {__version__}")
        raise typer.Exit()


@app.command()
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
    flags = re.IGNORECASE if ignore_case else 0
    try:
        regex = re.compile(pattern, flags=flags)
    except re.error as e:
        typer.secho(
            f"Invalid regular expression: '{pattern}' ({e})", fg=typer.colors.RED
        )
        raise typer.Exit(1) from e

    for f in files:
        with open(f, "r") as fh:
            lines = fh.readlines()
        contents = "".join(lines)

        for node in ast.walk(ast.parse(contents)):
            if value := get_str_value(node):
                if regex.search(value):
                    print_match(
                        f,
                        node,
                        lines[node.lineno - 1],
                        line_number,
                        pattern,
                        ignore_case,
                    )
