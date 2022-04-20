import tkinter as tk
from tkinter import ttk

class TreeviewToolTip:
    """
    Tooltip recipe from
    http://www.voidspace.org.uk/python/weblog/arch_d7_2006_07_01.shtml#e387

    copy & paste from matplotlib.backends._backend_tk.ToolTip und dann abgeändert.
    """
    @staticmethod
    def createToolTip(widget: ttk.Treeview, text):
        toolTip = TreeviewToolTip(widget, text)
        # def enter(event):
        #     toolTip.showtip(text)
        # def leave(event):
        #     toolTip.hidetip()

        def on_motion(event):
            toolTip.on_motion(event)

        def on_click(event):
            toolTip.on_click(event)
        widget.bind('<Motion>', on_motion)
        widget.bind('<Button-3>', on_click, add=True)
        # widget.bind('<Enter>', enter)
        # widget.bind('<Leave>', leave)

    def __init__(self, widget: ttk.Treeview, text):
        self.widget = widget
        self.tipwindow = None
        # self.id = None
        # self.x = self.y = 0
        self.text = text
        self._last_column = None

    def on_motion(self, event):
        if self.widget.identify_region(event.x, event.y) == 'heading':
            column = self.widget.identify_column(event.x)
            if column == '#0':
                self.hidetip()
            elif column != self._last_column:
                if self.tipwindow is not None:
                    self.hidetip()
                self._last_column = column
                self.showtip()
        else:
            self._last_column = None
            self.hidetip()

    def on_click(self, event=None):
        print(f'TreeviewTooltip_on_click [_last_column={self._last_column}]')
        self.hidetip()

    def showtip(self):
        """Display text in tooltip window."""
        if self.tipwindow or not self.text:
            return
        first_item = self.widget.get_children()[0]
        x, y, width, height = self.widget.bbox(first_item, self._last_column)
        x = x + self.widget.winfo_rootx() + 10
        y = y + self.widget.winfo_rooty() - 5
        # if tooltip is outside master window, then right adjust tooltip
        master = self.widget.master
        if master.winfo_rootx()+master.winfo_width() < x+160:
            x = master.winfo_rootx()+master.winfo_width()-160

        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        try:
            # For Mac OS
            tw.tk.call("::tk::unsupported::MacWindowStyle",
                       "style", tw._w,
                       "help", "noActivates")
        except tk.TclError:
            pass
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                         relief=tk.SOLID, borderwidth=1)
        label.pack(ipadx=1)

    def hidetip(self):
        self._last_column = None
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()
