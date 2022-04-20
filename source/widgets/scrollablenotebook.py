# -*- coding: utf-8 -*-

# Copyright (c) Muhammet Emin TURGUT 2020
# For license see LICENSE
# Quelle: https://github.com/muhammeteminturgut/ttkScrollableNotebook (22.11.2021)
#
# Close Button von: https://stackoverflow.com/questions/39458337/is-there-a-way-to-add-close-buttons-to-tabs-in-tkinter-ttk-notebook
# Close Symbol: \u2715
from tkinter import *
from tkinter import ttk

class ScrollableNotebook(ttk.Frame):
    """Notebook widget with scroll functionality and close button on each tab.
    
    Source is https://github.com/muhammeteminturgut/ttkScrollableNotebook (22.11.2021)
    Source for close button functionalty: https://stackoverflow.com/questions/39458337/is-there-a-way-to-add-close-buttons-to-tabs-in-tkinter-ttk-notebook
    """

    # Close Button
    __initialized = False

    def __init__(self,parent,wheelscroll=False,tabmenu=False,debug=True,*args,**kwargs):
        ttk.Frame.__init__(self, parent, *args)
        self._debug = debug

        # Close button
        if not ScrollableNotebook.__initialized:
            self.__initialize_custom_style()
            ScrollableNotebook.__initialized = True

        kwargs["style"] = "ScrollableNotebook"
        # ttk.Notebook.__init__(self, *args, **kwargs)
        self._active = None
        # END: Close Button

        self.xLocation = 0
        self.notebookContent = ttk.Notebook(self,**kwargs)
        self.notebookContent.pack(fill="both", expand=True)
        self.notebookTab = ttk.Notebook(self,**kwargs)
        self.notebookTab.bind("<<NotebookTabChanged>>",self._tabChanger)
        # Close Button
        self.notebookTab.bind("<ButtonPress-1>", self.on_close_press, True)
        self.notebookTab.bind("<ButtonRelease-1>", self.on_close_release)
        # END Close Button

        if wheelscroll==True:
            # Windows
            self.notebookTab.bind("<MouseWheel>", self._wheelscroll)
            # Linux
            self.notebookTab.bind("<Button-4>", self._wheelscroll)
            self.notebookTab.bind("<Button-5>", self._wheelscroll)
        slideFrame = ttk.Frame(self)
        slideFrame.place(relx=1.0, x=0, y=1, anchor=NE)
        self.menuSpace=30
        if tabmenu==True:
            self.menuSpace=50
            bottomTab = ttk.Label(slideFrame, text=" \u2630 ")
            bottomTab.bind("<1>",self._bottomMenu)
            bottomTab.pack(side=RIGHT)
        leftArrow = ttk.Label(slideFrame, text=" \u276E")
        leftArrow.bind("<1>",self._leftSlide)
        leftArrow.pack(side=LEFT)
        rightArrow = ttk.Label(slideFrame, text=" \u276F")
        rightArrow.bind("<1>",self._rightSlide)
        rightArrow.pack(side=RIGHT)
        self.notebookContent.bind("<Configure>", self._resetSlide)

    # START: Close button
    def on_close_press(self, event):
        """Called when the button is pressed over the close button"""

        element = self.identify(event.x, event.y)

        if "close" in element:
            if self._debug:
                print(f'close pressed in element: {element} of tab: {self._active}')
            index = self.index("@%d,%d" % (event.x, event.y))
            if index > 0:
                self.state(['pressed'])
                self._active = index
            return "break"

    def on_close_release(self, event):
        """Called when the button is released"""
        if not self.instate(['pressed']):
            return

        element =  self.identify(event.x, event.y)
        if self._debug:
            print(f'close released in element: {element} of tab: {self._active}')

        if "close" not in element:
            # user moved the mouse off of the close button
            return

        index = self.index("@%d,%d" % (event.x, event.y))

        if self._active == index:
            if 'text' in self.notebookTab.tab(index):
                key = self.notebookTab.tab(index)['text']
            else:
                key = None
            self.forget(index)
            self.event_generate("<<NotebookTabClosed>>", data=key)

        self.state(["!pressed"])
        self._active = None

    def __initialize_custom_style(self):
        style = ttk.Style()
        self.images = (
            PhotoImage("img_close", data='''
                R0lGODlhCAAIAMIBAAAAADs7O4+Pj9nZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
                '''),
            PhotoImage("img_closeactive", data='''
                R0lGODlhCAAIAMIEAAAAAP/SAP/bNNnZ2cbGxsbGxsbGxsbGxiH5BAEKAAQALAAA
                AAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU5kEJADs=
                '''),
            PhotoImage("img_closepressed", data='''
                R0lGODlhCAAIAMIEAAAAAOUqKv9mZtnZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
            ''')
        )
        self.images2 = (
            PhotoImage("img_close2", data='''
                iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QA/wD/AP+g
                vaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH5QseEQQwEhoNwwAAAHJJ
                REFUOMvNk7ENwCAMBK9khXQMQwEdA2YQJovSJY0jURiwlQZLVP47IVuG3er4kynA
                BeQJnCVTtGYAGnAPJFl6TbJ4JCZ4JHHBmsQNf1WBR171wv23Z4NdwsGwHdOqTJK0
                GFgvSZogAudi2kEycZ/rewG4Eya/YvUq+wAAAABJRU5ErkJggg==
                '''),
            PhotoImage("img_closeactive2", data='''
                iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QA/wD/AP+g
                vaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH5QseEQoWXpSlsAAAAIhJ
                REFUOMulkcsJgDAQBQfBHtKDJ23HcizAq914sgPBcuLliYr57OI7hWRnCPvgTos9
                n9kR2IFggINmR4BGlz3QAWtFEjTTiXllBiJwZCRBb1GzyeQkJjgnccEpiRu+sgiM
                Orvy/HZpsVV4NrRjqsokqW27KLFWlZVsjqouyfa8HIDJ0dIk5n9OoUs5uzWXBeUA
                AAAASUVORK5CYII=
                '''),
            PhotoImage("img_closepressed2", data='''
                iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QA/wD/AP+g
                vaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH5QseEQ809oMQEQAAALdJ
                REFUOMuNkbENwkAMRZ+QmIDGA6RGIjswBStFup6aHRgAZYRISJRpE1JTHY1POZkj
                Z0suLPs/W/6wxl7TEz+zF2AEnoBUxKJzo+oA6ICo+dqAiPbTbJdfMFUgVnwH2Gnz
                BByAt9YN8MggonWTAQd7XlDybC45ms1RZ4tRgny8YgtZjNAlTnEtiBeHxcVvR6fF
                m+LZA5E/3w4eiFSsqkJ6x7dLkD41z5ltwWHxBNyA1l7g8Tnk27+WAG6pWVGqwgAA
                AABJRU5ErkJggg==
            ''')
        )
        self.images3 = (
            PhotoImage("img_close3", data='''
                iVBORw0KGgoAAAANSUhEUgAAAAwAAAAMCAYAAABWdVznAAAABmJLR0QA/wD/AP+g
                vaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH5QwBBh4LsA8wEAAAACdJ
                REFUKM9jYCAeMDIwMDCwkKphFAwogMcBEwmRwkxq5DEyMDAwAAARKQAQEZj9aAAA
                AABJRU5ErkJggg==
                '''),
            PhotoImage("img_closeactive3", data='''
                iVBORw0KGgoAAAANSUhEUgAAAAwAAAAMCAYAAABWdVznAAAABmJLR0QA/wD/AP+g
                vaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH5QwBBh0i2ZD7vwAAAJJJ
                REFUKM+F0MEJg0AUhOHP4E2QnNKKfUTQc6rJTZuwDItILzkpCLk8wSSrDjx2d2Ye
                LD9kuCG3rzw6GZR4oT9Y6KNTrkaLBUOiPETW/gaPCLr4Qh73JbIvZXE2mPCMmcLb
                dv5U4x1T/4aXBI1q865O6Okw4x4zh5fUSqPZeE2K3iGNBD1XjDs0tvTG6ILCuQr4
                AMZ0H3Ei7MzHAAAAAElFTkSuQmCC
                '''),
            PhotoImage("img_closepressed3", data='''
                iVBORw0KGgoAAAANSUhEUgAAAAwAAAAMCAYAAABWdVznAAAABmJLR0QA/wD/AP+g
                vaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH5QwBBh44D99RBgAAAL9J
                REFUKM990TFqAlEUheEvGC0EIwimsLLKQiwE1+F+DKR2AYJNUgXBDNiIS3AHglho
                J+I4ae7AOIweuM07/33vcF4NL3hHF0fVekUfV2hhjQzjBwuf4X9BE/M4OFcszcI7
                4APesMIJtzBHESO/OcNfpAEdJEgjZ4ZpAV4Gc6c6FvFKWoB/w6tUE9sCnGHgiSYl
                +PKsvVkB/I5JI+Jde+U2lmjEJKX2htDG5kEbeXs37PKP62KPn7i1rEZ4R/T+AYXo
                QnJFRJ5hAAAAAElFTkSuQmCC
            ''')
        )


        style.element_create("close", "image", "img_close3",
                            ("active", "pressed", "!disabled", "img_closepressed3"),
                            ("active", "!disabled", "img_closeactive3"), border=8, sticky='')
        style.layout("ScrollableNotebook", [("ScrollableNotebook.client", {"sticky": "nswe"})])
        style.layout("ScrollableNotebook.Tab", [
                ("ScrollableNotebook.tab", {
                    "sticky": "nswe",
                    "children": [
                        ("ScrollableNotebook.padding", {
                            "side": "top",
                            "sticky": "nswe",
                            "children": [
                                ("ScrollableNotebook.focus", {
                                    "side": "top",
                                    "sticky": "nswe",
                                    "children": [
                                        ("ScrollableNotebook.label", {"side": "left", "sticky": ''}),
                                        ("ScrollableNotebook.close", {"side": "left", "sticky": ''}),
                                    ]
                            })
                        ]
                    })
                ]
            })
        ])
    # END: Close Button

    def _wheelscroll(self, event):
        if self._debug:
            print(f'_wheelscroll - event: {event}')

        if event.delta > 0 or event.num==4:
            self._leftSlide(event)
        else:
            self._rightSlide(event)

    def _bottomMenu(self,event):
        tabListMenu = Menu(self, tearoff = 0)
        for tab in self.notebookTab.tabs():
            tabListMenu.add_command(label=self.notebookTab.tab(tab, option="text"),command= lambda temp=tab: self.select(temp))
        try: 
            tabListMenu.tk_popup(event.x_root, event.y_root) 
        finally: 
            tabListMenu.grab_release()

    def _tabChanger(self,event):
        if self._debug:
            print(f'_tabChanger - event: {event}')
            
        try: self.notebookContent.select(self.notebookTab.index("current"))
        except: pass

    def _rightSlide(self,event):
        if self.notebookTab.winfo_width()>self.notebookContent.winfo_width()-self.menuSpace:
            if (self.notebookContent.winfo_width()-(self.notebookTab.winfo_width()+self.notebookTab.winfo_x()))<=self.menuSpace+5:
                self.xLocation-=20
                self.notebookTab.place(x=self.xLocation,y=0)
    def _leftSlide(self,event):
        if not self.notebookTab.winfo_x()== 0:
            self.xLocation+=20
            self.notebookTab.place(x=self.xLocation,y=0)

    def _resetSlide(self,event=None):
        if self._debug:
            print(f'_resetSlide - event: {event}')

        self.notebookTab.place(x=0,y=0)
        self.xLocation = 0

    def add(self,frame,**kwargs):
        """Add frame as new tab in notebook."""
        if len(self.notebookTab.winfo_children())!=0:
            self.notebookContent.add(frame, text="",state="hidden")
        else:
            self.notebookContent.add(frame, text="")
        # if 'text' in kwargs:
        #     kwargs["text"] = f'{kwargs["text"]} \u2715'
        self.notebookTab.add(ttk.Frame(self.notebookTab),**kwargs)

    def forget(self,tab_id):
        """Forget tab of notebook."""
        self.notebookContent.forget(self.__ContentTabID(tab_id))
        self.notebookTab.forget(tab_id)

    def hide(self,tab_id):
        """Hide tab."""
        self.notebookContent.hide(self.__ContentTabID(tab_id))
        self.notebookTab.hide(tab_id)

    def identify(self,x, y):
        """Return id of tab."""
        return self.notebookTab.identify(x,y)

    def index(self,tab_id):
        """Return index of tab."""
        return self.notebookTab.index(tab_id)

    def __ContentTabID(self,tab_id):
        # return self.notebookContent.tabs()[self.notebookTab.tabs().index(tab_id)]
        return tab_id

    def insert(self,pos,frame, **kwargs):
        """Insert a frame as new tab in notebook."""
        self.notebookContent.insert(pos,frame, **kwargs)
        self.notebookTab.insert(pos,frame,**kwargs)

    def select(self,tab_id):
        """Select tab of notebook."""
        # self.notebookContent.select(self.__ContentTabID(tab_id))
        self.notebookTab.select(tab_id)

    def tab(self,tab_id, option=None, **kwargs):
        """Return tab with given tab_id."""
        kwargs_Content = kwargs.copy()
        kwargs_Content["text"] = "" # important
        self.notebookContent.tab(self.__ContentTabID(tab_id), option=None, **kwargs_Content)
        return self.notebookTab.tab(tab_id, option=None, **kwargs)

    def tabs(self):
        """Return all tabs of notebook."""
        # return self.notebookContent.tabs()
        return self.notebookTab.tabs()

    def enable_traversal(self):
        """Enables traversal of tabs if there is no space for all of them."""
        self.notebookContent.enable_traversal()
        self.notebookTab.enable_traversal()
