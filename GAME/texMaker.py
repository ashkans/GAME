# -*- coding: utf-8 -*-
#################################################################
# Close the feedback file.					#
#################################################################
def close_feedback(f_ptr):

    f_ptr.write('\n\\end{document}\n')
    f_ptr.close

    return(f_ptr)

#################################################################
# Open the feedback file and print the header.			#
#################################################################

def open_feedback(f_fn,tstr,anum):

    f_ptr=open(f_fn,"w")
    f_ptr=print_header(f_ptr,tstr,anum)

    return(f_ptr)

#################################################################
# Print out the header for the feedback file.			#
#################################################################

def print_header(f_ptr,tstr,cnum):

    f_ptr.write('\\documentclass[a4paper,12pt]{CURSUS}\n')
    f_ptr.write('\n')
    f_ptr.write('\\usepackage[english]{babel}\n')
    f_ptr.write('\\usepackage{latexsym}\n')
    f_ptr.write('\\usepackage{amsfonts}\n')
    f_ptr.write('\\usepackage{times}\n')
    f_ptr.write('\\usepackage{fancyhdr}\n')
    f_ptr.write('\\usepackage{rotating}\n')
    f_ptr.write('\\usepackage{graphicx}\n')
    f_ptr.write('\\usepackage{longtable}\n')
    f_ptr.write('\\usepackage{booktabs}\n')
    f_ptr.write('\\usepackage[table]{xcolor}\n')
    f_ptr.write('\n')
    f_ptr.write('\\textwidth 16.5cm\n')
    f_ptr.write('\\textheight 23cm\n')
    f_ptr.write('\\marginparwidth 0cm\n')
    f_ptr.write('\\topmargin 0.54cm\n')
    f_ptr.write('\\oddsidemargin 0cm\n')
    f_ptr.write('\\evensidemargin 0cm\n')
    f_ptr.write('\\parindent 0pt\n')
    f_ptr.write('\\parskip 5mm\n')
    f_ptr.write('\\headsep 0cm\n')
    f_ptr.write('\\footskip 2cm\n')
    f_ptr.write('\\flushbottom\n')
    f_ptr.write('\n')
    f_ptr.write('\\newcommand{\\BE}{\\begin{equation}}\n')
    f_ptr.write('\\newcommand{\\EE}{\\end{equation}}\n')
    f_ptr.write('\\newcommand{\\BI}{\\begin{itemize}}\n')
    f_ptr.write('\\newcommand{\\EI}{\\end{itemize}}\n')
    f_ptr.write('\\newcommand{\\BN}{\\begin{enumerate}}\n')
    f_ptr.write('\\newcommand{\\EN}{\\end{enumerate}}\n')
    f_ptr.write('\\newcommand{\\D}{\\displaystyle}\n')
    f_ptr.write('\n')
    f_ptr.write('\\renewcommand {\\baselinestretch}{1.2}\n')
    f_ptr.write('\n')
    f_ptr.write('\\renewcommand{\\headrulewidth}{0mm}\n')
    f_ptr.write('\\renewcommand{\\footrulewidth}{0.2mm}\n')
    f_ptr.write('\n')
    f_ptr.write('\\pagestyle{fancy}\n')
    f_ptr.write('\\addtolength{\\headwidth}{4mm}\n')
    f_ptr.write('\\renewcommand{\\chaptermark}[1]{\\markboth{#1}{}}\n')
    f_ptr.write('\\fancypagestyle{plain}{\n')
    f_ptr.write('\\fancyhead[R,L]{}\n')
    f_ptr.write('\\fancyfoot[R]{\\thepage}\n')
    f_ptr.write('\\fancyfoot[C,L]{}}\n')
    f_ptr.write('\\fancyhead[R,L,C]{}\n')
    f_ptr.write('\\fancyfoot[R]{\\thepage}\n')
    f_ptr.write('\\fancyfoot[C,L]{}\n')
    f_ptr.write('\n')
    f_ptr.write('\\begin{document}\n')
    f_ptr.write('\n')
    ostr='\\addtocounter{chapter}{'+repr(cnum)+'}\n'
    f_ptr.write(ostr)
    f_ptr.write('\\renewcommand{\\chaptername}{Assignment}\n')
    ostr='\\chapter{'+tstr+'}\n'
    f_ptr.write(ostr)

    return(f_ptr)

def texMaker(ostr,outputfile,name='Calculate basic statistics',verbous=False,anum=0):
    #print(ostr)
    
    f_ptr = open_feedback(outputfile,name,anum-1)
    f_ptr.write('\n')
    all_ostr = ''
    
    for rec in ostr:
        all_ostr += ' %s\n\n' % rec

        
    f_ptr.write(all_ostr)
    print('Tex file is generated!')
    
    close_feedback(f_ptr)    
