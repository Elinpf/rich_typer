from __future__ import annotations

import re
from contextlib import contextmanager
from typing import Iterator, List, Optional, Tuple, Dict

from click import HelpFormatter as ClickHelpFormatter
from rich.console import Console, JustifyMethod
from rich.highlighter import RegexHighlighter
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.theme import Theme

from .utils import blend_text


class HelpFormatter(ClickHelpFormatter):

    def __init__(
        self,
        indent_increment: int = 2,
        width: Optional[int] = None,
        max_width: Optional[int] = None,
    ) -> None:
        super().__init__(indent_increment=indent_increment, width=width, max_width=max_width)
        self.highlighters = self.init_highlighters()
        self.console = self.init_console()

    def init_highlighters(self) -> Dict[str, RegexHighlighter]:
        class OptionHighlighter(RegexHighlighter):
            highlights = [
                r"(?P<switch>^\-\w$)",
                r"(?P<option>^\-\-[\w\-]+)(?P<metavar>\s.*$)?",
                r"(?P<args_and_cmds>^[\w]+$)",
            ]

        class HelpHighlighter(RegexHighlighter):
            highlights = [
                r"(?P<help_require>\([\w\s\d:]+\)$)",
            ]

        return_highlighters = {
            "opt": OptionHighlighter(), "help": HelpHighlighter()}

        return return_highlighters

    def init_console(self) -> Console:
        console = Console(
            theme=Theme(
                {
                    "option": "bold cyan",
                    "switch": "bold green",
                    "metavar": "bold yellow",
                    "help_require": "dim",
                    "args_and_cmds": "yellow"
                }
            ),
            # highlighter=self.highlighter,
        )
        return console

    @contextmanager
    def section(self, name: str) -> Iterator[None]:
        options_table = Table(highlight=True, box=None, show_header=False)
        yield options_table
        self.write(Panel(
            options_table, border_style="dim", title=name, title_align="left"
        ))

    def add_params(self, params: List[Tuple[str, str]], table: Table) -> None:
        for name, help in params:
            arg_list = name.split(',')
            if len(arg_list) == 2:
                opt1 = self.highlighters['opt'](arg_list[0])
                opt2 = self.highlighters['opt'](arg_list[1].strip())
            else:
                opt1 = Text("")
                opt2 = self.highlighters['opt'](arg_list[0])
            help = self.escape_text(help)
            help = Text.from_markup(help, emoji=False)

            table.add_row(opt1, opt2, self.highlighters['help'](help))

    def escape_text(self, text: str) -> str:
        match = re.search(r"(?:\[([\w\s\d:]+?)\]$)", text)
        if match:
            text = text.replace("[%s]" % match.group(1),
                                "(%s)" % match.group(1))
        return text

    def write_usage(
        self, prog: str, args: str = "", prefix: Optional[str] = None
    ) -> None:
        # ! 如果过长 会导致换行
        prog = "[bold]{}[/bold]".format(prog)
        args = "[bold][cyan]{}[/bold][/cyan]".format(
            args)
        super().write_usage(prog, args, prefix)

    def write_epilog(self, epilog: str) -> None:
        self.write(blend_text(epilog, (32, 32, 255), (255, 32, 255)), "right")

    def write(
        self, string: str | Text | Panel,
        justify: Optional[JustifyMethod] = None
    ) -> None:
        if string == "\n":
            self.console.print()
        else:
            self.console.print(string, justify=justify)
