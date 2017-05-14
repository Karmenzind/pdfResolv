# coding: utf-8

import re
import os
import json

# pattern = re.compile(r'((([^.]+?\s)?(((?i)fig(ure)?)([.][\s]*\d+)?)(\s[^.]*?)?)+\.)')

"""
figure / fig. 1, fig.1
开头、结尾、中间有多个
i.e. / 小数
"""
# (?!([^\s]\.)) \d\.\d[^.]*?(?i)fig   (?<=\b(\.\s))
pattern = re.compile(r'([^.]*?(((?i)fig(ure)?s?(\.\s{0,2}\d+)?)[^.]*?)+[\.\n])')
key_pat = re.compile(r'((?i)fig(ure)?(\.\s{0,2}\d+)?)')

def fetch_pattern(file_name, txt):
    dist_res = []
    match_results = pattern.findall(txt)
    if not match_results:
        return
    print "\tcurrent part is:", txt.__repr__()
    with open('./res.csv', 'a') as res_f:
        for res in pattern.finditer(txt):
            if not res:
                continue
            sentence = res.group().lstrip('. ')
            if sentence in dist_res:
                continue
            dist_res.append(sentence)
            keyword = '|'.join(set(i[0] for i in (re.findall(key_pat, sentence))))
            print "\t\tFOUND:", sentence
            print >> res_f, '{},{},{}'.format(file_name,
                                              keyword.encode('utf-8'),
                                              sentence.encode('utf-8')) # keyword, RE res

def main():
    with file('./li_patents.json') as fp:
        base_contents = json.load(fp)  # dicts in list, "description" "patentid"
    for dct in base_contents:
        file_name = dct.get("patentid")
        print "current file is: ", file_name
        txt_pieces = (p for p in dct.get("description").split('\n') if len(p)>20)
        for piece in txt_pieces:
            fetch_pattern(file_name, '. ' + (piece.strip().replace('\t', ' ').rstrip('.')) + '.')
        print "-" * 100

if __name__ == '__main__':
    main()