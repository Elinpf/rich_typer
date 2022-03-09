from .main import RichTyper
from . import Argument, Option, __version__


app = RichTyper()
banner = f"[b]Rich Typer[/b] [magenta]v{__version__}[/] 🤑\n\n[dim]将 Rich 与 Typer 结合起来，使界面更加漂亮。\n"

url = "♥ https://github.com/Elinpf/rich_typer"


@app.command(banner=banner, banner_justify='center', epilog=url)
def main(
    name: str = Argument(...,
                         help="Name of the [green]person to greet[/]."),
    message: str = Option('ms', '-m', '--message',
                                help="The message [red]to[/] display"),
    version: bool = Option(False, '-v', '--version',
                           help="Show the [u]version[/] and exit"),
) -> None:
    """[bold][blue]Rich Typer[/] example."""
    ...


app()
