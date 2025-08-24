import customtkinter as ct
from dotenv import load_dotenv
import os
import math
from PIL import Image, ImageTk
import re
import numpy
from classes.Graf import Graf
from classes.json_op import Json
from classes.ValCurs import ValCurs
from tkinter.messagebox import showerror

load_dotenv()


class Calculator_app:
    def __init__(self, root):
        self.root = root
        self.root.title(os.getenv('title'))
        self.root.geometry(f"{os.getenv('width')}x{os.getenv('height')}")
        self.root.resizable(False, False)
        self.json_history_objects = Json('history.json')
        self.history_list = self.json_history_objects.load_json()

        ct.set_appearance_mode(os.getenv('theme'))
        ct.set_default_color_theme(os.getenv('color_theme'))

        self.current_input = ''
        self.result_var = ct.StringVar(value='0')
        self.current_font = 24
        self.menu_visible = False
        self.current_mode = 'Обычный'
        self.graph_frame = None

        v = ValCurs()
        v.parse_with_xml()
        self.valute_dict = v.parse_with_xml()

        self.main_frame = ct.CTkFrame(self.root)
        self.main_frame.pack(fill='both', expand=True)
        self.history_text = ct.StringVar(value='')
        self.create_widgets()
        self.root.bind('<Key>', self.handle_key_press)

    def switch_mode(self, mode):
        self.current_mode = mode
        if mode == 'Графики':
            self.create_graph_interface()
        elif mode == 'Курс валют':
            self.create_valute_interface()
        else:
            # self.hide_graph_interface()
            self.create_calculator_interface()

    def create_valute_interface(self):
        def btn_ok():
            a = ''.join(filter(lambda x: x.isdigit() or x == '.', number_.get()))
            if list_.get() == 'Выберите вариант':
                showerror('Error', 'Выберите валюту')
                return

            res = float(a) * float(self.valute_dict[list_.get()].replace(',', '.'))
            number_.delete(0, ct.END)
            number_.insert(0, f'{res:.2f}')

        def on_key_release(event):
            a = ''.join(filter(lambda x: x.isdigit() or x == '.', number_.get()))
            number_.delete(0, ct.END)
            number_.insert(0, a)

        for widget in self.content_frame.winfo_children():
            widget.destroy()
        number_ = ct.CTkEntry(
            master=self.content_frame,
            placeholder_text='Введите сумму'
        )
        number_.bind('<KeyRelease>', on_key_release)
        number_.pack(pady=10, padx=10)

        list_ = ct.CTkComboBox(
            master=self.content_frame,
            values=list(self.valute_dict.keys()),
            state='readonly'
        )

        list_.pack(padx=10, pady=10)
        list_.set('Выберите вариант')

        btn = ct.CTkButton(master=self.content_frame, text='Oк', command=btn_ok)
        btn.pack()

    def create_graph_interface(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        self.menu_button = ct.CTkButton(
            self.content_frame,
            image=self.menu_icon,
            width=30,
            height=30,
            command=self.toggle_menu,
            text='>',
            compound='left'
        )
        self.menu_button.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky='nw')

        ct.CTkLabel(self.content_frame, text='Функция:').grid(row=1, column=0, padx=5, pady=5)
        self.function_entry = ct.CTkEntry(self.content_frame, width=200)
        self.function_entry.insert(0, 'x^2')
        self.function_entry.grid(row=1, column=1, padx=5, pady=5)

        ct.CTkLabel(self.content_frame, text='От:').grid(row=2, column=0, padx=5, pady=5)
        self.xmin_entry = ct.CTkEntry(self.content_frame, width=80)
        self.xmin_entry.insert(0, '-10')
        self.xmin_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        ct.CTkLabel(self.content_frame, text='До:').grid(row=3, column=0, padx=5, pady=5)
        self.xmax_entry = ct.CTkEntry(self.content_frame, width=80)
        self.xmax_entry.insert(0, '10')
        self.xmax_entry.grid(row=3, column=1, padx=5, pady=5, sticky='w')

        plot_button = ct.CTkButton(
            self.content_frame,
            text='Построить график',
            command=self.plot_function
        )
        plot_button.grid(row=4, column=0, columnspan=2, pady=10)
        if self.graph_frame:
            self.graph_frame.destroy()
        self.graph_frame = ct.CTkFrame(self.content_frame)
        self.graph_frame.grid(row=5, column=0, columnspan=2, sticky='nsew', padx=5, pady=5)

        self.content_frame.rowconfigure(5, weight=1)
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.columnconfigure(1, weight=1)

    def plot_function(self):
        function_text = self.function_entry.get()

        try:
            x_min = float(self.xmin_entry.get())
            x_max = float(self.xmax_entry.get())
            if x_min >= x_max:
                raise ValueError('Неверный диапазон')
        except ValueError:
            self.result_var.set('Ошибка в диапазоне')
            return
        x = numpy.linspace(x_min, x_max, int(os.getenv('x_count')))
        Graf(self.graph_frame, x, function_text)

    def hide_graph_interface(self):
        if self.graph_frame:
            self.graph_frame.destroy()
            self.graph_frame = None

    def create_calculator_interface(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.menu_button = ct.CTkButton(
            self.content_frame,
            image=self.menu_icon,
            width=30,
            height=30,
            command=self.toggle_menu,
            text='>',
            compound='left'
        )
        self.menu_button.grid(row=0, column=0, columnspan=5, sticky='nw', padx=5, pady=5)

        display_frame = ct.CTkFrame(self.content_frame, corner_radius=10)
        display_frame.grid(row=1, column=0, columnspan=5, pady=10, padx=5, sticky='nsew')

        self.history_display = ct.CTkLabel(
            display_frame,
            font=('Arial', 16),
            text='',
            height=40,
            anchor='e',
        )
        self.history_display.pack(fill='x', padx=5)

        self.display = ct.CTkLabel(
            display_frame,
            textvariable=self.result_var,
            font=('Arial', self.current_font),
            height=50,
            anchor='e'
        )
        self.display.pack(fill='x', pady=5, padx=5)

        buttons = [
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('/', 2, 3), ('(', 2, 4),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('*', 3, 3), (')', 3, 4),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('-', 4, 3), ('^2', 4, 4),
            ('0', 5, 0), ('.', 5, 1), ('=', 5, 2), ('+', 5, 3), ('√', 5, 4),
            ('C', 6, 0, 4), ('<', 6, 4)
        ]

        for button in buttons:
            text = button[0]
            row = button[1]
            col = button[2]
            colspan = button[3] if len(button) > 3 else 1

            btn = ct.CTkButton(
                self.content_frame,
                text=text,
                width=60 if colspan == 1 else 60 * colspan + 5 * (colspan - 1),
                height=50,
                font=('Arial', 18),
                command=lambda t=text: self.on_button_click(t)
            )
            btn.grid(row=row, column=col, columnspan=colspan, padx=2, pady=2, sticky='nsew')

        for i in range(5):
            self.content_frame.columnconfigure(i, weight=1)
        for i in range(7):
            self.content_frame.rowconfigure(i, weight=1)

    def toggle_menu(self):
        self.menu_visible = not self.menu_visible

        if self.menu_visible:
            self.menu_frame.pack(side='left', fill='y', padx=(0, 5))
            self.content_frame.pack(side='left', fill='both', expand=True)
            self.root.geometry(f"{int(os.getenv('width')) + 130}x{os.getenv('height')}")
            self.menu_button.configure(text='<')
        else:
            self.menu_frame.pack_forget()
            self.content_frame.pack(fill='both', expand=True)
            self.root.geometry(f"{os.getenv('width')}x{os.getenv('height')}")
            self.menu_button.configure(text='>')

    def handle_key_press(self, event):
        if self.current_mode != 'Обычный':
            return
        else:
            key = event.char
            if key in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '+', '*', '/', '='):
                self.on_button_click(key)

    def create_widgets(self):
        self.menu_frame = ct.CTkFrame(self.main_frame, width=120)

        menu_buttons = ['Обычный', 'Графики', 'Курс валют']
        for btn_text in menu_buttons:
            btn = ct.CTkButton(
                self.menu_frame,
                text=btn_text,
                width=110,
                height=30,
                font=('Arial', 12),
                fg_color='transparent',
                anchor='w',
                command=lambda mode=btn_text: self.switch_mode(mode)
            )
            btn.pack(pady=2, padx=5, fill='x')

        self.content_frame = ct.CTkFrame(self.main_frame)
        self.content_frame.pack(fill='both', expand=True)

        menu_icon = Image.open('icons/menu.png').resize((25, 25))
        self.menu_icon = ImageTk.PhotoImage(menu_icon)

        self.menu_button = ct.CTkButton(
            self.content_frame,
            image=self.menu_icon,
            width=30,
            height=30,
            command=self.toggle_menu,
            text='>',
            compound='left'
        )
        self.menu_button.grid(row=0, column=0, columnspan=5, sticky='nw', padx=5, pady=5)

        display_frame = ct.CTkFrame(self.content_frame, corner_radius=10)
        display_frame.grid(row=1, column=0, columnspan=5, pady=10, padx=5, sticky='nsew')

        self.history_display = ct.CTkLabel(
            display_frame,
            font=('Arial', 16),
            text='',
            height=40,
            anchor='e',
            textvariable=self.history_text
        )
        self.history_display.pack(fill='x', padx=5)

        self.display = ct.CTkLabel(
            display_frame,
            textvariable=self.result_var,
            font=('Arial', self.current_font),
            height=50,
            anchor='e'
        )
        self.display.pack(fill='x', pady=5, padx=5)

        buttons = [
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('/', 2, 3), ('(', 2, 4),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('*', 3, 3), (')', 3, 4),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('-', 4, 3), ('^2', 4, 4),
            ('0', 5, 0), ('.', 5, 1), ('=', 5, 2), ('+', 5, 3), ('√', 5, 4),
            ('C', 6, 0, 4), ('<', 6, 4)
        ]

        for button in buttons:
            text = button[0]
            row = button[1]
            col = button[2]
            colspan = button[3] if len(button) > 3 else 1

            btn = ct.CTkButton(
                self.content_frame,
                text=text,
                width=60 if colspan == 1 else 60 * colspan + 5 * (colspan - 1),
                height=50,
                font=('Arial', 18),
                command=lambda t=text: self.on_button_click(t)
            )
            btn.grid(row=row, column=col, columnspan=colspan, padx=2, pady=2, sticky='nsew')

        for i in range(5):
            self.content_frame.columnconfigure(i, weight=1)
        for i in range(7):
            self.content_frame.rowconfigure(i, weight=1)

    def on_button_click(self, text):
        if text == '=':
            try:
                result = str(eval(self.current_input))

                self.history_text.set(f'{self.current_input}={result}')
                d = {'v': self.current_input, 'result': f'{result}'}
                self.history_list.append(d)
                self.json_history_objects.upload_json(self.history_list)

                self.result_var.set(result)
                self.current_input = result
                self.history_list = self.json_history_objects.load_json()
            except:
                self.current_input = ''
                self.result_var.set('Ошибка')

        elif text == 'C':
            self.current_input = ''
            self.result_var.set('0')

        elif text == '<':
            self.current_input = self.current_input[:-1]
            self.result_var.set(self.current_input if self.current_input else '0')

        elif text == '√':
            try:
                res = str(math.sqrt(float(self.current_input)))
                self.result_var.set(res)
                self.current_input = res
            except:
                self.result_var.set('Ошибка')

        elif text == '^2':
            try:
                res = str(float(self.current_input) ** 2)
                self.result_var.set(res)
                self.current_input = res
            except:
                self.result_var.set('Ошибка')

        else:
            self.current_input += text
            self.result_var.set(self.current_input)

        # if len(self.current_input) > 18:
        #     self.display.configure(font=('Arial', 20))
        # else:
        #     self.display.configure(font=('Arial', 24))
