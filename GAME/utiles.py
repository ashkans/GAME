# -*- coding: utf-8 -*-
import yaml

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


