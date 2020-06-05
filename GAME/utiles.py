# -*- coding: utf-8 -*-
import yaml
import numpy as np
import inspect

class GuiStructure:
    def __init__(self):
        self.structure = {}
        
    def addElement(self, name, elementType, location, title, options=None):
        
        options = [] if options is None else options
        self.structure[name] = {'type':elementType, 'location':location, 'title':title, 'options':options}
        
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
    
    correctFeedbackString = '{varName} is correct!' if correctFeedbackString is None else correctFeedbackString
    cft = magic_fstring_function(correctFeedbackString)
    falseFeedbackString = '{varName} is not correct! The correct value is {correctAnswer}.' if falseFeedbackString is None else falseFeedbackString
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
        if studentAnswer == bounds:
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