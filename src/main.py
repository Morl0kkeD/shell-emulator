import argparse
import sys
import os
import getpass
import socket
import tkinter as tk
from tkinter import scrolledtext

from vfs import VFS
import commands

def run_gui(vfs_instance):
    username = getpass.getuser()
    hostname = socket.gethostname()
    
    root = tk.Tk()
    root.title(f"Эмулятор - [{username}@{hostname}]")
    root.geometry("700x450")
    root.configure(bg="black")

    text_area = scrolledtext.ScrolledText(
        root, wrap=tk.WORD, bg="black", fg="lime", 
        insertbackground="white", font=("Consolas", 11)
    )
    text_area.pack(fill=tk.BOTH, expand=True)

    def print_text(text):
        text_area.insert(tk.END, text + "\n")
        text_area.see(tk.END)

    print_text(f"--- VFS '{vfs_instance.name}' успешно загружена ---")
    print_text(f"Текущая директория: {vfs_instance.current_path}")
    text_area.insert(tk.END, f"{vfs_instance.current_path} $ ")

    input_start_mark = text_area.index("insert")

    def on_enter(event):
        nonlocal input_start_mark
        user_input = text_area.get(input_start_mark, "end-1c").strip()
        print_text("")
        
        if user_input:
            parts = user_input.split()
            cmd, cmd_args = parts[0], parts[1:]
            res = commands.execute_command(cmd, cmd_args)
            
            if res == "EXIT":
                root.destroy()
                return "break"
            if res:
                print_text(res)

        text_area.insert(tk.END, f"{vfs_instance.current_path} $ ")
        input_start_mark = text_area.index("insert")
        return "break"

    text_area.bind("<Return>", on_enter)
    root.mainloop()

def main():
    parser = argparse.ArgumentParser(description="Shell Emulator")
    parser.add_argument("--vfs", type=str, help="Путь к XML файлу VFS")
    parser.add_argument("--script", type=str, help="Путь к стартовому скрипту")
    args = parser.parse_args()

    vfs_instance = VFS()
    if args.vfs:
        vfs_instance.load_from_xml(args.vfs)

    commands.set_vfs(vfs_instance)

    # Режим скрипта (без GUI)
    if args.script:
        if not os.path.exists(args.script):
            print(f"Ошибка: файл скрипта не найден: {args.script}")
            return
        with open(args.script, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                print(f"$ {line}")
                parts = line.split()
                cmd, cmd_args = parts[0], parts[1:]
                res = commands.execute_command(cmd, cmd_args)
                if res == "EXIT":
                    print("Завершение работы эмулятора.")
                    break
                if res:
                    print(res)
    else:
        # Обычный запуск с GUI
        run_gui(vfs_instance)

if __name__ == "__main__":
    main()