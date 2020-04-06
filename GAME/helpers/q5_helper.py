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
        in_data = pd.read_csv(d_fn,sep=',',header=None,names=['Description','Values'],index_col=0)
    else:
        in_data = None
    return in_data


# ===================================================
def get_paths(base_path,Student_id,questionID):
    input_path = os.path.join(base_path,Student_id,'Inputs.csv')
    results_path = os.path.join(base_path,Student_id,'Results_%s.xlsx' % questionID)
    feedback_path = os.path.join(base_path,Student_id,'Assign5_feedbacks.tex')
    return input_path, results_path, feedback_path

def get_results(r_fn):
    #Table = pd.read_excel(r_fn,sheet_name=0,header=0,usecols = "A:I")
    #Chi2 = pd.read_excel(r_fn,sheet_name=0,header=0,usecols = "K:L",index_col=0,nrows = 3)
    #Pars = pd.read_excel(r_fn,sheet_name=0,header=0,usecols = "K:L",index_col=0,nrows = 7,skiprows=list(range(5)))
    

    Hypothesis = pd.read_excel(r_fn,sheet_name=0,header =0,usecols = "A:D",index_col=0,nrows = 2)
    Values = pd.read_excel(r_fn,sheet_name=0,header =None,usecols = "B:C",index_col=0,nrows = 10,skiprows=list(range(4)))

    
    results={'Hypothesis':Hypothesis,'Values':Values}
    return results

def mark_q5(Cal_Hypothesis, Cal_Values,Hypothesis,Values):
    mark_p=0
    feedback = []
    
    # Mark Hypothesis:
    for H in ['H0:','H1:']:
        max_mark = 1 / 8
        m, f =  check_value(Cal_Hypothesis.loc[H,'Sign'],Hypothesis.loc[H,'Sign'],tel_mode='non_number',var_to_check='%s' % (H[:-1]) ,max_mark=max_mark)
        mark_p += m
        feedback.append(f)
    
    for variable in Cal_Values.index:
        max_mark = 3 / 40
        if isinstance(Cal_Values.loc[variable].values[0],float):
            tel_mode = 'additive'
        else:
            tel_mode = 'non_number'
            
        calc = Cal_Values.loc[variable].values[0]
        correct  = Values.loc[variable].values[0]
        if variable == 'Table statistics':
           calc= abs(calc)
           correct = abs(correct)
        
        m, f =  check_value(correct,calc,telorance=0.02,tel_mode=tel_mode,var_to_check='%s' % (variable) ,max_mark=max_mark)
        mark_p += m
        feedback.append(f)
    
    return mark_p, feedback
            
   

def check_value(Calculated,Correct,telorance=0,tel_mode='additive',var_to_check='Lambda',max_mark=1/8):
    # Check the equation:
    
    if tel_mode.lower() != 'non_number':
        if tel_mode.lower() == 'additive':
            bounds = [Correct - telorance, Correct + telorance]
            
        elif tel_mode.lower() == 'multiplicative':
            bounds = [Correct * (1-telorance), Correct * (1+telorance)]
        
             
        sorted_bouds = [np.min(bounds),np.max(bounds)]
    
        if Calculated >= sorted_bouds[0] and Calculated <= sorted_bouds[1]:
            mark_p=max_mark
            feedback='%s is correct!' % var_to_check
    
        else:
            mark_p=0
            feedback='%s is not correct! The correct value is %8.3f' % (var_to_check, Correct)
    else:
        if Calculated == Correct:
            mark_p=max_mark
            feedback='%s is correct!' % var_to_check
        else:
            mark_p=0
            feedback='%s is not correct! The correct value is %s' % (var_to_check, Correct)
            
    return mark_p, feedback