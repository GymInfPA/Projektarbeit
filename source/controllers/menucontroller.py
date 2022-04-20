
import sys
import os
from tkinter import filedialog, messagebox
# sys.path.append('..')
from model.datacontainer import DataContainer
from controllers.datacontroller import DataController
from controllers.statisticcontroller import StatisticsController
from controllers.overviewcontroller import OverviewController
from controllers.heatmapcontroller import HeatmapController
from controllers.boxplotscontroller import BoxplotsController
from controllers.linregcontroller import LinRegController
from widgets.normalizedialog import NormalizeInputDialog
from widgets.linreginputdialog import LinRegInputDialog
from controllers.menuconst import MenuControllerConst


class MenuController():
    """Controls all menu commands.
    Acts as root controller."""

    def __init__(self, window=None, notebook=None, statusbar=None, debug=True):
        self._debug = debug
        self._parent = window
        self.notebook = notebook
        self.statusbar = statusbar
        self.data_controller = {}

        self._initial_dir = os.path.dirname(__file__)

    # file menu

    def on_open(self):
        """File Open..."""
        if self._debug:
            print('Open-File-Dialog')

        filepathname = filedialog.askopenfilename(parent=self._parent, title='Datendatei einlesen',
                                                  initialdir=self._initial_dir, filetypes=(('CSV', '*.csv'), ('Alle Dateien', '*.*')))
        if self._debug:
            print(f'filename: {filepathname}')

        if len(filepathname) > 0:
            filepath = os.path.dirname(filepathname)
            filename = os.path.basename(filepathname)
            self._open_file(filepath, filename)

    def on_load_covid(self):
        """File Open Covid Data."""
        if self._debug:
            print('Load Covid-Dataset')

        key = 'COVID19'
        filepath = os.path.join(self._initial_dir, '../data/')
        filename = 'COVID19Cases_vs_FullyVaccPersons_202139.csv'
        self._open_file(filepath, filename, key)

    def on_load_seaice(self):
        """File Open Seaice Data."""
        if self._debug:
            print('Load SeaIce-Dataset')

        key = 'SeaIce'
        filepath = os.path.join(self._initial_dir, '../data/')
        filename = 'SeaIce1979_2020.txt'
        self._open_file(filepath, filename, key)

    def _open_file(self, filepath, filename, key=None, error_msg='File not found.'):
        if key is None:
            key = filename

        if key in self.data_controller:
            self._select_controller(key)
        else:
            full_filename = os.path.join(filepath, filename)
            if os.path.isfile(full_filename):
                self._wait_state(wait=True)
                # empty nootebook
                self._clear_notebook()

                model = DataContainer(full_filename)
                controller = DataController(
                    model, self.notebook, self.statusbar, name=key, parent=self._parent)
                self.data_controller[key] = controller
                # self.notebook.bind('<<NotebookTabChanged>>', self._change_tab)
                self.notebook.notebookContent.bind(
                    '<<NotebookTabChanged>>', self._change_tab, add='+')
                # self.notebook.bind('<Button-3>', self.on_remove_controller)

                # Quelle: https://www.py4u.net/discuss/208298
                # should be:
                # self.notebook.bind('<<NotebookTabClosed>>', self.on_remove_controller)
                self._bind_event_data(
                    self.notebook, '<<NotebookTabClosed>>', self.on_remove_controller)
                self._wait_state(wait=False)

            else:
                messagebox.showerror('Open File error', error_msg)

    def on_close(self):
        """Close all notebook tabs."""
        if self._debug:
            print('close all tabs')

        self._clear_notebook()

    def on_exit(self):
        """Exit programm."""
        if self._debug:
            print('by by')

        self._parent.quit()

    # analyse menu
    def on_overview(self):
        """Invoke statistical Overview tab."""
        if self._debug:
            print('Statistische Übersicht')

        key = MenuControllerConst._STATISTICS
        data_key = list(self.data_controller.keys())[0]
        data_controller = self.data_controller[data_key]
        # if data_key+key in self.data_controller:
        if data_key+key in data_controller.subcontrollers:
            self._select_controller(data_key+key)
        else:
            self._wait_state(True)
            model = data_controller.model
            controller = StatisticsController(
                model, self.notebook, self.statusbar, data_key+key)
            data_controller.add_controller(controller)
            # self.data_controller[data_key+key] = controller
            self._wait_state()

    def on_normalize(self):
        """Open Normalize Dialog."""
        if self._debug:
            print('Standardisierung')

        data_key = list(self.data_controller.keys())[0]
        data_controller = self.data_controller[data_key]
        model = data_controller.model

        # Input Parameter
        labels = model.column_labels()
        dlg = NormalizeInputDialog(
            self._parent, title='Eingabedaten für die Standardisierung', items=labels)
        if dlg.result is not None:
            ok, arg_dict = dlg.result
            if ok:
                self._wait_state(wait=True)
                model.normalize_col(
                    col=arg_dict['normal'], scale=arg_dict['scale'], group_by=arg_dict['group_by'])
                data_controller.dirty = True
                data_controller.on_select(None)
                self._select_controller(data_key)
                for c in data_controller.subcontrollers:
                    data_controller.subcontrollers[c].dirty = True
                if self._debug:
                    print(f'Normalize Dialog Arguments:\n{arg_dict}')
                self._wait_state(wait=False)

    # plot menu
    def on_plot_overview(self):
        """Show scatter plot and bar plot of all attributes."""
        if self._debug:
            print('Plot overview')
            print(f'DataSet: {list(self.data_controller.keys())[0]}')
        key = MenuControllerConst._OVERVIEW
        data_key = list(self.data_controller.keys())[0]
        data_controller = self.data_controller[data_key]
        if data_key+key in data_controller.subcontrollers:
            self._select_controller(data_key+key)
        else:
            self._wait_state(wait=True)
            model = data_controller.model
            controller = OverviewController(
                model, self.notebook, self.statusbar, data_key+key, parent=data_controller)
            data_controller.add_controller(controller)
            self._wait_state(wait=False)

    def on_heatmap(self):
        """Show a heatmap of all pairs of attributes."""
        if self._debug:
            print('Heatmap')
            print(f'DataSet: {list(self.data_controller.keys())[0]}')
        key = MenuControllerConst._HEATMAP
        data_key = list(self.data_controller.keys())[0]
        data_controller = self.data_controller[data_key]
        if data_key+key in data_controller.subcontrollers:
            self._select_controller(data_key+key)
        else:
            self._wait_state(wait=True)
            model = data_controller.model
            controller = HeatmapController(
                model, self.notebook, self.statusbar, data_key+key, parent=data_controller)
            data_controller.add_controller(controller)
            self._wait_state(wait=False)

    def on_boxplots(self):
        """Show boxplot diagramm of all attributes."""
        if self._debug:
            print('Boxplots')
            print(f'DataSet: {list(self.data_controller.keys())[0]}')
        key = MenuControllerConst._BOXPLOTS
        data_key = list(self.data_controller.keys())[0]
        data_controller = self.data_controller[data_key]
        if data_key+key in data_controller.subcontrollers:
            self._select_controller(data_key+key)
        else:
            self._wait_state(wait=True)
            model = data_controller.model
            controller = BoxplotsController(
                model, self.notebook, self.statusbar, data_key+key, parent=data_controller)
            data_controller.add_controller(controller)
            self._wait_state(wait=False)

    def on_linear_regression(self):
        """Open Input dialog of linear regression."""
        if self._debug:
            print('Lineare Regression')
        key = MenuControllerConst._LINREG
        data_key = list(self.data_controller.keys())[0]
        data_controller = self.data_controller[data_key]
        if data_key+key in data_controller.subcontrollers:
            self._select_controller(data_key+key)
        else:
            model = data_controller.model

            # Input Parameter
            labels = model.column_labels()
            dlg = LinRegInputDialog(
                self._parent, title='Eingabedaten für die Lineare Korrelation', items=labels)
            if dlg.result is not None:
                ok, arg_dict = dlg.result
                if ok:
                    # effective Controller
                    self._wait_state(wait=True)
                    if not arg_dict['ci']:
                        # linear regression has allways a line
                        arg_dict['ci'] = 0
                    controller = LinRegController(
                        model, self.notebook, self.statusbar, name=data_key+key, parent=data_controller, x_axis=arg_dict['x_label'], y_axis=arg_dict['y_label'], with_text=arg_dict['with_text'], ci=arg_dict['ci'], size=arg_dict['size'])
                    data_controller.add_controller(controller)
                    self._wait_state(wait=False)

    # Info
    def on_help(self):
        """Show a messagebox with help information."""
        if self._debug:
            print('Is this a help?')
        msg = '''
        In der Begleitarbeit im Anhang A finden sich zwei Anwendungsbeispiele.

        Zwei Demodatensätze sind integriert:
        - Covid-19 Daten (06.10.21)
        - Meereis-Daten (1979-2020)
            
        Eine Beschreibung des Codes wurde mit sphinx erstellt.'''
        messagebox.showinfo(title='Hilfe', message=msg)

    def on_info(self):
        """Show a messagebox with general information."""
        if self._debug:
            print('Info')
        msg = 'AnaVis v0.5 (14.02.2022)'
        messagebox.showinfo(title='Info', message=msg)

    # Helper functions
    def _change_tab(self, event):
        if self._debug:
            print(f'_change_tab Event widget: {event.widget}')
            print(f'Event: {event}')
            data_key = list(self.data_controller.keys())[0]
            print(
                f'Controller: {self.data_controller.keys()}. Subs: {self.data_controller[data_key].subcontrollers}')

        self._wait_state(wait=True)
        # get selected tab
        # active_tab = self.notebook.index(self.notebook.select())
        active_tab = self.notebook.index('current')
        # find corresponding controller
        data_key = list(self.data_controller.keys())[0]
        data_controller = self.data_controller[data_key]
        if active_tab == 0:
            active_controller = data_controller
        else:
            active_controller = list(data_controller.subcontrollers.values())[
                active_tab-1]
        # throw controller.on_select(...)
        active_controller.on_select(event)
        self._wait_state(wait=False)

    def _wait_state(self, wait=False):
        if wait:
            self._parent.config(cursor='watch')
            self._parent.update()
            # self._parent.config(cursor='wait')
        else:
            self._parent.config(cursor='')
            # self._parent.config(cursor='')

        self._parent.update()

    def _clear_notebook(self):
        self.notebook.unbind('<<NotebookTabChanged>>')
        # self.notebook.unbind('<Button-3>')
        for i in range(len(self.notebook.tabs()), 0, -1):
            self.notebook.forget(i-1)
            for dc in self.data_controller.values():
                dc.subcontrollers = {}
            self.data_controller = {}
        self.statusbar.set_text()

    def _select_controller(self, key):
        # controller = self.data_controller[key]
        if key in self.data_controller:
            controller = self.data_controller[key]
        else:
            data_key = list(self.data_controller.keys())[0]
            data_controller = self.data_controller[data_key]
            controller = data_controller.subcontrollers[key]
        if self._debug:
            print(self.notebook.tabs())

        self.notebook.select(controller.view.tab_index)

    # Quelle: https://www.py4u.net/discuss/208298
    def _bind_event_data(self, widget, sequence, func, add=None):
        def _substitute(*args):
            def e(): return None  # simplest object with __dict__
            # e.data = eval(args[0])
            e.data = args[0]
            e.widget = widget
            return (e,)

        funcid = widget._register(func, _substitute, needcleanup=1)
        cmd = '{0}if {{"[{1} %d]" == "break"}} break\n'.format(
            '+' if add else '', funcid)
        widget.tk.call('bind', widget._w, sequence, cmd)

    def on_remove_controller(self, event):
        """Event handler to remove a tab of notebook."""
        if self._debug:
            print(
                f'MenuController_on_remove_controller - event.data:{event.data}')

        if event.data is not None:
            data_key = list(self.data_controller.keys())[0]
            if event.data == data_key:
                if self._debug:
                    print('Data Tab must not be removed. So clear everything.')
                # alles löschen
                self._clear_notebook()
                pass
            else:
                data_controller = self.data_controller[data_key]
                if event.data in data_controller.subcontrollers.keys():
                    data_controller.subcontrollers.pop(event.data)
                    if self._debug:
                        print(
                            f'Controller {event.data} removed from controller list')
                        print(
                            f'new contoller list: {self.data_controller.keys()}. Subs: {data_controller.subcontrollers.keys()}')

    # def on_remove_controller(self, event):
    #     if self._debug:
    #         print(f'MenuController_on_remove_controller - event:{event}')

    #     # Quelle: https://stackoverflow.com/questions/40828166/is-it-possible-to-bind-a-mouse-event-to-a-tab-of-a-notebook
    #     clicked_tab_idx = self.notebook.tk.call(
    #         self.notebook._w, "identify", "tab", event.x, event.y)
    #     if self._debug:
    #         print(
    #             f'on_remove_controller: {event.widget}. tab_idx: "{clicked_tab_idx}". type: {type(clicked_tab_idx)}')
    #     if isinstance(clicked_tab_idx, int):
    #         clicked_tab = self.notebook.tabs()[clicked_tab_idx]
    #         if clicked_tab_idx > 0:
    #             data_key = list(self.data_controller.keys())[0]
    #             data_controller = self.data_controller[data_key]
    #             for key, c in data_controller.subcontrollers.items():
    #                 if clicked_tab == c.view.tab_index:
    #                     self.notebook.forget(clicked_tab)
    #                     data_controller.subcontrollers.pop(key)
    #                     if self._debug:
    #                         print(
    #                             f'Controller {key} removed from controller list')
    #                         print(
    #                             f'new contoller list: {self.data_controller.keys()}. Subs: {data_controller.subcontrollers.keys()}')
    #                     break
    #         else:
    #             if self._debug:
    #                 print('Data Tab must not be removed.')
    #     else:
    #         if self._debug:
    #             print('No tab clicked')
