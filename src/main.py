import argparse
import sys
from vfs import VFS
from commands import execute_command, set_vfs

def parse_args():
    parser = argparse.ArgumentParser(description="Shell Emulator")
    parser.add_argument("--vfs", type=str, help="Путь к XML файлу VFS", default="")
    parser.add_argument("--script", type=str, help="Путь к скрипту команд", default="")
    return parser.parse_args()

def main():
    args = parse_args()

    vfs = VFS()
    if args.vfs:
        success = vfs.load_from_xml(args.vfs)
        if success:
            print(f"VFS '{vfs.name}' успешно загружена.")
        else:
            print("Не удалось загрузить VFS.")
    
    set_vfs(vfs)

    # Если передан скрипт для автоматического выполнения команд
    if args.script:
        try:
            with open(args.script, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    print(f"$ {line}")
                    parts = line.split()
                    cmd, cmd_args = parts[0], parts[1:]
                    res = execute_command(cmd, cmd_args)
                    if res == "EXIT":
                        break
                    if res:
                        print(res)
        except Exception as e:
            print(f"Ошибка при исполнении скрипта: {e}")
        return

    # Интерактивный режим
    while True:
        try:
            prompt = f"{vfs.current_path}$ "
            user_input = input(prompt).strip()
            if not user_input:
                continue
            
            parts = user_input.split()
            cmd, cmd_args = parts[0], parts[1:]
            
            res = execute_command(cmd, cmd_args)
            if res == "EXIT":
                print("Завершение работы эмулятора.")
                break
            if res:
                print(res)
        except (KeyboardInterrupt, EOFError):
            print("\nЗавершение работы эмулятора.")
            break

if __name__ == "__main__":
    main()