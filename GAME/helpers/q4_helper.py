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
        in_data = pd.read_csv(d_fn,sep=',',names=['Variable','Value'])
        in_data.set_index('Variable',inplace=True)
        in_data = in_data.to_dict()['Value']
    else:
        in_data = None
    return in_data


# ===================================================
def get_paths(base_path,Student_id,questionID):
    input_path = os.path.join(base_path,Student_id,'Inputs_%s.csv' % questionID)
    results_path = os.path.join(base_path,Student_id,'Results_%s.xlsx' % questionID)
    feedback_path = os.path.join(base_path,Student_id,'Assign4_feedbacks.tex')
    return input_path, results_path, feedback_path

def get_theoretical_probability(dist,LB,UB,Pars):
    LBp = dist.cdf(LB, loc=Pars.loc['Mean'], scale=Pars.loc['Standard deviation'])
    UBp = dist.cdf(UB, loc=Pars.loc['Mean'], scale=Pars.loc['Standard deviation'])
    return UBp-LBp

def get_results(r_fn):
    
    results = pd.read_excel(r_fn,sheet_name=0,index_col=0,header=None)
    results = results.to_dict()[1]
    return results

def check_probability(correct_answer, student_answer):
    
    mark_p=0
    feedback = []
    
    for key in correct_answer:

        max_mark = 1 / len(correct_answer)
        var_to_check = key
        if isinstance(student_answer[key],str): 
            tel_mode = 'string'
        else:
            tel_mode='multiplicative'
        m, f = check_value(student_answer[key],correct_answer[key],telorance=0.1,tel_mode=tel_mode,var_to_check=var_to_check,max_mark=max_mark)
        mark_p += m
        if max_mark != m:
            feedback.append(f)
    
    return mark_p, feedback
    


def check_value(Calculated,Correct,telorance=0,tel_mode='additive',var_to_check='Lambda',max_mark=1/8):
    # Check the equation:
    
    answer_is_correct = False
    if tel_mode.lower() != 'string':
        if tel_mode.lower() == 'additive':
            bounds = [Correct - telorance, Correct + telorance]
            
        elif tel_mode.lower() == 'multiplicative':
            bounds = [Correct * (1-telorance), Correct * (1+telorance)]
                        
        sorted_bouds = [np.min(bounds),np.max(bounds)]
    
        if (Calculated >= sorted_bouds[0] and Calculated <= sorted_bouds[1]) or \
        (np.isnan(Calculated) and np.isnan(Correct)) :
            answer_is_correct = True
        
    else:
        if Calculated.lower() == Correct.lower():
            answer_is_correct = True
            
    if answer_is_correct:     
        mark_p=max_mark
        feedback='%s is correct!' % var_to_check
    else:
        mark_p=0
        if isinstance(Correct,str):
            feedback='%s is not correct! The correct value is %s' % (var_to_check, Correct)                 
        else:
            feedback='%s is not correct! The correct value is %8.3f' % (var_to_check, Correct)                 
        
    return mark_p, feedback