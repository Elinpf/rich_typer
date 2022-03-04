from __future__ import annotations

from typing import Any, Callable, Dict, Optional, Type

import click
import typer
from click.core import Context
from typer.core import TyperCommand
from typer.models import CommandFunctionType

from .formatting import HelpFormatter
from .models import CommandInfo


class RichContext(click.core.Context):
    formatter_class: Type["HelpFormatter"] = HelpFormatter


class RichCommand(TyperCommand):
    context_class: Type["Context"] = RichContext

    def format_help(self, ctx: "Context", formatter: HelpFormatter) -> None:
        self.format_banner(ctx, formatter)
        self.format_usage(ctx, formatter)
        self.format_help_text(ctx, formatter)
        self.format_options(ctx, formatter)
        self.format_epilog(ctx, formatter)

    def format_banner(self, ctx: "Context", formatter: HelpFormatter) -> None:
        ...

    def format_options(self, ctx: "Context", formatter: HelpFormatter) -> None:
        args = []
        opts = []
        for param in self.get_params(ctx):
            rv = param.get_help_record(ctx)
            if rv is not None:
                if param.param_type_name == "argument":
                    args.append(rv)
                elif param.param_type_name == "option":
                    opts.append(rv)

        if args:
            with formatter.section("Arguments") as table:
                formatter.add_params(args, table)
        if opts:
            with formatter.section("Options") as table:
                formatter.add_params(opts, table)

    def format_epilog(self, ctx: "Context", formatter: HelpFormatter) -> None:
        if self.epilog:
            formatter.write_epilog(self.epilog)


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
