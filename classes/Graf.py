import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy


class Graf:
    def __init__(self, frame, x, function):
        self.frame = frame
        self.x = x
        self.function = function
        self.draw()

    def draw(self):
        try:
            y = eval(self.function, {'__builtins__': None}, {
                'x': self.x, 'sin': numpy.sin, 'cos': numpy.cos, 'tan': numpy.tan, 'sqrt': numpy.sqrt, 'log': numpy.log,
                'pi': numpy.pi, '^': numpy.pow
            })
        except Exception as e:
            # self.result_var.set(f'Ошибка: {e}')
            return

        for widget in self.frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(5, 3), dpi=100)
        ax.plot(self.x, y)
        ax.grid()
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title(self.function)

        canvas = FigureCanvasTkAgg(fig, master=self.frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side='top', fill='both', expand=True)
