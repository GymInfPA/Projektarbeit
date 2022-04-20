import tkinter as tk
from tkinter import ttk

class Statusbar(ttk.Frame):
    """Statusbar to show short information."""
    def __init__(self, master, relief=tk.SUNKEN, border=1, **kwargs):
        super().__init__(master=master, relief=relief, border=border, **kwargs)
        # self.config(relief=tk.SUNKEN,border=5)
        self.status_text = tk.StringVar()
        self.set_text('Status')
        self._status_label = ttk.Label(
            self, textvariable=self.status_text, anchor='e')
        self._status_label.pack(side=tk.LEFT)
        self.pack(side=tk.BOTTOM, fill=tk.X)

    def set_text(self, text='(Bitte zuerst Daten laden...)'):
        """Set a text in statusbar."""
        self.status_text.set(text)

    def get_text(self):
        """Return text in statusbar."""
        return self.status_text.get()
