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
        in_data = pd.read_csv(d_fn,sep=',',header=0,names=['A'])
    else:
        in_data = None
    return in_data


# ===================================================
def get_paths(base_path,Student_id,questionID):
    input_path = os.path.join(base_path,Student_id,'Inputs.csv')
    results_path = os.path.join(base_path,Student_id,'Results_%s.xlsx' % questionID)
    feedback_path = os.path.join(base_path,Student_id,'Assign3_feedbacks.tex')
    return input_path, results_path, feedback_path

def get_theoretical_probability(dist,LB,UB,Pars):
    LBp = dist.cdf(LB, loc=Pars.loc['Mean'], scale=Pars.loc['Standard deviation'])
    UBp = dist.cdf(UB, loc=Pars.loc['Mean'], scale=Pars.loc['Standard deviation'])
    return UBp-LBp

def get_results(r_fn):
    #Table = pd.read_excel(r_fn,sheet_name=0,header=0,usecols = "A:I")
    #Chi2 = pd.read_excel(r_fn,sheet_name=0,header=0,usecols = "K:L",index_col=0,nrows = 3)
    #Pars = pd.read_excel(r_fn,sheet_name=0,header=0,usecols = "K:L",index_col=0,nrows = 7,skiprows=list(range(5)))
    
    Chi2 = pd.read_excel(r_fn,sheet_name=0,header =0,usecols = "I:L",index_col=0,nrows = 2)
    Pars = pd.read_excel(r_fn,sheet_name=0,header =0,usecols = "I:J",index_col=0,nrows = 5,skiprows=list(range(4)))
    Table = pd.read_excel(r_fn,sheet_name=0,header =0,usecols = "A:G").iloc[:int(Pars.loc['Number of Classes'].values[0])]
    
    results={'Table':Table,'Chi2':Chi2,'Pars':Pars}
    return results

def mark_q3(Cal_Table,Cal_Pars,Cal_Chi2,Table,Pars,Chi2):
    mark_p=0
    feedback = []
    
    
    
    for column in Table.columns[2:]:
        if column in Cal_Table:
            for i in Cal_Table.index:
                max_mark = 1/len(Cal_Table.index)/7 # there are 6 column so 1/8 of marks for each column, and 2/8 for the pars and final chi2.
                m, f =  check_value(Cal_Table.loc[i,column],Table.loc[i,column],telorance=0.02,tel_mode='additive',var_to_check='%s for class %s' % (column,i) ,max_mark=max_mark)
                mark_p += m
                if max_mark != m:
                    feedback.append(f)
                    
     
    for i in Cal_Chi2['Chi sq.'].index:
        max_mark = 1/7/2
        m, f =  check_value(Cal_Chi2.loc[i].values[0],Chi2.loc[i].values[0],telorance=0.02,tel_mode='additive',var_to_check='Chi2 for %s' % i ,max_mark=max_mark)
        feedback.append(f)
        mark_p += m
    
    for col in ['Table chi sq. 95%','Table chi sq. 99%']:
        for i in Cal_Chi2[col].index:
            max_mark = 1/7/4
            m, f =  check_value(Cal_Chi2.loc[i].values[0],Chi2.loc[i].values[0],telorance=0.02,tel_mode='additive',var_to_check='%s for %s' % (col,i) ,max_mark=max_mark)
            feedback.append(f)
            mark_p += m
        
    return mark_p, feedback
            
   

def check_value(Calculated,Correct,telorance=0,tel_mode='additive',var_to_check='Lambda',max_mark=1/8):
    # Check the equation:
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
    return mark_p, feedback