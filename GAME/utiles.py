# -*- coding: utf-8 -*-
import yaml, os
import numpy as np
import inspect
import importlib
from os.path import join


def _writeModule(module, path, obfuscate, nonlatin):
    moduleString = inspect.getsource(module)
    
    pathTemp = path + 'temp'
    f = open(pathTemp, "w")
    f.write(moduleString)
    f.close()    
    
    
    string = f'pyminifier {pathTemp} > {path}'
    if obfuscate:
        string = f'pyminifier -O --nonlatin --replacement-length=2 {pathTemp} > {path}'
        
        if not nonlatin:
            string = f'pyminifier -O --replacement-length=2 {pathTemp} > {path}'
                
    
    os.system(string)
    os.remove(pathTemp)
    
    
    f = open(path, "r")
    lines = f.readlines()
    f.close()   
    
    f = open(path, "w")    
    f.writelines(lines[:-2])  
    f.close()

def installGameForGui(path=None, modules=['questionGui', 'fileNameManager'], 
                      obfuscate=False, nonlatin=True):
    
    path = '' if path is None else path
    gamePath = os.path.join(path, 'GAME')
    if not os.path.exists(gamePath):
        os.makedirs(gamePath)
    
    for m in modules:
        _writeModule(importlib.import_module('GAME.' + m), join(gamePath,m+'.py'),
                     obfuscate, nonlatin)
  
    f = open(join(gamePath,'__init__.py'), "w")
    f.write('')
    f.close()   

class GuiStructure:
    def __init__(self):
        self.structure = {}
        
    def addElement(self, name, elementType, location, title, options=None, withTitle=True):
        '''
        

        Parameters
        ----------
        name : TYPE
            DESCRIPTION.
        elementType : TYPE
            DESCRIPTION.
        location : TYPE
            DESCRIPTION.
        title : TYPE
            DESCRIPTION.
        options : TYPE, optional
            DESCRIPTION. The default is None.

        Returns
        -------
        None.

        '''
        
        
        options = [] if options is None else options
        self.structure[name] = {'type':elementType, 'location':location, 'title':title, 'options':options, 'withTitle':withTitle}
        
    def save(self, path):
        with open(path, 'w') as file:
            return yaml.dump(self.structure, file)
        
        
    def load(self, path):
        with open(path, 'r') as file:
            self.structure = yaml.load(file)
            return self.structure      

    def __repr__(self):
        import pprint
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self.structure)
        return ''


class magic_fstring_function:
    def __init__(self, payload):
        self.payload = payload
    def __str__(self):
        vars = inspect.currentframe().f_back.f_globals.copy()
        vars.update(inspect.currentframe().f_back.f_locals)
        return self.payload.format(**vars)


def checkValues(studentAnswer, correctAnswer,varName, maxMark=1,
                comparisonType=('Additive', 0), correctFeedbackString=None,
                falseFeedbackString=None):

    #correctFeedbackString = '%s is correct!' if correctFeedbackString is None else correctFeedbackString
    #falseFeedbackString = '%s is not correct! The correct value is %8.3f' if falseFeedbackString is None else falseFeedbackString
    
    correctFeedbackString = 'The {varName} is correct.' if correctFeedbackString is None else correctFeedbackString
    cft = magic_fstring_function(correctFeedbackString)
    falseFeedbackString = 'The {varName} is not correct, the correct value is {correctAnswer}.' if falseFeedbackString is None else falseFeedbackString
    fft = magic_fstring_function(falseFeedbackString)
    
    
    
    compDict = {'a':'Additive', 'additive':'Additive', 'Additive':'Additive',
                'm':'Multiplicative', 'multiplicative':'Multiplicative', 'Multiplicative':'Multiplicative',
                't':'String', 's':'String', 'string':'String', 'String':'String',
                'e':'Exact', 'exact':'Exact', 'Exact':'Exact' }
    
    if isinstance(comparisonType, str):
        comparisonType = (comparisonType, None)        
    comparisonHow = compDict[comparisonType[0].lower()]
    
    if comparisonHow != 'String':
        comparisonTol = comparisonType[1]
        
        
    if comparisonHow == 'Additive':
        bounds = [correctAnswer - comparisonTol, correctAnswer + comparisonTol]
        
    elif comparisonHow == 'Multiplicative':
        bounds = [correctAnswer * (1-comparisonTol), correctAnswer * (1+comparisonTol)]
        
    elif comparisonHow == 'Exact':
        bounds = [correctAnswer, correctAnswer]
    
    elif comparisonHow == 'String':
        bounds = [correctAnswer]
    
    else:   
        bounds = None
        

    correct = False
    if len(bounds) == 1:
        print(bounds[0], studentAnswer)
        if studentAnswer == bounds[0]:
            correct = True
    else:
        if studentAnswer >= bounds[0] and studentAnswer <= bounds[1]:
            correct = True
            
   
    if correct:
        #return maxMark, correctFeedbackString % varName
        return maxMark, str(cft)

    else:
        #return 0, falseFeedbackString % (varName, correctAnswer)  
        return 0, str(fft)  