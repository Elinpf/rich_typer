from typing import Any, Callable, Dict, Optional, Type

import click
import typer
from typer.models import CommandFunctionType

from .core import RichCommand
from .models import CommandInfo


class RichTyper(typer.Typer):
    def command(
        self,
        name: Optional[str] = None,
        *,
        cls: Optional[Type[click.Command]] = None,
        context_settings: Optional[Dict[Any, Any]] = None,
        help: Optional[str] = None,
        epilog: Optional[str] = None,
        short_help: Optional[str] = None,
        options_metavar: str = "[OPTIONS]",
        add_help_option: bool = True,
        no_args_is_help: bool = False,
        hidden: bool = False,
        deprecated: bool = False,
    ) -> Callable[[CommandFunctionType], CommandFunctionType]:
        if cls is None:
            cls = RichCommand

        def decorator(f: CommandFunctionType) -> CommandFunctionType:
            self.registered_commands.append(
                CommandInfo(
                    name=name,
                    cls=cls,
                    context_settings=context_settings,
                    callback=f,
                    help=help,
                    epilog=epilog,
                    short_help=short_help,
                    options_metavar=options_metavar,
                    add_help_option=add_help_option,
                    no_args_is_help=no_args_is_help,
                    hidden=hidden,
                    deprecated=deprecated,
                )
            )
            return f

        return decorator
