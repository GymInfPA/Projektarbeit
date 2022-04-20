import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

class NormalizeInputDialog(simpledialog.Dialog):
    """Input Dialog to collect information used by normalization.
    
    Args:
        items (list): attributes from which to select

    Returns:
        tuple (result, information)
        
        result (bool): True (ok), False (cancel)

        information (dict):

            'normal': attibute to normalize, i.e. mean=0,

            'scale': True: scales to standard deviation =1, False: no scaling

            'group_by': attibute for grouping, None: no grouping   
    """
    def __init__(self, parent, title='Dialog', items=[], selected_item=None):
        self.items = items
        self.selected_item = selected_item
        self.result = (False, {})
        super().__init__(parent, title=title)

    def body(self, master):
        """Define widgets of dialog."""
        # Normalisierung
        frame = tk.Frame(master)
        self.norm_label = tk.StringVar()
        tk.Label(frame, text='Normierung:').pack(side=tk.LEFT, padx=5, pady=5)
        self.cb_norm = ttk.Combobox(
            frame, textvariable=self.norm_label, state='readonly', width=30)
        self.cb_norm['values'] = self.items
        if self.selected_item:
            self.cb_norm.set(self.selected_item)
            self.cb_norm['state'] = 'disabled'
        self.cb_norm.pack(side=tk.LEFT, fill=tk.X, expand=True)
        frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # Skalierung
        frame = tk.Frame(master)
        self.scale = tk.BooleanVar(value=True)
        self.chk_scale = tk.Checkbutton(
            frame, text='Skalieren', variable=self.scale, onvalue=True, offvalue=False, command=self._on_cb_select)
        self.chk_scale.pack(side=tk.LEFT, padx=10, pady=5)
        frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # Gruppierung
        frame = tk.Frame(master)
        self.group = tk.BooleanVar(value=False)
        self.group_by = tk.StringVar(value=None)
        self.chk_group = tk.Checkbutton(
            frame, text='Gruppieren', variable=self.group, onvalue=True, offvalue=False, command=self._on_cb_select)
        self.chk_group.pack(side=tk.LEFT, padx=10, pady=5)
        self.cb_group_by = ttk.Combobox(
            frame, textvariable=self.group_by, state='disabled', width=30)
        self.cb_group_by['values'] = self.items
        self.cb_group_by.pack(side=tk.LEFT, fill=tk.X, expand=True)
        frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        return self.cb_norm

    def _on_cb_select(self):
        """Handles combobox state."""
        if self.group.get():
            self.cb_group_by.config(state='readonly')
        else:
            self.cb_group_by.config(state='disabled')

    def validate(self):
        """Invoked by superclass for input validation."""
        if len(self.norm_label.get()) == 0:
            msg = 'Bitte das zu normierende Attribut auswählen.'
            messagebox.showinfo('Eingabedaten', message=msg)
            self.cb_norm.focus_set()
            return False
        if self.group.get():
            if len(self.group_by.get()) == 0:
                msg = 'Bitte Attribut auswählen,\nnach dem gruppert werden soll.'
                messagebox.showinfo('Eingabedaten', message=msg)
                self.cb_group_by.focus_set()
                return False
        return True

    def apply(self):
        """Send inputs to caller and close dialog."""
        if self.group.get():
            group_by = self.group_by.get()
        else:
            group_by = None
        res_dict = {'normal': self.norm_label.get(),
                    'scale': self.scale.get(),
                    'group_by': group_by}
        self.result = (True, res_dict)
