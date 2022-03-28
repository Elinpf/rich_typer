from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional, Type, Union, Sequence, Tuple

import click
from click.core import Context, Parameter
from typer.core import TyperCommand, TyperGroup

from .formatting import RichHelpFormatter


def _rich_typer_format_banner(
    self: click.core.Command,
    ctx: Context,
    formatter: RichHelpFormatter
) -> None:
    if self.banner:
        formatter.write_banner(self.banner, self.banner_justify)


def _rich_typer_format_options(
    self: click.core.Command,
    ctx: Context,
    formatter: RichHelpFormatter
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
    formatter_class: Type["RichHelpFormatter"] = RichHelpFormatter


class RichCommand(TyperCommand):
    context_class: Type["Context"] = RichContext

    def __init__(
        self,
        name: Optional[str],
        context_settings: Optional[Dict[str, Any]] = None,
        callback: Optional[Callable[..., Any]] = None,
        params: Optional[List["Parameter"]] = None,
        help: Optional[str] = None,
        epilog: Optional[str] = None,
        epilog_blend: Optional[Tuple[Tuple[int, int, int],
                                     Tuple[int, int, int]]] = None,
        short_help: Optional[str] = None,
        banner: Optional[str] = None,
        banner_justify: Optional[str] = 'default',
        usage: Optional[str] = None,
        options_metavar: Optional[str] = "[OPTIONS]",
        add_help_option: bool = True,
        no_args_is_help: bool = False,
        hidden: bool = False,
        deprecated: bool = False,
    ) -> None:
        self.banner = banner
        self.banner_justify = banner_justify
        self.epilog_blend = epilog_blend
        self.usage = usage
        super().__init__(
            name=name,
            context_settings=context_settings,
            callback=callback,
            params=params,
            help=help,
            epilog=epilog,
            short_help=short_help,
            options_metavar=options_metavar,
            add_help_option=add_help_option,
            no_args_is_help=no_args_is_help,
            hidden=hidden,
            deprecated=deprecated
        )

    def format_help(self, ctx: "Context", formatter: RichHelpFormatter) -> None:
        self.format_banner(ctx, formatter)
        self.format_usage(ctx, formatter)
        self.format_help_text(ctx, formatter)
        self.format_options(ctx, formatter)
        self.format_epilog(ctx, formatter)

    def format_banner(self, ctx: "Context", formatter: RichHelpFormatter) -> None:
        _rich_typer_format_banner(self, ctx=ctx, formatter=formatter)

    def format_usage(self, ctx: "Context", formatter: RichHelpFormatter) -> None:
        if self.usage:
            formatter.write(self.usage)
            formatter.write("\n")
        else:
            super().format_usage(ctx, formatter)

    def format_options(self, ctx: "Context", formatter: RichHelpFormatter) -> None:
        _rich_typer_format_options(self, ctx=ctx, formatter=formatter)

    def format_epilog(self, ctx: "Context", formatter: RichHelpFormatter) -> None:
        if self.epilog:
            formatter.write_epilog(self.epilog, self.epilog_blend)


class RichGroup(TyperGroup):
    context_class: Type["Context"] = RichContext

    def __init__(
        self,
        name: Optional[str] = None,
        commands: Optional[Union[Dict[str, RichCommand],
                                 Sequence[RichCommand]]] = None,
        **attrs: Any,
    ) -> None:
        self.banner = attrs.pop("banner", None)
        self.banner_justify = attrs.pop("banner_justify", "default")
        self.epilog_blend = attrs.pop("epilog_blend", None)
        self.usage = attrs.pop("usage", None)
        super().__init__(name=name, commands=commands, **attrs)

    def format_help(self, ctx: "Context", formatter: RichHelpFormatter) -> None:
        self.format_banner(ctx, formatter)
        self.format_usage(ctx, formatter)
        self.format_help_text(ctx, formatter)
        self.format_options(ctx, formatter)
        self.format_epilog(ctx, formatter)

    def format_banner(self, ctx: "Context", formatter: RichHelpFormatter) -> None:
        _rich_typer_format_banner(self, ctx, formatter)

    def format_usage(self, ctx: "Context", formatter: RichHelpFormatter) -> None:
        if self.usage:
            formatter.write(self.usage)
            formatter.write("\n")
        else:
            super().format_usage(ctx, formatter)

    def format_commands(self, ctx: Context, formatter: RichHelpFormatter) -> None:
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

    def format_options(self, ctx: "Context", formatter: RichHelpFormatter) -> None:
        _rich_typer_format_options(self, ctx=ctx, formatter=formatter)
        self.format_commands(ctx, formatter)

    def format_epilog(self, ctx: "Context", formatter: RichHelpFormatter) -> None:
        if self.epilog:
            formatter.write_epilog(self.epilog, self.epilog_blend)
