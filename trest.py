# -*- coding: utf-8 -*-
# encoding=utf8
# encoding: utf-8
import sys
import re
import csv
import chardet
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import *
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase


reload(sys)
sys.setdefaultencoding('utf8')

bibtex_str = ''
text = []
name = ''
strname = ''
location = ''
strlocation = ''
citation =''
author =''
parser = BibTexParser()
with open('SPIM Bib file.bib') as bibtex_file:
    bibtex_str = bibtex_file.read()
output = bibtexparser.loads(bibtex_str)

def countAuthor(str,capital):
    '''
    author name > 3, plus et al.
    '''

    lis = str.split('and')
    print(lis)
    if len(lis) > 3:
        result = lis[0:3]
        result = ','.join(result)
        result = result.split(',')

        if (capital):
            for i in range(0,len(result)):
                if (i %2 ==0):
                    result[i] = result[i]+","
                elif(i == 3):
                    try:
                        result[i] = result[i][1]+"., &"
                    except:
                        result[i] = result[i] + ","
                else:
                    try:
                        result[i] = result[i][1]+".,"
                    except:
                        result[i] = result[i]+","
                i = i+1
            result = ''.join(result) +"et al."
        else:
            result = ''.join(str)
            result = result.split('and')
            result = result[0:3]

            result = 'and'.join(result)


        result = ''.join(str)
        result = result.strip('\\n')

    return result

def textSelection(flag,a,str):
    '''
    This method is used to check whether the return value from regEx
    can be used
    :param str: matchObj
    :return:string
    '''
    value = ''
    if flag == True:
        pattern = 'u\W' + str + '\W\:\su\'(.*?)\','
        reg = re.search(pattern,a,re.M)

        if reg is not None:
            value = reg.group(1)
    else:
        if a is not None:
            value = a.group(1)

    return value
def dewhitespace(str, type):
    str.strip()
    if not str:
        str = ""
    elif type == 'year':
        str = str
    elif type is 'month' :
        str = ', ' + str
    elif type is 'number':
        str = '('+ str + ")"
    elif type is 'link':
        str = ". Retrieved from " + str
    elif type is 'doi':
        str= 'doi: ' + str
    elif type is 'volume':
        str = " "+str+", "
    elif type is 'journal':
        str = '. '+str
    else:
        str = '. ' + str
    return str
# print output.entries_dict


for i in output.entries_dict:
    a = output.entries_dict[i]
    a = str(a)
    strname = textSelection(True,a,'author')
    strlocation = textSelection(True,a,'affiliation')
    year = textSelection(True,a,'year')
    title = textSelection(True,a,'title')
    booktitle = textSelection(True,a,'booktitle')
    publisher = textSelection(True,a,'publisher')
    journal = dewhitespace(textSelection(True,a,'journal'),'journal')
    month = textSelection(True,a,'month')
    month = re.match(r'([a-z]*)',month,re.M)
    month = textSelection(False,month,'')

    month = dewhitespace(month,'month')
    year = dewhitespace(year, 'year')
    doi = dewhitespace(textSelection(True,a,'doi'),'doi')
    url = dewhitespace(textSelection(True,a,'link'),'link')
    number = dewhitespace(textSelection(True, a, 'number'),'number')
    volume = dewhitespace(textSelection(True,a,'volume'), 'volume')
    page = dewhitespace(textSelection(True,a,'page'), 'page')
    citation = countAuthor(strname,True)+ '(' +year+month+ "). " +title+journal+ volume + number+ page + doi + url

    text.append((countAuthor(strname,False),strlocation))
    print citation




with open('a.csv', 'wb') as csvfile:

    writer = csv.writer(csvfile,  delimiter = ';')
    writer.writerow(['name','location','citation'])
    writer.writerows(text)

