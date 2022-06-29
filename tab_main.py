import tkinter as tk
from tkinter import ttk

from tab_settings import TaskConfig


class TaskSheetMain(tk.Frame):
    def create_calc(self):
        self.var_weight = tk.IntVar()
        self.var_lenght = tk.IntVar()
        self.var_floor = tk.IntVar()
        self.var_time_for_wait = tk.StringVar()
        self.rb_elevator = tk.BooleanVar()
        self.rb_from_to = tk.BooleanVar()
        self.var_sum = tk.IntVar()
        self.var_sum.set(3000)

        self.s_car = 0
        self.s_up = 0
        self.s_up_plus = 0
        self.s_down = 0
        self.s_down_plus = 0
        self.s_distance = 0
        self.s_elevator = 0

        self.var_address_from = tk.StringVar()
        self.var_address_to = tk.StringVar()

        self.dict_time_for_wait = {'1 час': 1, '2 часа': 2, '3 часа': 3, '4 часа': 4, '5 часов': 5}
        lb_time_for_wait = ttk.Combobox(self, values=list(sorted(self.dict_time_for_wait.keys())),
                                        textvariable=self.var_time_for_wait
                                        , state="readonly")
        lb_time_for_wait.current(0)

        l_weight = tk.Label(self, text="Вес", font="Arial 13", width=17, justify='left', anchor='sw')
        l_lenght = tk.Label(self, text="Расстояние", font="Arial 13", width=17, justify='left', anchor='sw')
        l_floor = tk.Label(self, text="Этаж", font="Arial 13", width=17, justify='left', anchor='sw')
        l_elevator = tk.Label(self, text="Лифт", font="Arial 13", width=17, justify='left', anchor='sw')
        l_time_for_wait = tk.Label(self, text="Ожидание", font="Arial 13", width=17, justify='left', anchor='sw')
        l_sum = tk.Label(self, text="Итого", font="Arial 20", width=25, justify='left', anchor='sw')

        t_weight = tk.Entry(self, font="Arial 13", width=17, textvariable=self.var_weight, validate="all")
        t_lenght = tk.Entry(self, font="Arial 13", width=17, textvariable=self.var_lenght, validate="all")
        t_floor = tk.Entry(self, font="Arial 13", width=17, textvariable=self.var_floor, validate="all")
        t_sum = tk.Entry(self, font="Arial 20", width=25, textvariable=self.var_sum, validate="all")

        t_weight['vcmd'] = (t_weight.register(self.validate), '%P', '%d')
        t_lenght['vcmd'] = (t_lenght.register(self.validate), '%P', '%d')
        t_floor['vcmd'] = (t_floor.register(self.validate), '%P', '%d')
        t_sum['vcmd'] = (t_sum.register(self.validate), '%P', '%d')

        self.rb_elevator.set(0)
        self.switch = ttk.Checkbutton(self, style="Switch", text="Нет", variable=self.rb_elevator,
                                      command=self.update_status)  # , text="Лифт",)

        l_weight.place(x=10, y=30)
        t_weight.place(x=110, y=30, width=135)

        l_lenght.place(x=10, y=60)
        t_lenght.place(x=110, y=60, width=135)

        l_floor.place(x=10, y=90, width=135)
        t_floor.place(x=110, y=90, width=135)

        l_elevator.place(x=10, y=120)
        self.switch.place(x=110, y=120)  # , width=135)

        lb_time_for_wait.place(x=110, y=150)
        l_time_for_wait.place(x=10, y=150, width=90)

        l_sum.place(x=10, y=390, width=135)
        t_sum.place(x=100, y=390, width=135)

    def get_values(self, event):
        field_weight = self.var_weight.get()
        field_lenght = self.var_lenght.get()
        field_floor = self.var_floor.get()
        field_time_for_waiting = self.dict_time_for_wait[self.var_time_for_wait.get()]
        field_elevator = self.rb_elevator.get()

        if field_weight == "":
            self.var_weight.set(0)
        if field_lenght == "":
            self.field_lenght.set(0)
        if field_floor == "":
            self.field_floor.set(0)

        if int(field_weight) >= 100:
            elevator_sum = (int(field_floor) * self.s_up_plus) + (int(field_floor) * self.s_down_plus)
            print(int(field_floor))
            print(self.s_up_plus)
            print(self.s_down_plus)
        else:
            elevator_sum = (int(field_floor) * self.s_up) + (int(field_floor) * self.s_down)

        if field_elevator:
            elevator_sum = elevator_sum * self.s_elevator / 100
        itogo_sum = self.s_car
        itogo_sum = int(itogo_sum) + int(elevator_sum) + (int(field_lenght) * self.s_distance) + (
                field_time_for_waiting * 1000)

        self.var_sum.set(itogo_sum)

    def update_status(self):
        if self.rb_elevator.get():
            self.switch.config(text="Есть")
        else:
            self.switch.config(text="Нет")

    def update_from_to(self):
        if self.rb_from_to.get():
            self.switch_from_to.config(text="Да")
        else:
            self.switch_from_to.config(text="Нет")

    def get_settings(self, valuess):
        self.s_car = valuess['car']
        self.s_up = valuess['up']
        self.s_up_plus = valuess['up_plus']
        self.s_down = valuess['down']
        self.s_down_plus = valuess['down_plus']
        self.s_distance = valuess['distance']
        self.s_elevator = valuess['elevator']

    def validate(self,value, action):
        if action == '1':
            return value.isdigit()
        return True