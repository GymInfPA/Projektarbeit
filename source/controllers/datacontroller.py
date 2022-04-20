from controllers.menuconst import MenuControllerConst
from controllers.tablecontroller import TableController
from controllers.boxplotcontroller import BoxplotController
from controllers.barplotcontroller import BarplotController
from model.datacontainer import DataContainer
from widgets.statusbar import Statusbar
from widgets.tooltip import TreeviewToolTip
from widgets.normalizedialog import NormalizeInputDialog
import tkinter as tk
from tkinter import messagebox


class DataController(TableController):
    """Controller for Raw Data."""

    def __init__(self, model: DataContainer, notebook, status: Statusbar, name='Data', parent=None, debug=True):
        self._parent = parent
        self.dirty = False
        self.current_column = None
        self.subcontrollers = {}
        super().__init__(model, notebook, status, name, debug)

    def _populate_view(self, model):
        self.view.create_columns(model.index_label(), model.column_labels())
        for row in self.model.get_all_rows():
            self.view.add_row(row[0], row[1:])
        # Muss vor den anderen bind stehen, damit Tooltip verschwindet, wenn etwas geklickt wird
        TreeviewToolTip.createToolTip(
            widget=self.view.tree, text='Click für Statistik\nRechtsclick für Kontextmenü')
        self.view.tree.bind('<Button-1>', self.on_click)
        self.view.tree.bind('<Button-3>', self.on_rightclick, add=True)

    def on_select(self, event):
        if self._debug:
            print(f'DataController.on_select event [dirty={self.dirty}]')
        if self.dirty:
            self.refresh()
        self._status_msg()

    def _status_msg(self, msg=None):
        if msg is None:
            n_of_rows, n_of_cols = self.model.get_dimension()
            msg = f'{n_of_rows} Zeilen x {n_of_cols} Spalten + Key-Spalte: "{self.model.index_label()}"'
        self.status.set_text(msg)

    def refresh(self):
        self.view.refresh_tree()
        self._populate_view(self.model)
        self.dirty = False

    def add_controller(self, controller):
        if self._debug:
            print(f'DataController_add_controller({controller.name})')

        self.subcontrollers[controller.name] = controller

    def on_click(self, event=None):
        if self._debug:
            print(f'DataController_on_click - event: {event}')
        if self.view.tree.identify_region(event.x, event.y) == 'heading':
            column = self.view.tree.identify_column(event.x)
            c_idx = int(column[1:])
            if c_idx > 0:
                self.current_column = column = self.model.column_labels()[
                    c_idx-1]
                msg = str(self.model._description(column).to_dict())[1:-1]
                msg = msg.replace(':', '\t').replace(', ', '\n')
                title = f'Statistik für «{column}»'
                messagebox.showinfo(title=title, message=msg)
            # if c_idx == 0:
            #     c_lbl = self.model.index_label()
            # else:
            #     c_lbl = self.model.column_labels()[c_idx-1]
            # print(f'DataController_on_click: {event} - column: {column}: "{c_lbl}"')

    # Kontextmenu nach https://stackoverflow.com/questions/12014210/tkinter-app-adding-a-right-click-context-menu
    # oder auch https://www.geeksforgeeks.org/right-click-menu-using-tkinter/
    def on_rightclick(self, event=None):
        if self._debug:
            print(f'DataController_on_rightclick - event: {event}')

        if self.view.tree.identify_region(event.x, event.y) == 'heading':
            column = self.view.tree.identify_column(event.x)
            c_idx = int(column[1:])
            if c_idx > 0:
                self.current_column = self.model.column_labels()[c_idx-1]
                m = tk.Menu(self.view.tree)
                if self.current_column in self.model.df.select_dtypes(include='number').columns.tolist():
                    # create numeric context menu
                    m.add_command(label='Standardisieren',
                                  command=self.on_normalize)
                    m.add_separator()
                    m.add_command(label='Boxplot', command=self.on_boxplot)
                    m.add_command(label='Histogramm',
                                  command=self.on_histogram)
                    m.add_separator()
                    m.add_command(label='Umbenennen',
                                  state='disabled', command=self.on_rename)
                else:
                    # create categorical context menu
                    m.add_command(label='Säulendiagramm',
                                  state='disabled', command=self.on_barplot)
                    m.add_separator()
                    m.add_command(label='Umbenennen',
                                  state='disabled', command=self.on_rename)

                try:
                    # m.post(event.x_root, event.y_root)
                    m.tk_popup(event.x_root, event.y_root)
                finally:
                    m.grab_release()

    def on_normalize(self, event=None):
        if self._debug:
            print(f'DataController_on_normalize. Event: {event}')

        title = f'Eingabedaten für die Standardisierung'
        items = self.model.column_labels()
        items.remove(self.current_column)

        dlg = NormalizeInputDialog(
            self._parent, title=title, items=items, selected_item=self.current_column)
        if dlg.result is not None:
            ok, arg_dict = dlg.result
            if ok:
                # self._wait_state(wait=True)
                self.model.normalize_col(
                    col=arg_dict['normal'], scale=arg_dict['scale'], group_by=arg_dict['group_by'])
                self.dirty = True
                for c in self.subcontrollers.values():
                    c.dirty = True
                # for c_key in MenuController.dynamic_controllers:
                #     if data_key+c_key in self.controllers:
                #         self.controllers[data_key+c_key].dirty = True
                self.on_select(None)
                if self._debug:
                    print(f'Normalize Dialog Arguments:\n{arg_dict}')
                # self._wait_state(wait=False)

    def on_rename(self, event=None):
        if self._debug:
            print(f'DataController_on_rename - wahrscheinlich komplex...')

        # ToDo
        # Umbenennen einer Datenspalte muss sicherstellen, dass
        # - die Namen vernünfig (Sonderzeichen) und eindeutig sind
        # - die Endungen _n bzw. _ns müssen angepasst werden
        # - verschiedene Views werden nicht mehr korrekten Namen haben
        # - ...

    def on_boxplot(self, event=None):
        if self._debug:
            print(f'DataController_on_boxplot for {self.current_column}')

        data_key = self.name
        key = f'{MenuControllerConst._BOXPLOT}-{self.current_column}'
        if data_key+key in self.subcontrollers:
            self.notebook.select(
                self.subcontrollers[data_key+key].view.tab_index)
        else:
            controller = BoxplotController(
                self.model, self.notebook, self.status, name=data_key+key, parent=self, column=self.current_column)
            self.add_controller(controller)

    def on_histogram(self, event=None):
        """for numerical data"""
        if self._debug:
            print(f'DataController_on_histogram for {self.current_column}')

        key = f'{MenuControllerConst._BARPLOT}-{self.current_column}'
        data_key = self.name
        if data_key+key in self.subcontrollers:
            self.notebook.select(
                self.subcontrollers[data_key+key].view.tab_index)
        else:
            controller = BarplotController(
                self.model, self.notebook, self.status, name=data_key+key, parent=self, x_axis=self.current_column)
            self.add_controller(controller)

    def on_barplot(self, event=None):
        """for categorical data"""
        if self._debug:
            print(f'DataController_on_barplot for {self.current_column}')

        pass
