import shlex


def parse_command(line: str) -> list[str]:
    """
    Парсер, который корректно обрабатывает аргументы в кавычках.
    Пример: ls "my folder" -l  →  ['ls', 'my folder', '-l']
    """
    line = line.strip()
    if not line:
        return []

    try:
        # shlex умеет правильно разбирать кавычки
        return shlex.split(line)
    except ValueError:
        # Если кавычки не закрыты
        return []