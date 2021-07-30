# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 17:27:59 2020

@author: ashkans
"""
class FileNameManager:
    def __init__(self, studentID, assignment_num, qid):
        self.studentID=studentID
        self.assignment_num=assignment_num
        self.qid=qid
    
    def getInputFileName(self):
        return 'input_%s_A%s_%s.csv' % (self.studentID, self.assignment_num, self.qid)
    
    def getAnswerFileName(self):
#        return 'answer_%s_A%s_%s.xlsx' % (self.studentID, self.assignment_num, self.qid)
        return 'answer_%s_A%s_%s.csv' % (self.studentID, self.assignment_num, self.qid)
    
    def feedbackFileName(self):
        return 'feedback_%s_A%d.pdf'%(self.studentID, self.assignment_num)
