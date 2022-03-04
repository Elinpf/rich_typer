from .core import RichTyper
import typer


app = RichTyper()
# app = typer.Typer()
banner = f"[b]Rich Typer[/b] [magenta]v0.1.0[/] 🤑\n\n[dim]将 Rich 与 Typer 结合起来，使界面更加漂亮。\n",

url = "♥ https://github.com/Elinpf/rich_typer\nLooking forward to your subscription!"


@app.command(epilog=url)
def main(
    name: str = typer.Argument(...,
                               help="Name of the [green]person to greet[/]."),
    message: str = typer.Option('ms', '-m', '--message',
                                help="The message [red]to[/] display"),
    version: bool = typer.Option(False, '-v', '--version',
                                 help="Show the [u]version[/] and exit"),
) -> None:
    """[bold][blue]Rich Typer[/] example."""
    ...


app()
