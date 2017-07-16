### parse PDF and extract certain information (OCR if needed)

in python 2.7

1. Parse a pdf file and extract text object.
2. For scanning pdf, the OCR method is needed. For now the result of recognition isn't precise enough.
3. Collect all sentences matching '((([^.]+?\s)?(((?i)fig(ure)?)([.][\s]*\d+)?)(\s[^.]*?)?)+\.)'.

