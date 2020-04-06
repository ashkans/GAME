# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 11:39:30 2020

@author: ashkans
"""
from tkinter import Tk, Button, Label, Entry


class QuestionGui(object):
    def __init__(self, title = None, resizable = True, geometry = None):
        if title is None:
            self.title = "Engineering Investigation"
        
        self.resizable = (0, 0) if not resizable else (1,1)
        
        if geometry is None:
            geometry = '600x350'
        self.geometry = geometry
        self.window = Tk()
        
        
    def equaly_weight(self):
        print(self.grid_size())
        gs = self.grid_size()
        for i in range(gs[1]):
            self.window.rowconfigure(i, weight=1)
        
        for j in range(gs[0]):
            self.window.columnconfigure(j, weight=1)
            
                
    def grid_size(self):
        return self.window.grid_size()
    
    def start(self):
        self.window.geometry(self.geometry)
        self.window.resizable(self.resizable[0], self.resizable[1])
        self.window.title(self.title)
        self.window.mainloop()
    
    def add_entry(self, default_value=None, column=0, row=0, **kwargs):
        ent = Entry(self.window, **kwargs)
        ent.grid(column=column, row=row)
        
        if default_value is not None:
            ent.delete(0, "end")
            ent.insert(0, default_value)
        return ent
    
    def add_text(self, column=0, row=0, **kwargs):
        txt = Label(self.window, **kwargs)
        txt.grid(column=column, row=row)
        return txt
    
    def add_button(self, column=0, row=0, **kwargs):
        btn = Button(self.window, **kwargs)
        btn.grid(column=column, row=row)
        return btn
        

if __name__ == '__main__':
    gui = QuestionGui()
    gui.start()
    