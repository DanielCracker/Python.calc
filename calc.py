import tkinter as tk
from tkinter import ttk

from tab_main import TaskSheetMain
from tab_settings import TaskConfig


class MainInterface:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Калькулятор стоимости')
        self.window.geometry("500x500")
        self.create_widgets()
        self.window.configure(background='black')
        self.window.option_add("*tearOff", False)
        self.window.iconbitmap('ik.ico')

    def create_widgets(self):
        self.window['padx'] = 5
        self.window['pady'] = 5
        self.notebook = ttk.Notebook(self.window, width=1000, height=700)
        style = ttk.Style(self.window)
        self.window.call("source", "forest-dark.tcl")
        style.theme_use("forest-dark")

        tab_set = TaskConfig(self.notebook)
        tab_main = TaskSheetMain(self.notebook)
        self.window.bind("<Key>", tab_main.get_values)
        self.window.bind("<Button-1>", tab_main.get_values)
        self.window.bind("<Motion>", tab_main.get_values)

        self.notebook.add(tab_main, text="Калькулятор")
        self.notebook.add(tab_set, text="Настройки")
        self.notebook.pack(expand=1, fill="both")
        tab_main.create_calc()
        tab_set.create_config()
        valuess = tab_set.get_config()

        tab_main.get_settings(valuess)


if __name__ == '__main__':
    program = MainInterface()
    program.window.mainloop()
