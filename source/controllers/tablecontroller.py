from abc import abstractmethod, ABC
from model.datacontainer import DataContainer
from views.dataview import DataView
from widgets.statusbar import Statusbar

class TableController(ABC):
    """Basic Controller for Tabular Data."""

    def __init__(self, model: DataContainer, notebook, status: Statusbar, name='Data', debug=True):
        self._debug = debug
        self.model = model
        self.notebook = notebook
        self.status = status
        self.name = name
        self.view = DataView(self.notebook, title=name)
        self._populate_view(model)
        self._status_msg()

    @abstractmethod
    def _populate_view(self, model):
        pass

    def on_select(self, event):
        if self._debug:
            print('TableController.on_select event')

        self._status_msg()

    def _status_msg(self):
        n_of_rows, n_of_cols = self.model.get_dimension()
        self.status.set_text(
            f'{n_of_rows} Zeilen x {n_of_cols} Spalten + Key-Spalte')
