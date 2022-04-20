from controllers.plotcontroller import PlotController
from controllers.linregcontroller import LinRegController
from controllers.barplotcontroller import BarplotController
from controllers.menuconst import MenuControllerConst
from model.datacontainer import DataContainer
from widgets.statusbar import Statusbar
from widgets.mytoolbar import NavigationToolbarButtons
from widgets.linreginputdialog import LinRegInputDialog
import os

class OverviewController(PlotController):
    """Show scatter plot of all pairs of attributes and a barplot of each single attribute."""
    def __init__(self, model: DataContainer, notebook, status: Statusbar, name='Plot', parent=None, debug=True):
        self.dirty = False
        self._toolbar_modified = False
        super().__init__(model, notebook, status, name, parent, debug)

    def show(self):
        self._change_toolbar()
        self.model.scatter_matrix(self.view.ax)
        self.view.canvas.mpl_connect(
            'button_press_event', self.on_double_click)
        self.view.show()

    def on_select(self, event):
        if self._debug:
            print(f'OverviewController.on_select event [dirty={self.dirty}]')

        if self.dirty:
            self.view.clear()
            self.show()
            self.dirty = False

        self._status_msg()

    def _status_msg(self):
        filename = os.path.basename(self.model.filename)
        self.status.set_text(f'Datenquelle: {filename}')

    def _change_toolbar(self):
        if self._debug:
            print(self.view.toolbar.toolitems)
        if not self._toolbar_modified:
            ntb = NavigationToolbarButtons
            self.view.toolbar.remove_button(
                [ntb.BACK, ntb.FORWARD, ntb.PAN, ntb.ZOOM])
            self.view.toolbar.new_tooltips()
            self.view.toolbar.set_on_mouse_move(self.mouse_move)
            self._toolbar_modified = True

    def mouse_move(self, event):
        if self._debug:
            print(f'OverviewMouseMoveEvent: {event}')
        ax = event.inaxes
        if ax is None:
            msg = ''
        else:
            x_label = ax.xaxis.label.get_text()
            y_label = ax.yaxis.label.get_text()
            if x_label == y_label:
                msg = f'Bar Plot "{ax.xaxis.label.get_text()}"'
            else:
                msg = f'Scatter Plot "{ax.xaxis.label.get_text()}" vs. "{ax.yaxis.label.get_text()}"'
        self.view.toolbar.set_message(msg)

    def on_double_click(self, event=None):
        if self._debug:
            print(f'Overview_on double_click: {event}')
        ax = event.inaxes
        if ax is None:
            msg = ''
        else:
            if event.dblclick:
                x_label = ax.xaxis.label.get_text()
                y_label = ax.yaxis.label.get_text()
                if x_label == y_label:
                    msg = f'Bar Plot "{ax.xaxis.label.get_text()}"'
                    self.bar_plot(x=x_label)
                else:
                    msg = f'Scatter Plot "{ax.xaxis.label.get_text()}" vs. "{ax.yaxis.label.get_text()}"'
                    self.scatter_plot(x=x_label, y=y_label)

                print(
                    f'Einzeldiagramm {msg} - DataController: {self.parent.name}')
                # messagebox.showinfo(title='Einzeldiagramm',message=msg)

    def scatter_plot(self, x=None, y=None):
        if self._debug:
            print(f'OverviewController - create scatterplot {x} vs. {y}')

        key = f'{MenuControllerConst._SCATTER}-{x}-{y}'
        data_key = self.parent.name
        if data_key+key in self.parent.subcontrollers:
            self.notebook.select(
                self.parent.subcontrollers[data_key+key].view.tab_index)
        else:
            dlg = LinRegInputDialog(
                self.notebook, title='Eingabedaten für Streudiagramm', items=[x, y], ci=None)
            if dlg.result is not None:
                ok, arg_dict = dlg.result
                if ok:
                    # effective Controller
                    # self._wait_state(wait=True)
                    controller = LinRegController(
                        self.model, self.notebook, self.status, name=data_key+key, parent=self.parent,
                        x_axis=arg_dict['x_label'], y_axis=arg_dict['y_label'], with_text=arg_dict['with_text'], ci=arg_dict['ci'], size=arg_dict['size'])
                    self.parent.add_controller(controller)
                    # self._wait_state(wait=False)

    def bar_plot(self, x=None, orientation='v'):
        if self._debug:
            print(
                f'OverviewController - creat barplot {x} orientation: {orientation}')

        key = f'{MenuControllerConst._BARPLOT}-{x}'
        data_key = self.parent.name
        if data_key+key in self.parent.subcontrollers:
            self.notebook.select(
                self.parent.subcontrollers[data_key+key].view.tab_index)
        else:
            controller = BarplotController(
                self.model, self.notebook, self.status, name=data_key+key, parent=self.parent, x_axis=x)
            self.parent.add_controller(controller)

