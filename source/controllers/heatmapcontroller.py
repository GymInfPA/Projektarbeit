from controllers.plotcontroller import PlotController
from model.datacontainer import DataContainer
from widgets.statusbar import Statusbar
from widgets.mytoolbar import NavigationToolbarButtons
import seaborn as sns
import os


class HeatmapController(PlotController):
    """Show a heatmap of all pairs of attributes."""
    def __init__(self, model: DataContainer, notebook, status: Statusbar, name='Plot', parent=None, debug=True):
        self.dirty = False
        self._toolbar_modified = False
        super().__init__(model, notebook, status, name, parent, debug)

    def show(self):
        self._change_toolbar()
        sns.heatmap(self.model.cormat(), annot=True,
                    ax=self.view.ax, square=True)
        self.view.show()

    def on_select(self, event):
        if self._debug:
            print(f'HeatmapController.on_select event [dirty={self.dirty}]')

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
            self._toolbar_modified = True
