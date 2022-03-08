from __future__ import annotations

from typing import Type

import click
from click.core import Context
from typer.core import TyperCommand, TyperGroup

from .formatting import HelpFormatter


def _rich_typer_format_banner(
    self: click.core.Command,
    ctx: Context,
    formatter: HelpFormatter
) -> None:
    ...


def _rich_typer_format_options(
    self: click.core.Command,
    ctx: Context,
    formatter: HelpFormatter
) -> None:
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
        _rich_typer_format_banner(self, ctx=ctx, formatter=formatter)

    def format_options(self, ctx: "Context", formatter: HelpFormatter) -> None:
        _rich_typer_format_options(self, ctx=ctx, formatter=formatter)

    def format_epilog(self, ctx: "Context", formatter: HelpFormatter) -> None:
        if self.epilog:
            formatter.write_epilog(self.epilog)


class RichGroup(TyperGroup):
    context_class: Type["Context"] = RichContext

    def format_help(self, ctx: "Context", formatter: HelpFormatter) -> None:
        self.format_banner(ctx, formatter)
        self.format_usage(ctx, formatter)
        self.format_help_text(ctx, formatter)
        self.format_options(ctx, formatter)
        self.format_epilog(ctx, formatter)

    def format_banner(self, ctx: "Context", formatter: HelpFormatter) -> None:
        _rich_typer_format_banner(self, ctx, formatter)

    def format_commands(self, ctx: Context, formatter: HelpFormatter) -> None:
        """Extra format methods for multi methods that adds all the commands
        after the options.
        """
        commands = []
        for subcommand in self.list_commands(ctx):
            cmd = self.get_command(ctx, subcommand)
            # What is this, the tool lied about a command.  Ignore it
            if cmd is None:
                continue
            if cmd.hidden:
                continue

            commands.append((subcommand, cmd))

        # allow for 3 times the default spacing
        if len(commands):
            limit = formatter.width - 6 - max(len(cmd[0]) for cmd in commands)

            rows = []
            for subcommand, cmd in commands:
                help = cmd.get_short_help_str(limit)
                rows.append((subcommand, help))

            if rows:
                with formatter.section("Commands") as table:
                    formatter.add_params(rows, table)

    def format_options(self, ctx: "Context", formatter: HelpFormatter) -> None:
        _rich_typer_format_options(self, ctx=ctx, formatter=formatter)
        self.format_commands(ctx, formatter)

    def format_epilog(self, ctx: "Context", formatter: HelpFormatter) -> None:
        if self.epilog:
            formatter.write_epilog(self.epilog)
