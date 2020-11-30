# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 15:21:10 2019

@author: ashka
"""

from os.path import join
import yaml, sys
from GAME.texMaker import texMaker
from GAME.question import Question
from GAME.answer import Answer
from GAME.fileNameManager import FileNameManager
import GAME
import shutil
import os
import subprocess
from distutils import dir_util

def load_assignment(path, qdb = None, verbose = False):
    file = open(path,'r')
    assign = yaml.load(file)
    file.close()
    
    if qdb is not None:
       assign.question_db = qdb

    for q in assign.question_qids:
        this_Question = Question(join(assign.question_db,q))
        assign.questions.append(this_Question)
        if verbose: print('question is added: %s' % q)
    
    return assign

markingSchem={'ub': [79.999999999, 69.999999999, 59.999999999, 49.999999999, 0],'name':['HD', 'D', 'C', 'P', 'N']}
class Assignment():
    def __init__(self,question_db=None,question_list=None,name=None,assignment_num=0,assignmentName=None, studentID=None, weights=None):
        self.questions = []
        self.candidate_questions=question_list
        self.name = name
        self.assignment_num = assignment_num
        self.marks = []
        self.mark = None
        self.feedbacks = None
        self.question_db = question_db
        self.fromTexFile = False
        self.assignmentName = assignmentName
        self.studentID = studentID
        self.returnLetterMark = True
        if weights is not None:
            self.weights = weights
        
        self.compilers = ['pdflatex']
        self.markingSchem={'ub': [79.999999999, 69.999999999, 59.999999999, 49.999999999, 0],
                           'name':['HD', 'D', 'C', 'P', 'N']}
    @property
    def letterMark(self):
        return self.convertToLetter(self.mark)
        
    def convertToLetter(self, m):
        m = 0 if m is None else m
        ms = markingSchem 
        sorted_zip = sorted(zip(ms['ub'], ms['name']), key = lambda t: t[0])
        letterMark = sorted_zip[0][1]
        for i in sorted_zip:
            if m>i[0]:
                letterMark = i[1]
        return letterMark
            
    
    def markToShow(self, m):
        if self.returnLetterMark:
            return self.convertToLetter(m)
        
        else:
            return "{:4.1f}\%".format(m*100)
        
    def condolidate_tex(self):
        assign_tex = ['\\BN']
        for q in self.questions:
            assign_tex.append('\\item')
            if not isinstance(q.text.tex,list):
                tex_to_add = [q.text.tex]
            else:
                tex_to_add = q.text.tex
            
            assign_tex += tex_to_add
        assign_tex.append('\\EN')
        return assign_tex

    def make_assignment_pdf_from_tex_file(self,path,verbose=False):
        pathToFolder = join(self.question_db, self.assignmentName)
        pathToFiles = join(pathToFolder, 'files')
        dirPath = os.path.dirname(path2pdf(path))
        tempPath = join(dirPath, 'temp')
        
        q = Question(pathToFolder)
        #shutil.copytree(pathToFiles, dirPath, symlinks=False, ignore=None)
        

        dir_util.copy_tree(pathToFiles, tempPath)
        
        # compile

        oldPath = os.getcwd()
        os.chdir(tempPath)
        compileTexself(self.compilers, q.text.tex[0])
        shutil.copy(path2pdf(q.text.tex[0]),dirPath)
        os.chdir(oldPath)
        dir_util.remove_tree(tempPath)
        
     
    def write_assignment_tex_file(self,path):
        texMaker(self.condolidate_tex(), path, name=self.name,anum=self.assignment_num)

    def make_assignment_pdf(self,path):
        self.write_assignment_tex_file(path2tex(path))
        makePdf(self.compilers,path)
        
    def save_input_files(self,directory):
        for q in self.questions:
            
            fnm = FileNameManager(self.studentID, self.assignment_num, q.qid)
            savingPath =  join(directory, fnm.getInputFileName())
            q.text.save_inputs(savingPath)


    def save(self,path):
        '''
        with open(path, 'wb') as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)
        '''
        assignment_questions = self.questions.copy()
        assignment_mark = None
        assignment_feedbacks = None
        if self.mark is not None:
            assignment_mark = self.mark.copy()
        if self.feedbacks is not None:
            assignment_feedbacks = self.feedbacks.copy()
        
        self.questions = []
        self.mark = None
        self.feedbacks = None
        
        file = open(path,'w')
        yaml.dump(self, file)
        file.close()
        
        self.questions = assignment_questions
        self.mark = assignment_mark
        self.feedbacks = assignment_feedbacks
    

    
    def generate_question_list(self,verbose=False):
        for q in self.candidate_questions:
            
            
            self.questions.append(Question(join(self.question_db,q)))
            if verbose: print('question is added: %s' % q)
        self.get_question_qids()
        
        
    
    def get_question_qids(self):
        self.question_qids = []
        for q in self.questions:
            self.question_qids.append(q.qid)
        
    
    def mark_and_get_feedbacks(self,result_path_list):
        self.mark = 0 
        self.feedbacks = []
        for i, q in enumerate(self.questions):
            print(result_path_list[i])
            r = q.marking.result_loader(result_path_list[i])
            try:
                m, f = q.marking.marker(q.text.inputs, r)
            except Exception as e:
                m = None
                errorString = 'Marker encountered a problem! Error: %s' % repr(e)
                errorString = errorString.replace('_','\_')
                errorString = errorString.replace('$','\$')
                f = [errorString]
            m = 0 if m is None else m
            
            self.marks.append(m)
            
            if 'weights' in self.__dict__:
                self.mark += m * self.weights[i]
            else:
                self.mark += m / len(self.questions)
            
            self.feedbacks.append('Feedback for %s' % q.qid)
            self.feedbacks += f
            self.feedbacks.append("Mark for this part = %s" % self.markToShow(m))
            self.feedbacks.append(' \\noindent\\rule{8cm}{0.4pt} ')
            self.feedbacks.append(' \\noindent\\rule{8cm}{0.4pt} ')
        self.feedbacks.append("\\textbf{Total mark = " + self.letterMark + "}")
        self.feedbacks.append(' \\noindent\\rule{8cm}{0.4pt} ')
            
        
    
    def write_feedback_file(self,path,name=None,assignment_num=None):
        
        texMaker(self.feedbacks,path2tex(path),name=name,anum=assignment_num)
        


    def make_feedback_pdf(self,path,name=None,assignment_num=None):
        self.write_feedback_file(path2tex(path),name=name,assignment_num=assignment_num)
        makePdf(self.compilers, path)
        
    
    def path_manager(self):
        '''
        This should be organised better and should set results file names and 
        other sutff.
        '''
        pass
    
    def get_marking_scheme(self):
        '''
        This should manage the marking scheme!
        '''
        pass
    
def compileTexself(compilers, texFile):
    #si = subprocess.STARTUPINFO()
    #si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
   
    for command in compilers:
        subprocess.call(command + ' "%s"' % texFile, shell=True)        

def path2tex(path):
    pre, ext = os.path.splitext(path)
    return pre + '.tex'

def path2pdf(path):
    pre, ext = os.path.splitext(path)
    return pre + '.pdf'



def makePdf(compilers, texFile):
    
    #shutil.copytree(src, dst, symlinks=False, ignore=None)
    
    dirPath = os.path.dirname(path2pdf(texFile))
    #shutil.copytree(src, dst, symlinks=True)
    shutil.copyfile(GAME.clsFile, join(dirPath, 'CURSUS.cls'))
    oldPath = os.getcwd()
    os.chdir(dirPath)
    #os.system("pdflatex %s" % path)
    
    compileTexself(compilers, path2tex(texFile))
    '''
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    subprocess.call("pdflatex %s" % path, startupinfo=si)
    '''
    os.chdir(oldPath)

class Student():
    def __init__(self, student_id):
        self.ID = student_id
        self.marks = {}
        self.feedbacks = {}

    def add_answer(self, input_path, result_path, question, verbous=True):

        qid = question.qid
        self.marks[qid], self.feedbacks[qid] = Answer(input_path, result_path, question).get_mark()
        if self.marks[qid] is None:
            if verbous: print('  Mark = None')
        else:
            if verbous: print('  Mark = %8.2f' % self.marks[qid])

    def make_feedback_file(self, out_path, anum=0):
        texMaker(self.feedbacks, path2tex(out_path), anum=anum)

