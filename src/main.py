import tkinter as tk
from tkinter import scrolledtext
import getpass
import socket
import os

from parser import parse_command
from commands import execute_command
from config import parse_args


class ShellEmulator:
    def __init__(self, root, vfs_path=None, script_path=None):
        self.root = root
        self.vfs_path = vfs_path
        self.script_path = script_path

        username = getpass.getuser()
        hostname = socket.gethostname()
        self.root.title(f"Эмулятор - [{username}@{hostname}]")
        self.root.geometry("800x500")

        self.output = scrolledtext.ScrolledText(
            root, state="disabled", wrap=tk.WORD, font=("Consolas", 11)
        )
        self.output.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.input_frame = tk.Frame(root)
        self.input_frame.pack(fill=tk.X, padx=5, pady=5)

        self.prompt_label = tk.Label(
            self.input_frame, text="> ", font=("Consolas", 11)
        )
        self.prompt_label.pack(side=tk.LEFT)

        self.entry = tk.Entry(self.input_frame, font=("Consolas", 11))
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.bind("<Return>", self.on_enter)
        self.entry.focus()

        self.print_output("Эмулятор оболочки запущен.")
        self.print_output(f"VFS path: {self.vfs_path}")
        self.print_output(f"Script path: {self.script_path}")
        self.print_output("Доступные команды: ls, cd, exit\n")

        if self.script_path:
            self.run_script(self.script_path)

    def print_output(self, text: str):
        self.output.configure(state="normal")
        self.output.insert(tk.END, text + "\n")
        self.output.configure(state="disabled")
        self.output.see(tk.END)

    def on_enter(self, event):
        line = self.entry.get()
        self.entry.delete(0, tk.END)
        should_continue = self.execute_line(line)
        if not should_continue:
            self.root.destroy()

    def execute_line(self, line: str) -> bool:
        if not line.strip():
            return True

        self.print_output(f"> {line}")

        parts = parse_command(line)
        if not parts:
            self.print_output("Ошибка: не удалось разобрать команду")
            return True

        command = parts[0]
        args = parts[1:]

        result = execute_command(command, args)

        if result == "EXIT":
            return False

        self.print_output(result)
        return True

    def run_script(self, script_path: str):
        if not os.path.exists(script_path):
            self.print_output(f"Ошибка: файл скрипта не найден: {script_path}")
            return

        self.print_output(f"--- Выполнение скрипта: {script_path} ---")

        try:
            with open(script_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue

                    should_continue = self.execute_line(line)
                    if not should_continue:
                        self.print_output("--- Скрипт завершён (exit) ---")
                        self.root.destroy()
                        return

        except Exception as e:
            self.print_output(f"Ошибка при чтении скрипта: {e}")

        self.print_output("--- Скрипт завершён ---\n")


def main():
    args = parse_args()

    print("=== Отладочный вывод параметров ===")
    print(f"VFS path: {args.vfs}")
    print(f"Script path: {args.script}")
    print("===================================")

    root = tk.Tk()
    app = ShellEmulator(root, vfs_path=args.vfs, script_path=args.script)
    root.mainloop()


if __name__ == "__main__":
    main()