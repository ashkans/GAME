# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 14:03:26 2019

@author: ashka
"""

import os
import pandas as pd
import numpy as np



def input_loader(d_fn,verbous=False):
    if verbous: print(d_fn)
    if (os.path.exists(d_fn)):
        in_data = pd.read_csv(d_fn,sep=':',header=None,names=['variables','descriptions'],index_col=[1])
    else:
        in_data = None
    return in_data

def get_feedback(False_answers):
    
    ostr = []
    #print("-----")
    #print(False_answers)
    for var in False_answers:
        for stat in False_answers[var]:
            ostr.append(('%s is calculated wrong for' % stat).capitalize()+ ' %s.' % var)
    
    feedbacks = ostr
    
    return feedbacks

def check_value(Calculated,Correct,telorance=0,tel_mode='additive',var_to_check='Lambda',max_mark=1/8):
    # Check the equation:
    if tel_mode.lower() == 'additive':
        bounds = [Correct - telorance, Correct + telorance]
        
    elif tel_mode.lower() == 'multiplicative':
        bounds = [Correct * (1-telorance), Correct (1+telorance)]
        
        
    sorted_bouds = [np.min(bounds),np.max(bounds)]

    if Calculated >= sorted_bouds[0] and Calculated <= sorted_bouds[1]:
        mark_p=max_mark
        feedback='%s is correct!' % var_to_check

    else:
        mark_p=0
        feedback='%s is not correct! The correct value is %8.3f' % (var_to_check, Correct)
    return mark_p, feedback

# ===================================================
def get_paths(base_path,Student_id,questionID):
    input_path = os.path.join(base_path,Student_id,'%s_assignment_01_parameters.txt' % Student_id)
    results_path = os.path.join(base_path,Student_id,'probability.xlsx')
    feedback_path = os.path.join(base_path,Student_id,'Q2_feedbacks.tex')

    return input_path, results_path, feedback_path
