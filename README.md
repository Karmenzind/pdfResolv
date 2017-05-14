### parse PDF and extract certain information (OCR if needed)

in python 2.7

1. Parse a pdf file and extract text object.
2. For scanning pdf, the OCR method is needed. For now, the result of recognition is not precise enough.
3. Collect all sentences including '(?i)fig(ure)(\s?\.\d+)?'.


required Py modules:
*  PythonMagick or wand
*  pyocr
*  PyPDF2
*  pdfminer
others:
*  tesseract-ocr
*  ImageMagick
*  GhostScript
