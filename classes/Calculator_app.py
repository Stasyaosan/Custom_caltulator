import customtkinter as ct
from dotenv import load_dotenv
import os

load_dotenv()


class Calculator_app:
    def __init__(self, root):
        self.root = root
        self.root.title(os.getenv('title'))
        self.root.geometry(f'{os.getenv('width')}x{os.getenv('height')}')

        ct.set_appearance_mode(os.getenv('theme'))
        ct.set_default_color_theme(os.getenv('color_theme'))
        self.current_input = ''
        self.result_var = ct.StringVar(value='0')

        self.current_font = 24

        self.create_widgets()

        self.root.bind('<Key>', self.handle_key_press)

    def handle_key_press(self, event):
        key = event.char
        if key in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '+', '*', '/', '='):
            self.on_button_click(key)

    def create_widgets(self):
        display_frame = ct.CTkFrame(self.root, corner_radius=10)
        display_frame.pack(pady=10, padx=5, fill='x')
        self.display = ct.CTkLabel(
            display_frame,
            textvariable=self.result_var,
            font=('Arial', self.current_font),
            width=260,
            height=50,
            anchor='e'
        )
        self.display.pack(pady=5, padx=5)

        buttons = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2), ('/', 0, 3),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2), ('*', 1, 3),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2), ('-', 2, 3),
            ('0', 3, 0), ('.', 3, 1), ('=', 3, 2), ('+', 3, 3),
            ('C', 4, 0, 3), ('<', 4, 3)
        ]

        buttons_frame = ct.CTkFrame(self.root, corner_radius=10)
        buttons_frame.pack(pady=10, padx=5, fill='both', expand=True)

        for button in buttons:
            text = button[0]
            row = button[1]
            col = button[2]

            if len(button) == 4:
                colspan = button[3]
            else:
                colspan = 1

            if colspan == 1:
                width = 60
            else:
                width = 60 * colspan + 5 * (colspan - 1)

            btn = ct.CTkButton(
                buttons_frame,
                text=text,
                width=width,
                height=50,
                font=('Arial', 18),
                command=lambda t=text: self.on_button_click(t)
            )
            btn.grid(row=row, column=col, columnspan=colspan, padx=2, pady=2)

    def on_button_click(self, text):
        if text == '=':
            try:
                result = str(eval(self.current_input))
                self.result_var.set(result)
                self.current_input = result
            except:
                self.current_input = ''
                self.result_var.set('Некорректное выражение')

        elif text == 'C':
            self.current_input = ''
            self.result_var.set('0')

        elif text == '<':
            self.current_input = self.current_input[:-1]
            if self.current_input:
                self.result_var.set(self.current_input)
            else:
                self.result_var.set('0')

        elif text.isdigit() or text in ('-', '+', '*', '/'):
            self.current_input += text
            self.result_var.set(self.current_input)

        if len(self.current_input) > 18:
            self.display.configure(font=('Arial', self.current_font / 1.2))

        if len(self.current_input) <= 18:
            self.current_font = 24
            self.display.configure(font=('Arial', self.current_font))
