import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Эмулятор оболочки UNIX")
    parser.add_argument(
        "--vfs",
        type=str,
        default=None,
        help="Путь к физическому расположению VFS"
    )
    parser.add_argument(
        "--script",
        type=str,
        default=None,
        help="Путь к стартовому скрипту"
    )
    return parser.parse_args()