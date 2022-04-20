import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

# Quelle: http://tkinter.programujte.com/tkinter-dialog-windows.htm
# und https://stackoverflow.com/questions/10057672/correct-way-to-implement-a-custom-popup-tkinter-dialog-box
class LinRegInputDialog(simpledialog.Dialog):
    """Input Dialog to collect information used by simple linear regression.
    
    Args:
        items (list): attributes from which to select.

        ci (float): percentage of confidence intervall or None.

    Returns:
        tuple (result, information)
        
        result (bool): True (ok), False (cancel).

        information (dict):

            'x_label': item selected as x-label,

            'y_label': item selected as y-label,

            'size': item selected as size or None,

            'with_text': True: dots get labled, False: no lables,

            'ci': chosen conficence intervall or None        
    """
    def __init__(self, parent, title='Dialog', items=[], ci=95):
        self.items = items
        self.ci = ci
        self.result = (False, {})
        super().__init__(parent, title=title)

    def body(self, master):
        """Define widgets of dialog."""
        # x-Achse
        frame = tk.Frame(master)
        tk.Label(frame, text='x-Achse:', width=10).pack(side=tk.LEFT)
        self.x_label = tk.StringVar()
        self.cb_x_label = ttk.Combobox(
            frame, textvariable=self.x_label, state='readonly', width=30)
        if len(self.items) == 2:
            self.cb_x_label['values'] = self.items[0]
            self.x_label.set(self.items[0])
        else:
            self.cb_x_label['values'] = self.items
        self.cb_x_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # y-Achse
        frame = tk.Frame(master)
        tk.Label(frame, text='y-Achse:', width=10).pack(side=tk.LEFT)
        self.y_label = tk.StringVar()
        self.cb_y_label = ttk.Combobox(
            frame, textvariable=self.y_label, state='readonly', width=30)
        if len(self.items) == 2:
            self.cb_y_label['values'] = self.items[1]
            self.y_label.set(self.items[1])
        else:
            self.cb_y_label['values'] = self.items
        self.cb_y_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        self.cb_y_label.bind('<<ComboboxSelected>>', self.on_select)
        self.cb_x_label.bind('<<ComboboxSelected>>', self.on_select)

        # size of data dots
        frame = tk.Frame(master)
        tk.Label(frame, text='Grösse:', width=10).pack(side=tk.LEFT)
        self.size_label = tk.StringVar(value='None')
        self.cb_size_label = ttk.Combobox(
            frame, textvariable=self.size_label, state='readonly', width=30)
        self.cb_size_label['values'] = ['None']+self.items
        self.cb_size_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # data labeling
        self.with_text = tk.BooleanVar(value=False)
        self.checkbox_text = tk.Checkbutton(
            master, text='Datenpunkte labeln', variable=self.with_text, onvalue=True, offvalue=False)
        self.checkbox_text.pack(side=tk.TOP, padx=10, pady=5)

        # confidence interval
        self.with_ci = tk.BooleanVar(value=(self.ci is not None))
        self.ci_var = tk.StringVar(value=self.ci)
        frame = tk.Frame(master)
        self.checkbox_ci = tk.Checkbutton(
            frame, text='Konfidenznieveau', variable=self.with_ci, onvalue=True, offvalue=False, command=self._on_cb_select)
        self.checkbox_ci.pack(side=tk.LEFT, padx=10, pady=5)
        # only predefined values in Spinbox
        ci_values = [i for i in range(50, 99)]
        ci_values.extend([f'{99+i/10:.2f}' for i in range(0, 10)])
        ci_values.extend([f'{99.9+i/100:.2f}' for i in range(1, 10)])
        self.sb_ci = ttk.Spinbox(
            frame, values=ci_values, textvariable=self.ci_var, wrap=False, state='readonly')
        self.sb_ci.pack(side=tk.LEFT, padx=5, pady=5)
        frame.pack(side=tk.TOP, padx=5, pady=5)

        return self.cb_x_label

    def _on_cb_select(self):
        """Handles combobox state."""
        if self.with_ci.get():
            self.sb_ci.config(state='normal')
            if len(self.ci_var.get()) == 0:
                self.ci_var.set(95)
        else:
            self.sb_ci.config(state='disabled')

    def buttonbox(self):
        """Return predefined buttonbox"""
        return super().buttonbox()
        # # Buttons
        # frame = ttk.Frame(self)
        # frame.pack(fill='both', expand=True)
        # self.ok_button =  ttk.Button(frame, text='OK',command=self.on_ok,state='disabled')
        # self.ok_button.pack(side=tk.LEFT)
        # ttk.Button(frame, text='Abbrechen',command=self.on_cancel).pack(side=tk.RIGHT)

        # # positioniere versetzt über das Master-Fensters
        # self.geometry('300x200+{}+{}'.format(master.winfo_rootx()+50,master.winfo_rooty()+50))
        # self.grab_set()             # dialog shoul be modal
        # self.wait_window(self)

    def on_select(self, event):
        """Handle combobox selection"""
        x_lbl = self.cb_x_label.get()
        y_lbl = self.cb_y_label.get()
        if x_lbl == y_lbl:
            msg = 'Die Labels für die Achsen müssen unterschiedlich sein.\n' \
                f'x-Label: {x_lbl}\n' \
                f'y-Label: {y_lbl}'
            messagebox.showerror('Eingabedaten', message=msg)
            # self.ok_button['state']='disabled'
        # else:
        #     print(f'x-Label: {x_lbl}\n' \
        #             f'y-Label: {y_lbl}')
        #     # if len(x_lbl)>0 and len(y_lbl)>0:
        #     #     self.ok_button['state']='normal'

    def validate(self):
        """Invoked by superclass for input validation."""
        x_lbl = self.cb_x_label.get()
        y_lbl = self.cb_y_label.get()
        if x_lbl == y_lbl:
            msg = 'Die Labels für die Achsen müssen unterschiedlich sein.\n' \
                f'x-Label: {x_lbl}\n' \
                f'y-Label: {y_lbl}'
            messagebox.showinfo('Eingabedaten', message=msg)
            # self.ok_button['state']='disabled'
            return False
        else:
            # print(f'x-Label: {x_lbl}\n' \
            #         f'y-Label: {y_lbl}')
            if len(x_lbl) > 0 and len(y_lbl) > 0:
                # self.ok_button['state']='normal'
                return True
            else:
                msg = 'Für beide Achsen muss je\nein anderes Merkmal ausgewählt werden.'
                messagebox.showinfo('Eingabedaten', message=msg)
                return False

    def apply(self):
        """Send inputs to caller and close dialog."""
        if self.with_ci.get():
            ci = float(self.ci_var.get())
        else:
            ci = None
        res_dict = {'x_label': self.cb_x_label.get(),
                    'y_label': self.cb_y_label.get(),
                    'size': self.cb_size_label.get(),
                    'with_text': self.with_text.get(),
                    'ci': ci}
        self.result = (True, res_dict)
