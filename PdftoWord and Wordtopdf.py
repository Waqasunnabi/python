import os
from pdf2docx import parse
from docx2pdf import convert


folder_path_meps = r'link'
excel_files_meps = [f for f in os.listdir(folder_path_meps) if f.endswith('.docx')]


for files in excel_files_meps:
    file = folder_path_meps + "\\" + files
    docxfile = file[0:-4] + ".pdf"
    convert(file, docxfile)


# import os
# from pdf2docx import parse


# folder_path_meps = r'Link'
# excel_files_meps = [f for f in os.listdir(folder_path_meps) if f.endswith('.pdf')]


# for files in excel_files_meps:
#     file = folder_path_meps + "\\" + files
#     docxfile = file[0:-3] + ".docx"
#     parse(file, docxfile)


