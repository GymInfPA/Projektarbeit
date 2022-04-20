import tkinter as tk
from tkinter import ttk
from tkinter import font


class DataView():
    """Add a Frame with a Treeview and a scrollbar to the notebook."""
    def __init__(self, notebook: ttk.Notebook, title='DataView'):
        self.notebook = notebook
        self.frame = ttk.Frame(self.notebook)
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.notebook.add(self.frame, text=title)
        self._create_tree()
        # self.tab_idx = len(self.notebook.tabs())-1
        self.tab_index = self.notebook.tabs()[-1]
        # print(f'{self.tab_idx}: {self.tab_index}')
        self.notebook.select(self.tab_index)

    def _create_tree(self):
        """Create Treeview with horizontal and vertical scrollbar."""
        self.tree = ttk.Treeview(self.frame)
        self._vsb = ttk.Scrollbar(self.frame, orient='vertical',
                                  command=self.tree.yview)
        self._vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=self._vsb.set)
        self._hsb = ttk.Scrollbar(self.frame, orient='horizontal',
                                  command=self.tree.xview)
        self._hsb.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.configure(xscrollcommand=self._hsb.set)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self._hsb.bind('<Enter>', self._bind_mousewheel)
        self._hsb.bind('<Leave>', self._unbind_mousewheel)

    # Quelle: https://stackoverflow.com/questions/17355902/tkinter-binding-mousewheel-to-scrollbar
    def _bind_mousewheel(self, event):
        """Bind mousewheel to scrollbar."""
        # Windows
        self.tree.bind_all('<MouseWheel>', self._on_mousewheel)
        # Linux
        self.tree.bind_all('<Button-4>', self._on_mousewheel)
        self.tree.bind_all('<Button-5>', self._on_mousewheel)

    def _unbind_mousewheel(self, event):
        """Unbind mousewheel to scrollbar."""
        # Windows
        self.tree.unbind_all('<MouseWheel>')
        # Linux
        self.tree.unbind_all('<Button-4>')
        self.tree.unbind_all('<Button-5>')

    def _on_mousewheel(self, event):
        """Scroll Treeview with mousewheel."""
        if event.num == 5:
            delta = -120
        elif event.num == 4:
            delta = 120
        else:
            delta = event.delta
        val = -1*delta/6
        # print(f'Scrollbar MouseWheel value={val}')
        self.tree.xview_scroll(int(val), 'units')
    # END mousewheel

    def refresh_tree(self):
        """Refresh Treeview, i.g. if a column is added."""
        self.tree.pack_forget()
        self._hsb.pack_forget()
        self._vsb.pack_forget()
        self._create_tree()

    def create_columns(self, index_label, headers):
        """Create columns given column headers."""
        FACTOR = 1.1
        PADDING_X = 50
        cur_font = font.nametofont('TkHeadingFont')
        width = int(cur_font.measure(index_label)*FACTOR+PADDING_X)
        self.tree['columns'] = headers
        self.tree.heading('#0', text=index_label)
        self.tree.column('#0', minwidth=width)
        for i, h in enumerate(headers):
            width = int(cur_font.measure(h)*FACTOR+PADDING_X)
            col_id = f'#{i+1}'
            self.tree.heading(col_id, text=h)
            self.tree.column(col_id, width=width, stretch=tk.NO)

    def add_row(self, key, values):
        """Append a tuple to the Treeview."""
        try:
            self.tree.insert(
                '', 'end', iid=key, text=key, values=values)
        except Exception as e:
            print(e)

