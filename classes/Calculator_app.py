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

        self.result_var = ct.StringVar(value='0')

        self.create_widgets()

    def create_widgets(self):
        display_frame = ct.CTkFrame(self.root, corner_radius=10)
        display_frame.pack(pady=10, padx=5, fill='x')
        display = ct.CTkLabel(
            display_frame,
            textvariable=self.result_var,
            font=('Arial', 24),
            width=260,
            height=50,
            anchor='e'
        )
        display.pack(pady=5, padx=5)

        buttons = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2), ('/', 0, 3),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2), ('*', 1, 3),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2), ('-', 2, 3),
            ('0', 3, 0), ('.', 3, 1), ('=', 3, 2), ('+', 3, 3),
            ('C', 4, 0, 3), ('<', 4, 3)
        ]

        buttons_frame = ct.CTkFrame(self.root, corner_radius=10)
        buttons_frame.pack(pady=10, padx=5, fill='both', expand=True)
