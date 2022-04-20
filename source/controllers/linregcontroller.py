from controllers.plotcontroller import PlotController
from model.datacontainer import DataContainer
from widgets.statusbar import Statusbar
import os
import seaborn as sns
from scipy import stats

class LinRegController(PlotController):
    """Show a simple linear regression of two attributes."""
    def __init__(self, model: DataContainer, notebook, status: Statusbar, name='Plot', parent=None, x_axis=None, y_axis=None, ci=None, with_text=False, size=None, debug=True):
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.with_text = with_text
        self.ci = ci
        self.size = None if size == 'None' else size
        if debug:
            print(f'LinReg: size={self.size}')
        self._reg_result = None
        self._toolbar_modified = False
        super().__init__(model, notebook, status, name, parent, debug)

    def show(self):
        self._change_toolbar()
        labels = self.model.column_labels()

        if self.ci is None:
            p = sns.scatterplot(x=self.x_axis, y=self.y_axis, size=self.size, sizes=(50,500),
                                data=self.model.df, ax=self.view.ax)
            self.view.ax.set(
                title=f'Streudiagramm «{self.x_axis}» vs. «{self.y_axis}»')
        else:
            p = sns.scatterplot(x=self.x_axis, y=self.y_axis, size=self.size, sizes=(50,500),
                                data=self.model.df, ax=self.view.ax)
            p = sns.regplot(x=self.x_axis, y=self.y_axis, scatter=False,
                            data=self.model.df, ax=self.view.ax, ci=self.ci)
            # x_data = p.get_lines()[0].get_xdata()
            # y_data = p.get_lines()[0].get_ydata()
            x_data = self.model.df[self.x_axis].to_list()
            y_data = self.model.df[self.y_axis].to_list()
            self._reg_result = stats.linregress(x_data, y_data)
            x_idx = labels.index(self.x_axis)
            y_idx = labels.index(self.y_axis)
            corr_coef = self.model.corr_coef(x_idx, y_idx)
            if self.ci==0:
                title = f'Lineare Regression «{self.x_axis}» vs. «{self.y_axis}» [r={corr_coef:.2f}]'
            else:
                title=f'Lineare Regression «{self.x_axis}» vs. «{self.y_axis}» [r={corr_coef:.2f}, ci={self.ci}%]'
            self.view.ax.set(title=title)

        # labeling of data points
        if self.with_text:
            keys = self.model.df[self.model.index_label()].to_list()
            xmin, xmax, ymin, ymax = self.view.ax.axis()
            dx = (xmax-xmin)*0.005
            dy = (ymax-ymin)*0.005
            i = 0
            for x, y in zip(self.model.df[self.x_axis], self.model.df[self.y_axis]):
                self.view.ax.text(x=x+dx, y=y+dy, s=keys[i])
                i += 1
        self._status_msg()

    def on_select(self, event):
        if self._debug:
            print('LinRegController.on_select event')

        self._status_msg()

    def _status_msg(self):
        if self._reg_result is None:
            filename = os.path.basename(self.model.filename)
            text = f'Datenquelle: {filename}'
        else:
            text = f'Regressionsgerade: y = {self._reg_result.slope:.3f} x + {self._reg_result.intercept:.3f}'
        self.status.set_text(text)

    def _change_toolbar(self):
        if self._debug:
            print(self.view.toolbar.toolitems)
        if not self._toolbar_modified:
            self.view.toolbar.new_tooltips()
            self._toolbar_modified = True
