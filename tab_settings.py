import re
import tkinter as tk
from tkinter import ttk


class TaskConfig(tk.Frame):
    def create_config(self):
        self.var_car = tk.IntVar()
        self.var_up = tk.IntVar()
        self.var_up_plus = tk.IntVar()
        self.var_down = tk.IntVar()
        self.var_down_plus = tk.IntVar()
        self.var_distance = tk.IntVar()
        self.var_elevator = tk.IntVar()

        self.def_var_car = 2000
        self.def_var_up = 200
        self.def_var_up_plus = 300
        self.def_var_down = 100
        self.def_var_down_plus = 150
        self.def_var_distance = 60
        self.def_var_elevator = 50

        l_car = tk.Label(self, text="Подача машины", font="Arial 13", width=17, justify='left', anchor='sw')
        t_car = tk.Entry(self, font="Arial 13", width=17, textvariable=self.var_car)
        l_car.place(x=10, y=30, width=200)
        t_car.place(x=250, y=30, width=135)

        l_up = tk.Label(self, text="Подъем, за этаж", font="Arial 13", width=17, justify='left', anchor='sw')
        t_up = tk.Entry(self, font="Arial 13", width=17, textvariable=self.var_up)
        l_up.place(x=10, y=60, width=200)
        t_up.place(x=250, y=60, width=135)

        l_up_plus = tk.Label(self, text="Подъем 100+,за этаж", font="Arial 13", width=17, justify='left', anchor='sw')
        t_up_plus = tk.Entry(self, font="Arial 13", width=17, textvariable=self.var_up_plus)
        l_up_plus.place(x=10, y=90, width=200)
        t_up_plus.place(x=250, y=90, width=135)

        l_down = tk.Label(self, text="Спуск, за этаж", font="Arial 13", width=17, justify='left', anchor='sw')
        t_down = tk.Entry(self, font="Arial 13", width=17, textvariable=self.var_down)
        l_down.place(x=10, y=120, width=200)
        t_down.place(x=250, y=120, width=135)

        l_down_plus = tk.Label(self, text="Спуск 100+, за этаж", font="Arial 13", width=17, justify='left', anchor='sw')
        t_down_plus = tk.Entry(self, font="Arial 13", width=17, textvariable=self.var_down_plus)
        l_down_plus.place(x=10, y=150, width=200)
        t_down_plus.place(x=250, y=150, width=135)

        l_distance = tk.Label(self, text="Расстояние, за км", font="Arial 13", width=17, justify='left', anchor='sw')
        t_distance = tk.Entry(self, font="Arial 13", width=17, textvariable=self.var_distance)
        l_distance.place(x=10, y=180, width=200)
        t_distance.place(x=250, y=180, width=135)

        l_elevator = tk.Label(self, text="Лифт, скидка %", font="Arial 13", width=17, justify='left', anchor='sw')
        t_elevator = tk.Entry(self, font="Arial 13", width=17, textvariable=self.var_elevator)
        l_elevator.place(x=10, y=210, width=200)
        t_elevator.place(x=250, y=210, width=135)

        b_default = tk.Button(self, text="Сбросить настройки", width=10, command=self.set_default)
        b_default.place(x=10, y=400, width=135)

        b_new_config = tk.Button(self, text="Сохранить настройки", width=10, command=self.set_new_config)
        b_new_config.place(x=150, y=400, width=135)

    def set_default(self):
        text = 'car:{}\nup:{}\nup_plus:{}\ndown:{}\ndown_plus:{}\ndistance:{}\nelevator:{}'.format(
            self.def_var_car,
            self.def_var_up,
            self.def_var_up_plus,
            self.def_var_down,
            self.def_var_down_plus,
            self.def_var_distance,
            self.def_var_elevator)
        # print(text)
        f = open('config.txt', 'w')
        f.write(text)
        f.close()
        self.get_config()
        print(a)

    def set_new_config(self):
        car = self.var_car.get()
        up = self.var_up.get()
        up_plus = self.var_up_plus.get()
        down = self.var_down.get()
        down_plus = self.var_down_plus.get()
        distance = self.var_distance.get()
        elevator = self.var_elevator.get()
        text = 'car:{}\nup:{}\nup_plus:{}\ndown:{}\ndown_plus:{}\ndistance:{}\nelevator:{}'.format(car, up,
                                                                                                   up_plus,
                                                                                                   down,
                                                                                                   down_plus,
                                                                                                   distance,
                                                                                                   elevator)
        # print(text)
        f = open('config.txt', 'w')
        f.write(text)
        f.close()
        self.get_config()

    def get_config(self):
        f = open('config.txt', 'r')
        valuess = {}
        for line in f:

            car = re.findall("\d+", str(re.findall('car:\d+', line)))
            up = re.findall("\d+", str(re.findall('up:\d+', line)))
            up_plus = re.findall("\d+", str(re.findall('up_plus:\d+', line)))
            down = re.findall("\d+", str(re.findall('down:\d+', line)))
            down_plus = re.findall("\d+", str(re.findall('down_plus:\d+', line)))
            distance = re.findall("\d+", str(re.findall('distance:\d+', line)))
            elevator = re.findall("\d+", str(re.findall('elevator:\d+', line)))

            if car:
                self.var_car.set(int(car[0]))
                valuess['car'] = int(car[0])
                print(int(car[0]))
            if up:
                self.var_up.set(int(up[0]))
                valuess['up'] = int(up[0])
                print(int(up[0]))
            if up_plus:
                self.var_up_plus.set(int(up_plus[0]))
                valuess['up_plus'] = int(up_plus[0])
                print(int(up_plus[0]))
            if down:
                self.var_down.set(int(down[0]))
                valuess['down'] = int(down[0])
            if down_plus:
                self.var_down_plus.set(int(down_plus[0]))
                valuess['down_plus'] = int(down_plus[0])
            if distance:
                self.var_distance.set(int(distance[0]))
                valuess['distance'] = int(distance[0])
            if elevator:
                self.var_elevator.set(int(elevator[0]))
                valuess['elevator'] = int(elevator[0])
        return valuess
