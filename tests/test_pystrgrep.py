"""Test pystrgrep """

from pystrgrep import __version__
from pystrgrep.__main__ import app
from typer.testing import CliRunner

runner = CliRunner()


def test_version():
    """Test --version"""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert result.output == f"pystrgrep: {__version__}" + "\n"
