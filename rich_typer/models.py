from __future__ import annotations

from typing import Any, Callable, Dict, Optional, Type, TYPE_CHECKING, Tuple

import click
from rich.console import JustifyMethod

from typer.models import (
    TyperInfo as _TyperInfo,
    CommandInfo as TyperCommandInfo,
    Default
)

if TYPE_CHECKING:
    from typer import Typer


class TyperInfo(_TyperInfo):
    def __init__(
        self,
        typer_instance: Optional["Typer"] = Default(None),
        *,
        name: Optional[str] = Default(None),
        cls: Optional[Type[click.Command]] = Default(None),
        invoke_without_command: bool = Default(False),
        no_args_is_help: bool = Default(False),
        subcommand_metavar: Optional[str] = Default(None),
        chain: bool = Default(False),
        result_callback: Optional[Callable[..., Any]] = Default(None),
        # Command
        context_settings: Optional[Dict[Any, Any]] = Default(None),
        callback: Optional[Callable[..., Any]] = Default(None),
        help: Optional[str] = Default(None),
        epilog: Optional[str] = Default(None),
        epilog_blend: Optional[Tuple[Tuple[int, int, int],
                                     Tuple[int, int, int]]] = Default(None),
        short_help: Optional[str] = Default(None),
        banner: Optional[str] = Default(None),
        banner_justify: Optional[JustifyMethod] = Default('default'),
        usage: Optional[str] = Default(None),
        options_metavar: str = Default("[OPTIONS]"),
        add_help_option: bool = Default(True),
        hidden: bool = Default(False),
        deprecated: bool = Default(False),
    ):
        self.typer_instance = typer_instance
        self.name = name
        self.cls = cls
        self.invoke_without_command = invoke_without_command
        self.no_args_is_help = no_args_is_help
        self.subcommand_metavar = subcommand_metavar
        self.chain = chain
        self.result_callback = result_callback
        self.context_settings = context_settings
        self.callback = callback
        self.help = help
        self.epilog = epilog
        self.epilog_blend = epilog_blend
        self.short_help = short_help
        self.banner = banner
        self.banner_justify = banner_justify
        self.usage = usage
        self.options_metavar = options_metavar
        self.add_help_option = add_help_option
        self.hidden = hidden
        self.deprecated = deprecated


class CommandInfo(TyperCommandInfo):
    def __init__(
        self,
        name: Optional[str] = None,
        *,
        cls: Optional[Type[click.Command]] = None,
        context_settings: Optional[Dict[Any, Any]] = None,
        callback: Optional[Callable[..., Any]] = None,
        help: Optional[str] = None,
        epilog: Optional[str] = None,
        epilog_blend: Optional[Tuple[Tuple[int, int, int],
                                     Tuple[int, int, int]]] = None,
        short_help: Optional[str] = None,
        banner: Optional[str] = None,
        banner_justify: Optional[JustifyMethod] = 'default',
        usage: Optional[str] = None,
        options_metavar: str = "[OPTIONS]",
        add_help_option: bool = True,
        no_args_is_help: bool = False,
        hidden: bool = False,
        deprecated: bool = False,
    ):
        self.name = name
        self.cls = cls
        self.context_settings = context_settings
        self.callback = callback
        self.help = help
        self.epilog = epilog
        self.epilog_blend = epilog_blend
        self.short_help = short_help
        self.banner = banner
        self.banner_justify = banner_justify
        self.usage = usage
        self.options_metavar = options_metavar
        self.add_help_option = add_help_option
        self.no_args_is_help = no_args_is_help
        self.hidden = hidden
        self.deprecated = deprecated
