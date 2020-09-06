from tkinter import Tk, Button, Label, Entry, messagebox, StringVar, OptionMenu, filedialog, ttk
import tkinter as tk
import yaml
from os.path import join
from tkinter.ttk import Separator, Style
from GAME.fileNameManager import FileNameManager
import pandas as pd

class QuestionGui(object):
    def __init__(self, title = None, resizable = True, geometry = None, 
                 aid_default="1", qid_default="1", sid_default="0000"):
        self.title = "Engineering Investigation" if title is None else title
        self.resizable = (0, 0) if not resizable else (1,1)
        
        if geometry is None:
            geometry = '600x350'
        self.geometry = geometry
        self.window = Tk()
    
        self.aid_default=aid_default
        self.qid_default=qid_default
        self.sid_default=sid_default
        
        self.savingOrder = None

        
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

    def add_dropDown(self, column=0, row=0, options = None, callback=None, **kwargs):
        options = ['--'] if options is None else options
        variable = StringVar(self.window)
        variable.set(options[0]) # default value
        opt = OptionMenu(self.window, variable, *options)
        opt.grid(column=column, row=row)
        
        if callback is None:
            def callback(*args):
                pass
                #self.msgbox(title='a', message=variable.get())
        
        variable.trace("w", callback)

        return opt, variable    
    
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
        self.details['aid_label'] = self.add_text(column=left, row=top, text='Assignment number',
                                                  font=("Arial Bold", 10))
        self.details['aid'] = self.add_entry(column=left+1, row=top, width=20,
                                             justify="center", default_value = self.aid_default)
        
        self.details['qid_label'] = self.add_text(column=left+2, row=top, text='Question number',
                                                  font=("Arial Bold", 10))
        self.details['qid'] = self.add_entry(column=left+3, row=top, width=20, 
                                             justify="center", default_value = self.qid_default)
        
        self.details['sid_label'] = self.add_text(column=left+2, row=top+1, text='Student ID',
                                                  font=("Arial Bold", 12))
        self.details['sid'] = self.add_entry(column=left+3, row=top+1, width=20,
                                             justify="center", default_value = self.sid_default)
          
    def savedf(self,df, fn):
        d = filedialog.askdirectory(title='Please select a folder to save the output!')
        
        if d != "":

            #fn = "output.xlsx" if fn == "" else fn_no_ext
            
            f = join(d, fn)
                        
            try:
                df.to_excel(f)
                self.msgbox(title="Your file is saved!", message= "File is saved here: %s" % f)
            except:
                self.msgbox(msgtype='error', title="There is some issue with saving! Your file is not saved!", message= "Your file is not saved!")        
        
    def msgbox(self, title=None, message=None, msgtype='info', **options):
        
        if msgtype == 'error':
            messagebox.showerror(title=title, message=message, **options)
        elif msgtype == 'warning' :   
            messagebox.showwarning(title=title, message=message, **options)
        else:
            messagebox.showinfo(title=title, message=message, **options)
        
    def makeByYaml(self, path, addDetailsBar = True, savingOrder=None):
        self.elements={}
        self.savingOrder=savingOrder
        offset = [0, 0]
        
        
      
        
        if addDetailsBar:
            offset[0] = offset[0] + 2 
            top, left = offset
            self.add_details_bar(left=0, top=0)
            
        
        with open(path) as file:
            structure = yaml.load(file)
            for key, element in structure.items():
                row, column = element['location'][0] + offset[0], element['location'][1] + offset[1]
                if 'withTitle' in element.keys():
                    withTitle = element['withTitle']

                out = self.add_element(element, column, row, key, withTitle=withTitle)
                if out[1] is not None: 
                    self.elements[key] = out[1]
                    
                    
        self.add_save_button(column=1, row = 15)
        
                   
    def add_save_button(self, column, row, savingOrder=None):
        self.add_button(column=column, row=row, text="Save", bg="white", fg="black", command=self.saveElements)

    def saveElements(self):
        df = pd.DataFrame(columns=['0'])   
        
        if self.savingOrder is None:
            for k, e in self.elements.items():
                df.loc[k]=e.get()
        else:
            for k in self.savingOrder:
                df.loc[k]=self.elements[k].get()                         

        
    
        fnm = FileNameManager(self.details['sid'].get() , self.details['aid'].get(), self.details['qid'].get())
        fn = fnm.getAnswerFileName()
            
        self.savedf(df, fn)
            
        
        
    def add_element(self, element, column, row, name, withTitle=True):
        '''
        element (dict)
            element['title']
            element['type']

        '''
        
        if withTitle:
            txt = self.add_text(text=element['title'],  font=("Arial Bold", 12), column=column-1, row=row)
        else:
            txt = None
            
        if element['type'] == 'textBox':
            obj = self.add_entry(width=20, name=name, column=column, row=row)
            return [txt, obj]
    
        elif element['type'] == 'dropDown':
            options = element['options']
            if 'callback' in element.keys():
                callback = element['callback']
            else:
                callback = None
                
            obj, strvar = self.add_dropDown(width=20, name=name, column=column, row=row, options=options, callback = callback)
            return [txt, obj], strvar

        if element['type'] == 'text':

            obj = self.add_text(text=element['title'],  font=("Arial Bold", 10), column=column-1, row=row)
            return [None, None]
        
        
        if element['type'] == 'hl':
            options = element['options']
            sty = Style(self.window)
            sty.configure("TSeparator", background="black")            
            sep_h = Separator(self.window, orient="horizontal")            
            sep_h.grid(column=column, row=row, rowspan = options[0], columnspan = 1, sticky='ns')
            return [None, None]
          
        if element['type'] == 'vl':
            options = element['options']
            sty = Style(self.window)
            sty.configure("TSeparator", background="black")  
            sep_v = Separator(self.window, orient="vertical")            
            sep_v.grid(column=column, row=row, rowspan = 1, columnspan = options[0], sticky='ew')
            return [None, None]  


        
def make_element(title,elementType,options=None, callback=None):
    '''
    title -> str
    elementType in {'textBox', 'dropDown'}
    

    '''
    options =[] if options is None else options
    return {'title': title, 'type': elementType, 'options':options, 'callback':callback}        

if __name__ == '__main__':
    gui = QuestionGui()
    gui.start()
    