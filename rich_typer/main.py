from typing import Any, Callable, Dict, Optional, Type, List, Tuple
import inspect

import click
import typer
from rich.console import JustifyMethod
from typer.models import CommandFunctionType, Default, DefaultPlaceholder
from typer.main import (
    get_install_completion_arguments,
    solve_typer_info_defaults,
    get_params_convertors_ctx_param_name_from_function,
    get_callback,
    get_command_name,
    get_group_name,
    solve_typer_info_help,
)

from .core import RichCommand, RichGroup
from .models import CommandInfo, TyperInfo


class RichTyper(typer.Typer):

    def __init__(
        self,
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
        banner: Optional[str] = Default(None),
        banner_justify: Optional[JustifyMethod] = Default(None),
        usage: Optional[str] = Default(None),
        epilog: Optional[str] = Default(None),
        epilog_blend: Optional[Tuple[Tuple[int, int, int],
                                     Tuple[int, int, int]]] = Default(None),
        short_help: Optional[str] = Default(None),
        options_metavar: str = Default("[OPTIONS]"),
        add_help_option: bool = Default(True),
        hidden: bool = Default(False),
        deprecated: bool = Default(False),
        add_completion: bool = True,
    ):
        """
        :name: 程序名称
        :cls: click.core.Group 类
        :invoke_without_command: 单独调用时，是否自动执行
        :no_args_is_help: 取消参数帮助
        :subcommand_metavar: 子命令显示名称
        :chain:
        :result_callback: 结果回调函数
        :context_settings:
        :callback: 命令回调函数
        :help: 帮助信息
        :banner: 标题
        :banner_justify: 标题对齐方式
        :usage: 自定义命令用法
        :epilog: 底部信息
        :epilog_blend: 底部信息颜色混合，使用两个RGB的元组
        :short_help: 短的帮助信息
        :options_metavar: 参数显示名称
        :add_help_option: 是否添加帮助选项
        :hidden: 是否隐藏
        :deprecated: 是否为废弃命令
        :add_completion: 是否添加自动完成
        """
        if not cls:
            cls = RichGroup
        self._add_completion = add_completion
        self.info = TyperInfo(
            name=name,
            cls=cls,
            invoke_without_command=invoke_without_command,
            no_args_is_help=no_args_is_help,
            subcommand_metavar=subcommand_metavar,
            chain=chain,
            result_callback=result_callback,
            context_settings=context_settings,
            callback=callback,
            help=help,
            banner=banner,
            banner_justify=banner_justify,
            usage=usage,
            epilog=epilog,
            epilog_blend=epilog_blend,
            short_help=short_help,
            options_metavar=options_metavar,
            add_help_option=add_help_option,
            hidden=hidden,
            deprecated=deprecated,
        )
        self.registered_groups: List[TyperInfo] = []
        self.registered_commands: List[CommandInfo] = []
        self.registered_callback: Optional[TyperInfo] = None

    def command(
        self,
        name: Optional[str] = None,
        *,
        cls: Optional[Type[click.Command]] = None,
        context_settings: Optional[Dict[Any, Any]] = None,
        help: Optional[str] = None,
        epilog: Optional[str] = None,
        epilog_blend: Optional[Tuple[Tuple[int, int, int],
                                     Tuple[int, int, int]]] = None,
        short_help: Optional[str] = None,
        banner: Optional[str] = None,
        banner_justify: Optional[JustifyMethod] = None,
        usage: Optional[str] = None,
        options_metavar: str = "[OPTIONS]",
        add_help_option: bool = True,
        no_args_is_help: bool = False,
        hidden: bool = False,
        deprecated: bool = False,
    ) -> Callable[[CommandFunctionType], CommandFunctionType]:
        """
        :name: 命令名称
        :cls: click.core.Command 类
        :context_settings: 命令上下文设置
        :help: 帮助信息
        :epilog: 底部信息
        :epilog_blend: 底部信息颜色混合，使用两个RGB的元组
        :short_help: 短的帮助信息
        :banner: 标题
        :banner_justify: 标题对齐方式
        :usage: 自定义命令用法
        :options_metavar: 参数显示名称
        :add_help_option: 是否添加帮助选项
        :no_args_is_help: 取消参数帮助
        :hidden: 是否隐藏
        :deprecated: 是否为废弃命令
        """
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
                    epilog_blend=epilog_blend,
                    short_help=short_help,
                    banner=banner,
                    banner_justify=banner_justify,
                    usage=usage,
                    options_metavar=options_metavar,
                    add_help_option=add_help_option,
                    no_args_is_help=no_args_is_help,
                    hidden=hidden,
                    deprecated=deprecated,
                )
            )
            return f

        return decorator

    def callback(
        self,
        name: Optional[str] = Default(None),
        *,
        cls: Optional[Type[click.Command]] = Default(None),
        invoke_without_command: bool = Default(False),
        no_args_is_help: bool = Default(False),
        subcommand_metavar: Optional[str] = Default(None),
        chain: bool = Default(False),
        result_callback: Optional[Callable[..., Any]] = Default(None),
        # Command
        context_settings: Optional[Dict[Any, Any]] = Default(None),
        help: Optional[str] = Default(None),
        epilog: Optional[str] = Default(None),
        epilog_blend: Optional[Tuple[Tuple[int, int, int],
                                     Tuple[int, int, int]]] = Default(None),
        short_help: Optional[str] = Default(None),
        banner: Optional[str] = Default(None),
        banner_justify: Optional[JustifyMethod] = Default(None),
        usage: Optional[str] = Default(None),
        options_metavar: str = Default("[OPTIONS]"),
        add_help_option: bool = Default(True),
        hidden: bool = Default(False),
        deprecated: bool = Default(False),
    ) -> Callable[[CommandFunctionType], CommandFunctionType]:
        """
        :name: 命令名称
        :cls: click.core.TypeGroup 类
        :invoke_without_command: 是否可以不带参数
        :no_args_is_help: 取消参数帮助
        :subcommand_metavar: 子命令名称
        :chain: 是否链式调用
        :result_callback: 回调函数
        :context_settings: 命令上下文设置
        :help: 帮助信息
        :epilog: 底部信息
        :epilog_blend: 底部信息颜色混合，使用两个RGB的元组
        :short_help: 短的帮助信息
        :banner: 标题
        :banner_justify: 标题对齐方式
        :usage: 自定义命令用法
        :options_metavar: 参数显示名称
        :add_help_option: 是否添加帮助选项
        :hidden: 是否隐藏
        :deprecated: 是否为废弃命令
        """
        def decorator(f: CommandFunctionType) -> CommandFunctionType:
            self.registered_callback = TyperInfo(
                name=name,
                cls=cls,
                invoke_without_command=invoke_without_command,
                no_args_is_help=no_args_is_help,
                subcommand_metavar=subcommand_metavar,
                chain=chain,
                result_callback=result_callback,
                context_settings=context_settings,
                callback=f,
                help=help,
                epilog=epilog,
                epilog_blend=epilog_blend,
                short_help=short_help,
                banner=banner,
                banner_justify=banner_justify,
                usage=usage,
                options_metavar=options_metavar,
                add_help_option=add_help_option,
                hidden=hidden,
                deprecated=deprecated,
            )
            return f

        return decorator

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return get_command(self)(*args, **kwargs)


def get_group(typer_instance: typer.Typer) -> click.Command:
    group = get_group_from_info(TyperInfo(typer_instance))
    return group


def get_command(typer_instance: typer.Typer) -> click.Command:
    if typer_instance._add_completion:
        click_install_param, click_show_param = get_install_completion_arguments()
    if (
        typer_instance.registered_callback
        or typer_instance.info.callback
        or typer_instance.registered_groups
        or len(typer_instance.registered_commands) > 1
    ):
        # Create a Group
        click_command = get_group(typer_instance)
        if typer_instance._add_completion:
            click_command.params.append(click_install_param)
            click_command.params.append(click_show_param)
        return click_command
    elif len(typer_instance.registered_commands) == 1:
        # Create a single Command
        click_command = get_command_from_info(
            typer_instance.registered_commands[0])
        if typer_instance._add_completion:
            click_command.params.append(click_install_param)
            click_command.params.append(click_show_param)
        return click_command
    assert False, "Could not get a command for this Typer instance"  # pragma no cover


def get_group_from_info(group_info: TyperInfo) -> click.Command:
    assert (
        group_info.typer_instance
    ), "A Typer instance is needed to generate a Click Group"
    commands: Dict[str, click.Command] = {}
    for command_info in group_info.typer_instance.registered_commands:
        command = get_command_from_info(command_info=command_info)
        if command.name:
            commands[command.name] = command
    for sub_group_info in group_info.typer_instance.registered_groups:
        sub_group = get_group_from_info(sub_group_info)
        if sub_group.name:
            commands[sub_group.name] = sub_group
    solved_info: TyperInfo = solve_typer_info_defaults(group_info)
    (
        params,
        convertors,
        context_param_name,
    ) = get_params_convertors_ctx_param_name_from_function(solved_info.callback)
    cls = solved_info.cls or RichGroup
    group = cls(  # type: ignore
        name=solved_info.name or "",
        commands=commands,
        invoke_without_command=solved_info.invoke_without_command,
        no_args_is_help=solved_info.no_args_is_help,
        subcommand_metavar=solved_info.subcommand_metavar,
        chain=solved_info.chain,
        result_callback=solved_info.result_callback,
        context_settings=solved_info.context_settings,
        callback=get_callback(
            callback=solved_info.callback,
            params=params,
            convertors=convertors,
            context_param_name=context_param_name,
        ),
        params=params,  # type: ignore
        help=solved_info.help,
        epilog=solved_info.epilog,
        epilog_blend=solved_info.epilog_blend,
        short_help=solved_info.short_help,
        banner=solved_info.banner,
        banner_justify=solved_info.banner_justify,
        usage=solved_info.usage,
        options_metavar=solved_info.options_metavar,
        add_help_option=solved_info.add_help_option,
        hidden=solved_info.hidden,
        deprecated=solved_info.deprecated,
    )
    return group


def get_command_from_info(command_info: CommandInfo) -> click.Command:
    assert command_info.callback, "A command must have a callback function"
    name = command_info.name or get_command_name(
        command_info.callback.__name__)
    use_help = command_info.help
    if use_help is None:
        use_help = inspect.getdoc(command_info.callback)
    else:
        use_help = inspect.cleandoc(use_help)
    (
        params,
        convertors,
        context_param_name,
    ) = get_params_convertors_ctx_param_name_from_function(command_info.callback)
    cls = command_info.cls or RichCommand
    command = cls(
        name=name,
        context_settings=command_info.context_settings,
        callback=get_callback(
            callback=command_info.callback,
            params=params,
            convertors=convertors,
            context_param_name=context_param_name,
        ),
        params=params,  # type: ignore
        help=use_help,
        epilog=command_info.epilog,
        epilog_blend=command_info.epilog_blend,
        short_help=command_info.short_help,
        banner=command_info.banner,
        banner_justify=command_info.banner_justify,
        usage=command_info.usage,
        options_metavar=command_info.options_metavar,
        add_help_option=command_info.add_help_option,
        no_args_is_help=command_info.no_args_is_help,
        hidden=command_info.hidden,
        deprecated=command_info.deprecated,
    )
    return command


def solve_typer_info_defaults(typer_info: TyperInfo) -> TyperInfo:
    values: Dict[str, Any] = {}
    name = None
    for name, value in typer_info.__dict__.items():
        # Priority 1: Value was set in app.add_typer()
        if not isinstance(value, DefaultPlaceholder):
            values[name] = value
            continue
        # Priority 2: Value was set in @subapp.callback()
        try:
            callback_value = getattr(
                typer_info.typer_instance.registered_callback, name  # type: ignore
            )
            if not isinstance(callback_value, DefaultPlaceholder):
                values[name] = callback_value
                continue
        except AttributeError:
            pass
        # Priority 3: Value set in subapp = typer.Typer()
        try:
            instance_value = getattr(
                typer_info.typer_instance.info, name  # type: ignore
            )
            if not isinstance(instance_value, DefaultPlaceholder):
                values[name] = instance_value
                continue
        except AttributeError:
            pass
        # Value not set, use the default
        values[name] = value.value
    if values["name"] is None:
        values["name"] = get_group_name(typer_info)
    values["help"] = solve_typer_info_help(typer_info)
    return TyperInfo(**values)
