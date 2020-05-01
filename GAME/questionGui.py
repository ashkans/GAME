# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 11:39:30 2020

@author: ashkans
"""
from tkinter import Tk, Button, Label, Entry, messagebox, StringVar, OptionMenu
import yaml


class QuestionGui(object):
    def __init__(self, title = None, resizable = True, geometry = None):
        self.title = "Engineering Investigation" if title is None else title
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

    def add_dropDown(self, column=0, row=0, options = None, **kwargs):
        options = ['--'] if options is None else options
        variable = StringVar(self.window)
        variable.set(options[0]) # default value
        opt = OptionMenu(self.window, variable, *options)
        opt.grid(column=column, row=row)
        return opt    
    
    def add_button(self, column=0, row=0, **kwargs):
        btn = Button(self.window, **kwargs)
        btn.grid(column=column, row=row)
        return btn

    def add_details_bar(self, left=0, top=0):
        ''' This function, generates a 2 rows x 4 columns panel to get the 
        Assignment and question number and student ID.
        
        Parameters
        ----------
        left : TYPE, optional
            The location of the most left grid. The default is 0.
        top : TYPE, optional
            The location of the most top grid. The default is 0.

        Returns
        -------
        None.

        '''
        self.details = {}
        self.details['aid_label'] = self.add_text(column=left, row=top, text='Assignment number',  font=("Arial Bold", 10))
        self.details['aid'] = self.add_entry(column=left+1, row=top, width=20, justify="center", default_value = "1")
        
        self.details['qid_label'] = self.add_text(column=left+2, row=top, text='Question number',  font=("Arial Bold", 10))
        self.details['qid'] = self.add_entry(column=left+3, row=top, width=20, justify="center", default_value = "1")
        
        self.details['sid_label'] = self.add_text(column=left+2, row=top+1, text='Student ID',  font=("Arial Bold", 12))
        self.details['sid'] = self.add_entry(column=left+3, row=top+1, width=20, justify="center", default_value = "0000000")
          

        
    def msgbox(self, title=None, message=None, **options):
        messagebox.showinfo(title=title, message=message, **options)
        
    def makeByYaml(self, path, addDetailsBar = True):
        self.elements={}
        offset = [0, 0]
        
        if addDetailsBar:
            offset[0] = offset[0] + 2 
            top, left = offset
            self.add_details_bar(left=0, top=0)
            
        
        with open(path) as file:
            structure = yaml.load(file)
            for key, element in structure.items():
                row, column = element['location'][0] + offset[0], element['location'][1] + offset[1]
                _ = self.add_text(text=element['title'],  font=("Arial Bold", 15), column=column-1, row=row)                
                
                if element['type'] == 'textBox':
                    self.elements[key] = self.add_entry(width=20, name=key, column=column, row=row)

                    
                elif element['type'] == 'dropDown':
                    options=element['options']
                    self.elements[key] = self.add_dropDown(width=20, name=key, column=column, row=row, options=options)
                
                    
                    
                    
        
        print(structure)
        

if __name__ == '__main__':
    gui = QuestionGui()
    gui.start()
    