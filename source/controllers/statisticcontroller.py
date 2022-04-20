from controllers.tablecontroller import TableController
from model.datacontainer import DataContainer
from widgets.statusbar import Statusbar

class StatisticsController(TableController):
    """Controller for basic statitical information
     based on raw data."""

    def __init__(self, model: DataContainer, notebook, status: Statusbar, name='Data', debug=True):
        self.dirty = False
        super().__init__(model, notebook, status, name, debug)

    def _populate_view(self, model):
        self.view.create_columns('Beschreibung', model.column_labels())
        infos = self.model.descriptions()
        for row in infos:
            self.view.add_row(row[0], row[1:])

    def on_select(self, event):
        if self._debug:
            print(f'StatisticsController.on_select event [dirty={self.dirty}]')

        if self.dirty:
            self.refresh()

        self._status_msg()

    def _status_msg(self):
        n_of_rows, n_of_cols = self.model.get_dimension()
        self.status.set_text(
            f'Statistische Kennzahlen von {n_of_cols} Spalten')

    def refresh(self):
        self.view.refresh_tree()
        self._populate_view(self.model)
        self.dirty = False
