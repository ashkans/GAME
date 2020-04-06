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
        in_data = pd.read_csv(d_fn,sep=',',header=0,index_col=0)
    else:
        in_data = None
    return in_data


# ===================================================
def get_paths(base_path,Student_id,questionID):
    input_path = os.path.join(base_path,Student_id,'Inputs.csv')
    results_path = os.path.join(base_path,Student_id,'Results.xlsx')
    feedback_path = os.path.join(base_path,Student_id,'Assign7_feedbacks.tex')
    return input_path, results_path, feedback_path

def get_results(r_fn):

    Hypothesis = pd.read_excel(r_fn,sheet_name=0,header =None,usecols = "A:B",index_col=0,nrows = 2)
    ANOVA = pd.read_excel(r_fn,sheet_name=0,header =0,usecols = "A:G",index_col=0,nrows = 2,skiprows=list(range(3)))
    CR_tk = pd.read_excel(r_fn,sheet_name=0,header =0,usecols = "A:C",index_col=0,nrows = 2,skiprows=list(range(7)))
    CR_tk_Comp_Table =  pd.read_excel(r_fn,sheet_name=0,header =0,usecols = "A:H",index_col=0,nrows = 15,skiprows=list(range(12)))

    
    results={'Hypothesis':Hypothesis,'ANOVA':ANOVA,'CR_tk':CR_tk,'CR_tk_Comp_Table':CR_tk_Comp_Table}
    return results

def mark_q7(Cal_Hypothesis, Cal_ANOVA, Cal_CR_tk,  Cal_CR_tk_Comp_Table,Hypothesis, ANOVA,CR_tk,  CR_tk_Comp_Table):
    mark_p=0
    feedback = []
    

    #mark ANOVA:
    
    for var in ['SS', 'DF', 'MS']:
        for source in ['Treatments', 'Error']:
            max_mark = 1/10 * 1/2 * 1/2
            m, f =  check_value(ANOVA.loc[source,var],Cal_ANOVA.loc[source,var],telorance=0.02,tel_mode='additive', var_to_check='%s of %s' % (var, source) ,max_mark=max_mark)
            mark_p += m
            feedback.append(f)            
            
    for var in ['F', 'F_Table 95%', 'F_Table 99%']:
        for source in ['Treatments']:	
            
            if var == 'F':
                max_mark = 1/2 * 1/2
            else:
                max_mark = 1/5 * 1/2 * 1/2
                
            
            m, f =  check_value(ANOVA.loc[source,var],Cal_ANOVA.loc[source,var],telorance=0.02,tel_mode='additive',var_to_check='%s' % (var) ,max_mark=max_mark)
            mark_p += m
            feedback.append(f) 
            
    #mark Cal_CR_tk:
    for var in ['Q','CR_tk']:
        for conf in [0.05,0.01]:	
            max_mark = 1/4 * 1/4 
            m, f =  check_value(CR_tk.loc[conf,var],Cal_CR_tk.loc[conf,var],telorance=0.1,tel_mode='multiplicative',var_to_check='%s of %5.2f' % (var, conf) ,max_mark=max_mark)
            mark_p += m
            feedback.append(f)     
    
    
    #mark Cal_CR_tk_Comp_Table:

    
    var = ['Meaningful difference at 99?','Meaningful difference at 95?']
        
    
    Cols= np.where(Cal_CR_tk_Comp_Table[var] != CR_tk_Comp_Table[var])[1]
    Rows = np.where(Cal_CR_tk_Comp_Table[var] != CR_tk_Comp_Table[var])[0]
    m = 1 / 4
    for i in Cols:
        if var[i] == 'Meaningful difference at 99?':
            conf = '99\\%'
        else:
            conf = '95\\%'
        
        feedback.append('The conclusion about the meaningfulness of difference of %d and %d at level of %s is not right.' % 
                        (Cal_CR_tk_Comp_Table.index[Rows[0]], Cal_CR_tk_Comp_Table['Fert. B'].iloc[Rows[0]],conf)) 
        m -= 0.05
        
    mark_p += max(m,0)  
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