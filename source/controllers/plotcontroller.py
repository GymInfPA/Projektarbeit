from abc import abstractmethod, ABC
from views.plotview import PlotView
from model.datacontainer import DataContainer
from widgets.statusbar import Statusbar

class PlotController(ABC):
    """Abstract base controller of a plot."""
    
    def __init__(self, model: DataContainer, notebook, status: Statusbar, name='Plot', parent=None, debug=True):
        self._debug = debug
        self.model = model
        self.notebook = notebook
        self.status = status
        self.name = name
        self.parent = parent
        self.view = PlotView(self.notebook, title=name)
        self._status_msg()
        self.show()

    @abstractmethod
    def show(self):
        pass

    def on_select(self, event):
        if self._debug:
            print('PlotController.on_select event')
        self._status_msg()

    def _status_msg(self):
        filename = self.model.filename
        self.status.set_text(f'Datenquelle: {filename}')
