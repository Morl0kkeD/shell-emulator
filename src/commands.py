def cmd_ls(args: list[str]) -> str:
    """Заглушка команды ls"""
    return f"ls: {args}"


def cmd_cd(args: list[str]) -> str:
    """Заглушка команды cd"""
    return f"cd: {args}"


def cmd_exit(args: list[str]) -> str:
    """Команда выхода"""
    return "EXIT"


def execute_command(command: str, args: list[str]) -> str:
    """
    Выполняет команду.
    Возвращает текст результата или 'EXIT'.
    """
    commands = {
        "ls": cmd_ls,
        "cd": cmd_cd,
        "exit": cmd_exit,
    }

    if command in commands:
        return commands[command](args)
    else:
        return f"Ошибка: неизвестная команда '{command}'"