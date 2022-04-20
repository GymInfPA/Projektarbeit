import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from widgets.mytoolbar import MyNavigationToolbar2Tk


class PlotView():
    """Add a Frame with a canvas and a toolbar to the notebook."""
    def __init__(self, notebook: ttk.Notebook, title='PlotView'):
        self.notebook = notebook
        self.frame = ttk.Frame(self.notebook)
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.notebook.add(self.frame, text=title)

        self._fig = Figure(figsize=(10, 5), dpi=72)

        self.canvas = FigureCanvasTkAgg(self._fig, self.frame)
        self.toolbar = MyNavigationToolbar2Tk(
            self.canvas, self.frame, pack_toolbar=False)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.ax = self._fig.add_subplot(1, 1, 1)
        self.tab_index = self.notebook.tabs()[-1]
        self.notebook.select(self.tab_index)

    def clear(self):
        """Clear plot on canvas."""
        self._fig.clear()
        self.ax = self._fig.add_subplot(1, 1, 1)

    def show(self):
        """Show plot on canvas."""
        # Hinweise unter https://www.py4u.net/discuss/172516
        # items = self._toolbar.toolitems
        # print(items)
        self.canvas.draw()
        pass
