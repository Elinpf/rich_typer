from __future__ import annotations

from typing import Any, Callable, Dict, Optional, Type

import click
from typer.models import CommandInfo as TyperCommandInfo


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
        short_help: Optional[str] = None,
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
        self.short_help = short_help
        self.options_metavar = options_metavar
        self.add_help_option = add_help_option
        self.no_args_is_help = no_args_is_help
        self.hidden = hidden
        self.deprecated = deprecated
