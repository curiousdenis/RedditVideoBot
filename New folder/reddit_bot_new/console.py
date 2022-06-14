from rich.console import Console
from rich.padding import Padding
from rich.text import Text
from rich.markdown import Markdown
from rich.panel import Panel
console = Console()
def print_markdown(text):
    """Prints a rich info message. Support Markdown syntax."""

    md = Padding(Markdown(text), 2)
    console.print(md)


def print_step(text, justify='left'):
    """Prints a rich info message."""

    panel = Panel(Text(text, justify))
    console.print(panel)


def print_substep(text, style=""):
    """Prints a rich info message without the panelling."""
    console.print(text, style=style)