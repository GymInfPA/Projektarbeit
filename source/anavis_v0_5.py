"""
Prototyp mit beispielhafter Funktionalität.

Analyse- und Visualisierungsapplikation
für Daten in tabellarischer Form (\*.csv)
wobei ein Tupel pro Zeile mit korrespondierenen Attributen
in derselben Spalte.
Es dürfen keine ungültigen oder fehlenden Werte enthalten sein.
Die erste Spalte enthält den Index (PrimaryKey), die erste Zeile die Attributbezeichnungen.

Zwei Datensätze sind integriert:

- Covid-19: Daten vom 06.10.21
- Meereis: Daten von 1979-2020

Statistische Funktionen:

- Standardisierung
- Statistische Kennzahlen

Auswertungen:

- Boxplot
- Einfache lineare Regression mit Korrelationsinformationen
- Streudiagramm
- Heatmap
- einfaches Säulendiagramm
"""

__version__ = '0.5'

import sys

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from widgets.scrollablenotebook import ScrollableNotebook       # schliessen ist \u2715

from widgets.statusbar import Statusbar
from controllers.menucontroller import MenuController


class App():
    """Application class.

    Define a window, add a menubar on top,
    empty notebook as main widget and finally a statusbar on the bottom.
    """

    def __init__(self, title='Tk'):
        # root = tix.Tk()
        root = tk.Tk()
        root.option_add('*tearOff', False)      # no line for menus

        self.root = root
        self.root.title(title)
        self.root.geometry("640x480")
        self.style = ttk.Style()
        self.style.theme_use('clam')
        # style1 = self.style.lookup('default', 'font')
        self.root.protocol('WM_DELETE_WINDOW', self.quit)
        # self.root.bind('<Escape>', quit)

        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        self.statusbar = Statusbar(self.root)
        self.statusbar.set_text()

        nb = ScrollableNotebook(self.root, wheelscroll=True, tabmenu=True)
        nb.pack(fill=tk.BOTH, expand=True)
        self.notebook = nb

        self.creat_menu()

    def quit(self):
        """Exit point - shows dialog ok-cancel"""
        if messagebox.askokcancel('Beenden', 'Soll das Programm wirklich beendet werden?'):
            self.root.quit()
            self.root.destroy()
            sys.exit()

    def creat_menu(self):
        """Defines all menu entries. Menubar is attached to the main window."""

        self.menu_controller = MenuController(
            self.root, self.notebook, self.statusbar)

        # File menu
        menu_file = tk.Menu(self.menubar)
        menu_file.add_command(
            label='Öffnen...', underline=0, command=self.menu_controller.on_open)
        menu_demo_daten = tk.Menu(menu_file)
        menu_demo_daten.add_command(label='Covid-19 Daten (06.10.21)', underline=0,
                                    command=self.menu_controller.on_load_covid)
        menu_demo_daten.add_command(label='Meereis-Daten (1979-2020)', underline=0,
                                    command=self.menu_controller.on_load_seaice)
        menu_file.add_cascade(
            label='Demodaten', menu=menu_demo_daten, underline=0)
        menu_file.add_separator()
        menu_file.add_command(label='Schliessen', underline=0,
                              command=self.menu_controller.on_close)
        menu_file.add_separator()
        menu_file.add_command(label='Beenden', underline=0,
                              command=self.menu_controller.on_exit)
        self.menubar.add_cascade(label='Datei', underline=0, menu=menu_file)

        # Analyse
        menu_analyse = tk.Menu(self.menubar)
        menu_analyse.add_command(
            label='Zusammenstellung', underline=0, command=self.menu_controller.on_overview)
        menu_analyse.add_separator()
        menu_analyse.add_command(
            label='Standardisierung', underline=0, command=self.menu_controller.on_normalize)
        self.menubar.add_cascade(
            label='Analyse', underline=0, menu=menu_analyse)

        # Plot
        menu_plot = tk.Menu(self.menubar)
        menu_plot.add_command(label='Übersicht', underline=0,
                              command=self.menu_controller.on_plot_overview)
        menu_plot.add_command(label='Heatmap', underline=0,
                              command=self.menu_controller.on_heatmap)
        menu_plot.add_command(label='Boxplots', underline=0,
                              command=self.menu_controller.on_boxplots)
        menu_plot.add_separator()
        menu_plot.add_command(label='Lineare Regression', underline=0,
                              command=self.menu_controller.on_linear_regression)
        self.menubar.add_cascade(label='Plot', underline=0, menu=menu_plot)

        # Hilfe
        menu_help = tk.Menu(self.menubar)
        menu_help.add_command(label='Hilfe', underline=0,
                              command=self.menu_controller.on_help)
        menu_help.add_separator()
        menu_help.add_command(label='Info', underline=0,
                              command=self.menu_controller.on_info)
        self.menubar.add_cascade(label='Hilfe', underline=0, menu=menu_help)

    def run(self):
        """Run the applications main loop."""

        self.root.mainloop()


if __name__ == '__main__':
    App('AnaVis v0.5').run()
