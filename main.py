# coding: utf-8

import os
import shutil
import tempfile
from Extract import (PdfExtBasic, fetch_pattern)

PDF_DIR_PATH = u'./files'
TEMP_TXT_PATH = os.path.join(tempfile.gettempdir(), 'outputforpdf.txt')

if __name__ == '__main__':
    finished = []
    for file_name in os.listdir(PDF_DIR_PATH):
        print 'current file: ', file_name
        file_path = os.path.join(PDF_DIR_PATH, file_name)
        try:
            pdf_ext = PdfExtBasic(file_path)
            pdf_ext.proc_file(TEMP_TXT_PATH)
            fetch_pattern(file_path, TEMP_TXT_PATH)
        except Exception, e:
            print e.__class__.__name__, e
        else:
            finished.append(file_name)
            shutil.move(file_path, os.path.join('./finished', file_name))
    else:
        print "ALL IS DONE :)"