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
        return "Ошибка: не указан путь"
    return vfs.change_dir(args[0])

def cmd_exit(args: list[str]) -> str:
    return "EXIT"

def execute_command(command: str, args: list[str]) -> str:
    commands = {
        "ls": cmd_ls,
        "cd": cmd_cd,
        "exit": cmd_exit,
    }

    if command in commands:
        return commands[command](args)
    else:
        return f"Ошибка: неизвестная команда '{command}'"