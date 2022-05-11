import os
import shutil

def get_files():
    i = 0
    for filepath,dirnames,filenames in os.walk(r'E:\QQ_file\200\20220402181519952031'):
        for filename in filenames:
            print(filepath+'\\'+filename)
            os.rename(filepath+'\\'+filename,filepath+'\\'+'5_'+filename)
get_files()