import pandas as pd

def get_all_marks(students):
    data_frame1 = pd.DataFrame()
    for stu in students:
        data_frame2 = pd.DataFrame.from_dict(stu.marks, orient='index', columns=[stu.ID]).T

        data_frame1 = pd.concat([data_frame1, data_frame2], axis=0, sort=False)
        
    return data_frame1

def get_all_feedbacks(students):
    data_frame1 = pd.DataFrame()
    for stu in students:
        data_frame2 = pd.DataFrame.from_dict(stu.feedbacks, orient='index', columns=[stu.ID]).T
        data_frame = pd.concat([data_frame1, data_frame2], axis=0, sort=False)
    return data_frame
# -*- coding: utf-8 -*-

