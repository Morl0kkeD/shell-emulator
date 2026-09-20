import tkinter as tk
from tkinter import scrolledtext
import getpass
import socket

from parser import parse_command
from commands import execute_command


class ShellEmulator:
    def __init__(self, root):
        self.root = root

        # Заголовок окна по требованию варианта
        username = getpass.getuser()
        hostname = socket.gethostname()
        self.root.title(f"Эмулятор - [{username}@{hostname}]")

        self.root.geometry("800x500")

        # Область вывода
        self.output = scrolledtext.ScrolledText(
            root, state="disabled", wrap=tk.WORD, font=("Consolas", 11)
        )
        self.output.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Поле ввода
        self.input_frame = tk.Frame(root)
        self.input_frame.pack(fill=tk.X, padx=5, pady=5)

        self.prompt_label = tk.Label(self.input_frame, text="> ", font=("Consolas", 11))
        self.prompt_label.pack(side=tk.LEFT)

        self.entry = tk.Entry(self.input_frame, font=("Consolas", 11))
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.bind("<Return>", self.on_enter)
        self.entry.focus()

        self.print_output("Эмулятор оболочки запущен. Введите команду.")
        self.print_output("Доступные команды: ls, cd, exit\n")

    def print_output(self, text: str):
        self.output.configure(state="normal")
        self.output.insert(tk.END, text + "\n")
        self.output.configure(state="disabled")
        self.output.see(tk.END)

    def on_enter(self, event):
        line = self.entry.get()
        self.entry.delete(0, tk.END)

        if not line.strip():
            return

        self.print_output(f"> {line}")

        parts = parse_command(line)
        if not parts:
            self.print_output("Ошибка: не удалось разобрать команду")
            return

        command = parts[0]
        args = parts[1:]

        result = execute_command(command, args)

        if result == "EXIT":
            self.root.destroy()
            return

        self.print_output(result)


def main():
    root = tk.Tk()
    app = ShellEmulator(root)
    root.mainloop()


if __name__ == "__main__":
    main()