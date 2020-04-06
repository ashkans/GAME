# -*- coding: utf-8 -*-

import os
from os.path import join
import importlib.util
import pickle


def load_module_by_name(path):
    spec = importlib.util.spec_from_file_location('', path)
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    return foo


class Question():
    def __init__(self, load_from_path=None, input_loader=None, result_loader=None, marker=None ,get_paths=None, qid=None, text_maker=None):
        self.qid = qid
        
        self.marking = Marking()
        self.marking.input_loader = input_loader
        self.marking.result_loader = result_loader
        self.marking.marker = marker
        self.marking.get_paths = get_paths
        
        self.text = TextMaker()
        self.text.maker = text_maker # for now all of the inputs should be saved as file, in future they should be able to be saved as variables.
        self.text.inputs=None
        self.text.tex=None
        
        
        
        if load_from_path is not None:
            self.load_from_path(load_from_path)
            
    def load_from_path(self,path):
        
        if not os.path.isdir(path):
            raise Exception('Path is not a directory!')
        
        marking_path = join(path, 'marking.py')
        loaded_module = load_module_by_name(marking_path)
        self.qid = os.path.basename(os.path.normpath(path))
        self.marking.input_loader = loaded_module.input_loader
        self.marking.result_loader = loaded_module.result_loader
        self.marking.marker = loaded_module.marker
        #self.marking.get_paths = loaded_module.get_paths
        
        question_maker_path = join(path, 'text_maker.py')
        loaded_module = load_module_by_name(question_maker_path)
        self.text.maker = loaded_module.maker
        self.text.save_inputs = lambda path, qid : loaded_module.save_inputs(self.text.inputs, path, qid)
        
        self.generate_inputs_tex(join(path,'files'))
    
    
    def generate_inputs_tex(self,file_path=None):
        self.text.inputs, self.text.tex = self.text.maker(file_path)        
        
    
    def save(self,path):
        with open(path, 'wb') as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)  


class Marking():
    def __init__(self,input_loader=None, result_loader=None, marker=None ,get_paths=None):
        self.input_loader = input_loader
        self.result_loader = result_loader
        self.marker = marker        
        self.get_paths = get_paths
        
        
        def get_correct_answer(): # The marker should be divided to get_correct answer and marker which just compares the answers
            print('This function is not ready, yet!')
            pass

class TextMaker():
    def __init__(self,maker=None ,tex=None, inputs=None, save_inputs=None):
        self.maker=maker
        self.tex=tex
        self.inputs=inputs
        self.save_inputs=lambda path, qid : save_inputs(self.inputs, path, qid)


