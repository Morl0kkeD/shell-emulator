vfs = None

def set_vfs(v):
    global vfs
    vfs = v

def cmd_ls(args: list[str]) -> str:
    if vfs is None:
        return "ls: VFS не загружена"
    path = args[0] if args else ""
    return vfs.list_dir(path)

def cmd_cd(args: list[str]) -> str:
    if vfs is None:
        return "cd: VFS не загружена"
    if not args:
        return "cd: не указан путь"
    return vfs.change_dir(args[0])

def cmd_du(args: list[str]) -> str:
    if vfs is None:
        return "du: VFS не загружена"
    path = args[0] if args else ""
    return vfs.du(path)

def cmd_wc(args: list[str]) -> str:
    if vfs is None:
        return "wc: VFS не загружена"
    if not args:
        return "wc: не указан файл"
    return vfs.wc(args[0])

def cmd_echo(args: list[str]) -> str:
    return " ".join(args)

def cmd_touch(args: list[str]) -> str:
    if vfs is None:
        return "touch: VFS не загружена"
    if not args:
        return "touch: не указан файл"
    return vfs.touch(args[0])

def cmd_chown(args: list[str]) -> str:
    if vfs is None:
        return "chown: VFS не загружена"
    if len(args) < 2:
        return "chown: пропущен операнд после владельца"
    return vfs.chown(args[0], args[1])

def cmd_exit(args: list[str]) -> str:
    return "EXIT"

def execute_command(command: str, args: list[str]) -> str:
    commands = {
        "ls": cmd_ls,
        "cd": cmd_cd,
        "du": cmd_du,
        "wc": cmd_wc,
        "echo": cmd_echo,
        "touch": cmd_touch,
        "chown": cmd_chown,
        "exit": cmd_exit,
    }

    if command in commands:
        return commands[command](args)
    else:
        return f"Ошибка: неизвестная команда '{command}'"