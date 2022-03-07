from __future__ import annotations

from typing import Type

import click
from click.core import Context
from typer.core import TyperCommand

from .formatting import HelpFormatter


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
