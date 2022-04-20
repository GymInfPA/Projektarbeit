from controllers.plotcontroller import PlotController
from model.datacontainer import DataContainer
from widgets.statusbar import Statusbar
import os
import seaborn as sns

class BarplotController(PlotController):
    """Show a simple vertical bar plot of an attribute."""
    def __init__(self, model: DataContainer, notebook, status: Statusbar, name='Plot', parent=None, x_axis=None, debug=True):
        self.x_axis = x_axis
        self._toolbar_modified = False
        super().__init__(model, notebook, status, name, parent, debug)

    def show(self):
        self._change_toolbar()
        ax = sns.histplot(data=self.model.df, x=self.x_axis,
                          ax=self.view.ax, stat='frequency')
        self.view.ax.set(
            title=f'Histogramm von «{self.x_axis}»')

        # # labeling of data points
        # if self.with_text:
        #     keys = self.model.df[self.model.index_label()].to_list()
        #     xmin, xmax, ymin, ymax = self.view.ax.axis()
        #     dx = (xmax-xmin)*0.005
        #     dy = (ymax-ymin)*0.005
        #     i = 0
        #     for x, y in zip(self.model.df[self.x_axis], self.model.df[self.y_axis]):
        #         self.view.ax.text(x=x+dx, y=y+dy, s=keys[i])
        #         i += 1
        self._status_msg()

    def on_select(self, event):
        if self._debug:
            print('BarplotController.on_select event')

        self._status_msg()

    def _status_msg(self):
        filename = os.path.basename(self.model.filename)
        text = f'Datenquelle: {filename}'
        self.status.set_text(text)

    def _change_toolbar(self):
        if self._debug:
            print(self.view.toolbar.toolitems)
        if not self._toolbar_modified:
            self.view.toolbar.new_tooltips()
            self._toolbar_modified = True
