# coding: utf-8
"""
从pdf中提取文本
1、文字版
2、扫描版（纯/混合）
"""

import os
import re
import tempfile
from OcrPart import ManImage
from pdfminer import layout as LT
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import (PDFPage, PDFTextExtractionNotAllowed)
from pdfminer.pdfinterp import (PDFResourceManager, PDFPageInterpreter)
from pdfminer.converter import PDFPageAggregator

pattern = re.compile(r'((([^.]+?\s)?(((?i)fig(ure)?)([.][\s]*\d+)?)(\s[^.]*?)?)+\.)')

def fetch_pattern(pdf_file_path, txt_path):
    with open(txt_path, 'r') as f:
        final_txt = ' '.join((line.strip() for line in f
                              if len(line) > 15))
    with open('./res.csv', 'a') as f:
        for res in pattern.findall(final_txt):
            print "Found: ", res[0]
            print >> f, "{},{},{}".format(pdf_file_path, res[-4], res[0])


class PdfExtBasic(object):

    def __init__(self, file_path):
        self.file_path = file_path
        self.to_ocr = [] # raw picture page idx, needed to OCR

    def get_layouts(self):
        """
        get layouts from raw pdf file.
        :return: (page idx, layout obj) generator 
        """
        with open(self.file_path, 'rb') as fp:
            parser = PDFParser(fp)
            document = PDFDocument(parser, password='') # stores the document structure.
            if not document.is_extractable:
                raise PDFTextExtractionNotAllowed
            rsrcmgr = PDFResourceManager() # stores shared resources.
            laparams = LT.LAParams()
            device = PDFPageAggregator(rsrcmgr, laparams=laparams)
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            for idx, page in enumerate(PDFPage.create_pages(document)):
                interpreter.process_page(page)
                yield idx, device.get_result() # page idx, layout obj

    def parse_layout(self, layout):
        """
        recursively parse the layout tree.
        """
        for lt_obj in layout:
            if isinstance(lt_obj, LT.LTTextBox) or isinstance(lt_obj, LT.LTTextLine):
                yield lt_obj.get_text()
            elif isinstance(lt_obj, LT.LTFigure):
                self.parse_layout(lt_obj)

    def proc_file(self, output):
        MI = ManImage(os.path.abspath(self.file_path), tempfile.gettempdir())
        with open(output, 'w') as f:
            for idx, layout in self.get_layouts():
                has_txt = 0
                for txt_res in self.parse_layout(layout):
                    has_txt += 1
                    print >> f, txt_res.encode('utf-8'),
                if not has_txt:
                    pic_txt = MI.fetch_pic_txt(idx)
                    try:
                        print >> f, pic_txt.encode('utf-8')
                    except Exception, e:
                        print e.__class__.__name__, e
                else:
                    print "Got raw txt from page ", idx + 1

if __name__ == '__main__':
    fetch_pattern('XXX.pdf','C:\Users\Karmenzind\AppData\Local\Temp\outputforpdf.txt')