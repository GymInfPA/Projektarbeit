from controllers.plotcontroller import PlotController
from model.datacontainer import DataContainer
from widgets.statusbar import Statusbar
import os

class BoxplotsController(PlotController):
    """Show a boxplot of all attributes."""
    def __init__(self, model: DataContainer, notebook, status: Statusbar, name='Plot', parent=None, debug=True):
        self.dirty = False
        self._toolbar_modified = False
        super().__init__(model, notebook, status, name, parent, debug)

    def show(self):
        self._change_toolbar()

        self.model.df.boxplot(ax=self.view.ax)
        self.view.ax.set(title=f'Boxplots')

        # sns.heatmap(self.model.cormat(), annot=True,
        #             ax=self.view.ax, square=True)
        self.view.show()

    def on_select(self, event):
        if self._debug:
            print(f'BoxplotsController.on_select event [dirty={self.dirty}]')

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
            self.view.toolbar.new_tooltips()
            self._toolbar_modified = True
