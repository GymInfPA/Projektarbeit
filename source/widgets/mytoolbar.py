import tkinter as tk
from matplotlib.backends._backend_tk import ToolTip
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk


# Quelle: https://stackoverflow.com/questions/68685881/how-to-add-an-edit-option-to-tkinter-matplotlib-navigation-toolbar
#
# ## Hinweise für Tooltips nicht verwendet, sondern andere Lösung gefunden via from matplotlib.backends._backend_tk import ToolTip
# ## Für Tooltips: https://stackoverflow.com/questions/3221956/how-do-i-display-tooltips-in-tkinter
# ## auch: https://towardsdatascience.com/tooltips-with-pythons-matplotlib-dcd8db758846


"""
Standard NavigationToolbar2Tk from matplotlib backend_tkagg
with german Tooltips and methods for customization.
"""
class MyNavigationToolbar2Tk(NavigationToolbar2Tk):
    def __init__(self, canvas, window, *, pack_toolbar=True):
        self._on_mouse_move = None
        super().__init__(canvas, window, pack_toolbar=pack_toolbar)

    def set_on_mouse_move(self, on_mouse_move_cb=None):
        """Register mouse move event handler."""
        self._on_mouse_move = on_mouse_move_cb

    def new_tooltips(self, tooltips: dict = {}):
        """German translation of tooltips."""
        if not tooltips:
            ntb = NavigationToolbarButtons
            tooltips = {
                ntb.HOME: 'Ursprüngliche Darstellung',
                ntb.BACK: 'Darstellung zurück',
                ntb.FORWARD: 'Darstellung vorwärts',
                ntb.PAN: 'Linke Maustaste zum Verschieben, rechte zum Zoomen\nx/y fixiert Achse, CTRL fixiert Verhältnis',
                ntb.ZOOM: 'Rechteckszoom\n(rechte Maustaste verkleinert)',
                ntb.SUBPLOTS: 'Darstellungseinstellungen',
                ntb.SAVE: 'Speichern'
            }
        for b, t in tooltips.items():
            self._set_tooltip(button=b, text=t)

    def _set_tooltip(self, button=None, text=''):
        """Set tooltips."""
        if button in self._buttons.keys():
            ToolTip.createToolTip(self._buttons[button], text)

    def mouse_move(self, event):
        """Handle mouse move event."""
        if self._on_mouse_move is not None:
            self._on_mouse_move(event)

    def remove_button(self, button_list=[]):
        """Remove given toolbar buttons."""
        for b in button_list:
            if b in self._buttons.keys():
                btn = self._buttons[b]
                self.children[btn._name].pack_forget()

    def disable_button(self, button_list=[]):
        """Disable given toolbar buttons."""
        for b in button_list:
            if b in self._buttons.keys():
                btn = self._buttons[b]
                self.children[btn._name]['state'] = tk.DISABLED


"""
Helper Class with Button names of NavigationToolbar.
"""
class NavigationToolbarButtons():
    # Standard names
    #
    # HOME = '!button'
    # BACK = '!button2'
    # FORWARD = '!button3'
    # PAN = '!checkbutton'
    # ZOOM = '!checkbutton2'
    # SUBPLOTS = '!button4'
    # SAVE = '!button5'

    # new names
    HOME = 'Home'
    BACK = 'Back'
    FORWARD = 'Forward'
    PAN = 'Pan'
    ZOOM = 'Zoom'
    SUBPLOTS = 'Subplots'
    SAVE = 'Save'
