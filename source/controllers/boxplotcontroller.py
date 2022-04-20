from controllers.plotcontroller import PlotController
from model.datacontainer import DataContainer
from widgets.statusbar import Statusbar
from widgets.mytoolbar import NavigationToolbarButtons
import os

class BoxplotController(PlotController):
    """Show the barplot of an attribute with additional information on mouse hover."""
    def __init__(self, model: DataContainer, notebook, status: Statusbar, name='Plot', parent=None, column=[], debug=True):
        self.dirty = False
        self._toolbar_modified = False
        self.column = column
        super().__init__(model, notebook, status, name, parent, debug)

    def show(self):
        self._change_toolbar()
        data = self.model.df[self.column]

        # matplotlib.boxplot
        # Daten des boxplots, Quelle: https://www.tutorialspoint.com/how-to-get-boxplot-data-for-matplotlib-boxplots
        # Versuche allenfalls auch 'PickEvent' oder dann mit dem sns.swarmplot
        # PickEvent Beispiel: https://stackoverflow.com/questions/59899108/how-do-you-increase-the-pickradius-of-a-matplotlib-line2d-artist
        self.boxplot = self.view.ax.boxplot(
            data, meanline=True, showmeans=True)
        # self.view.canvas.mpl_connect('pick_event',self.on_pick)

        # # pandas.DataFrame.boxplot
        # self.model.df.boxplot(column=self.column,ax=self.view.ax)

        # # Seaborn boxplot
        # ax = self.boxplot = sns.boxplot(y=self.column, data=self.model.df,orient='v', ax=self.view.ax, width=0.5, showmeans=True, meanline=True)
        # ax2 = sns.swarmplot(y=self.column, data=self.model.df,orient='v', ax=ax, color='0.25')

        # Hide xticks
        # Quelle: https://www.geeksforgeeks.org/how-to-hide-axis-text-ticks-or-tick-labels-in-matplotlib/
        xax = self.view.ax.get_xaxis().set_visible(False)
        self.view.ax.set(title=f'Boxplot von "{self.column}"')
        self.view.show()

    def on_select(self, event):
        if self._debug:
            print(f'BoxplotController.on_select event [dirty={self.dirty}]')

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
            ntb = NavigationToolbarButtons
            self.view.toolbar.disable_button(
                [ntb.BACK, ntb.FORWARD, ntb.PAN, ntb.ZOOM])
            self.view.toolbar.set_on_mouse_move(self.mouse_move)
            self._toolbar_modified = True

    # def on_pick(self, event=None):
    #     if self._debug:
    #         print(f'BoxplotController_on_pick. Event={event}')

    def mouse_move(self, event):
        if self._debug:
            print(f'BoxplotMouseMoveEvent: {event}')
        ax = event.inaxes
        if ax is not None:
            stop = False
            for e in self.boxplot['fliers']:
                b, d = e.contains(event)
                if b:
                    idx = d['ind'][0]
                    value = e.get_ydata()[idx]
                    data = self.model.df[self.model.df[self.column] == value]
                    msg = f'Ausreisser:  Key: {data.iat[0,0]} - Wert: {data.iloc[0][self.column]:g}'
                    stop = True
            if not stop:
                for e in self.boxplot['means']:
                    b, d = e.contains(event)
                    if b:
                        idx = d['ind'][0]
                        value = e.get_ydata()[idx]
                        data = self.model.df[self.model.df[self.column] == value]
                        msg = f'Mittelwert: {value:g}'
                        stop = True
            if not stop:
                for e in self.boxplot['medians']:
                    b, d = e.contains(event)
                    if b:
                        idx = d['ind'][0]
                        value = e.get_ydata()[idx]
                        data = self.model.df[self.model.df[self.column] == value]
                        if data.empty:
                            msg = f'Median: {value:g}'
                        else:
                            msg = f'Median:  Key: {data.iat[0,0]} - Wert: {data.iloc[0][self.column]:g}'
                        stop = True
            if not stop:
                for e in self.boxplot['caps']:
                    b, d = e.contains(event)
                    if b:
                        median = self.model.df[self.column].median()
                        idx = d['ind'][0]
                        value = e.get_ydata()[idx]
                        data = self.model.df[self.model.df[self.column] == value]
                        if value < median:
                            msg = f'Kleinster normaler Wert: Key: {data.iat[0,0]} - Wert: {data.iloc[0][self.column]:g}'
                        else:
                            msg = f'Grösster normaler Wert: Key: {data.iat[0,0]} - Wert: {data.iloc[0][self.column]:g}'
                        stop = True
            if not stop:
                for e in self.boxplot['boxes']:
                    b, d = e.contains(event)
                    if b:
                        idx = d['ind'][0]
                        value = e.get_ydata()[idx]
                        data = self.model.df[self.model.df[self.column] == value]
                        if idx == 0:
                            if data.empty:
                                msg = f'1. Quartil: {value:g}'
                            else:
                                msg = f'1. Quartil: {data.iat[0,0]} - Wert: {data.iloc[0][self.column]:g}'
                        elif idx == 2:
                            if data.empty:
                                msg = f'3. Quartil: {value:g}'
                            else:
                                msg = f'3. Quartil: {data.iat[0,0]} - Wert: {data.iloc[0][self.column]:g}'
                        stop = True
            if not stop:
                msg = ''  # 'keine Boxplot Element'
        else:
            msg = ''  # '(ausserhalb der Grafik)'

        self.view.toolbar.set_message(msg)
