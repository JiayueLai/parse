# -*- coding: utf-8 -*-
import sys
import re
import csv
import bibtexparser
from bibtexparser.bparser import BibTexParser
reload(sys)
sys.setdefaultencoding('utf8')

bibtex_str = ''
text = []
name = '' # name to add in the citation
strname = '' # names of all authors in one entry
location = ''  # the first location
strlocation = ''  # all locations in one entry
citation =''
author =''  # info in the author column

parser = BibTexParser()
with open('SPIM Bib file.bib') as bibtex_file:
    bibtex_str = bibtex_file.read()
output = bibtexparser.loads(bibtex_str)


def textSelection(a,str):
    '''
    This method is used to check whether the return value from regEx
    can be used and extract the data in the entry
    :param str: matchObj, a: string a of each entry
    :return: value: string
    '''
    value = ''
    pattern = 'u\W' + str + '\W\:\su\'(.*?)\','
    reg = re.search(pattern, a, re.M)
    if reg is not None:
        value = reg.group(1)
        value = special(value)
    return value


def createAuthorCol(str):
    '''
    create the information for author column
    format: author 1 , author 2 , author 3 ,...., last author
    problem: since original text is concatenated by ' and ',
    after spliting and joining, how to remove white space around ','???
    :param str:string of names
    :return: expected format in string
    '''

    list = str.split('and')
    if len(list) > 3:
        authors = list[0:2]
        authors.append('...')
        authors.append(list[-1])
        authors = 'and'.join(authors)
    else:
        authors = 'and'.join(list)

    authors = authors.split(',')
    authors = ''.join(authors)
    authors = authors.split(' and')
    authors = ','.join(authors)
    authors = authors.replace('\\n', ' ')

    return authors


def locationCol(str):
    '''
    split and merge until only one location left.
    also remove email addr and number in the location
    :param str: string of all locations
    :return: list: string
    '''
    list = str.split('\n')
    list = list[0]
    list = list.split(';')
    list = list[0]
    list = list.split('.')
    list = list[0]
    list = ''.join(list)
    list = list.replace('\\n', ' ')
    #remove numbers
    list = list.split(',')
    list = ','.join([i for i in list if not any(c.isdigit() for c in i)])
    list = special(list)
    return list


def count(str):
    '''
    author name > 3, plus et al in citation.
    :param str:
    :return: output string
    '''
    result = ''
    str = str.replace('\\n', ' ')
    lis = str.split(' and ')
    result = lis[0:3]
    result =','.join(result)
    result =result.split(',')
    i = 0

    for i in range(0, len(result)):
        if (i % 2 == 0):
            result[i] = result[i]
        elif (i == len(result)-3):
            try:
                result[i] = result[i][1]+"., & "
            except:
                result[i] = result[i]
        else:
            try:
                result[i] = result[i][1]+"."
            except:
                result[i] = result[i]
    result = ', '.join(result)
    result = re.sub('\&\s\,', '&', result)
    if len(lis) > 3:
        result += " et al."
    return result

def special(str):
    '''
    replace special char in the string
    :param str: string
    :return: str
    '''
    char = ''
    dict1 ={
        'u': 'ü',
        'a': 'ä',
        'o': 'ö'
    }
    Italian ={
        'e': 'è',
        'a': 'à',
        'i': 'ì',
        'o': 'ò',
        'u': 'ù'
    }

    for i in (0,2):
        match = re.search('[\\\][\\\]\`\{(\w)\}',str)
        if match:
            char = match.group(1)
            str = re.sub('[\\\][\\\]\`\{['+char+']\}', Italian[char], str)

    str = re.sub('[\\\][\\\][\\\]\'\{[e]\}', 'é', str)  # german char
    for i in (0,3):
        match = re.search('\{[\\\]*\"\{(\w)[\}]*',  str)
        if match:
            char = match.group(1)
            try:
                str = re.sub('\{[\\\]*\"\{['+char+'][\}]*', dict1[char], str)
            except:
                return
    str = re.sub('[\\\][\\\]','',str)
    return str

def generator(a):
    journal =''
    year = textSelection(a, 'year')
    month = textSelection(a, 'month')
    month = re.match(r'([a-z]*)', month, re.M)
    month = month.group(1)
    if (month):
        month = ', ' + month
    title = textSelection(a, 'title')
    if (title):
        title = title +'. '
    journal = textSelection(a, 'journal')
    if (journal):
        journal = journal +', '
    volume = textSelection(a, 'voulme')
    if (volume):
        volume = volume  +', '
    page = textSelection(a, 'pages')
    if (page):
        page = page + ', '
    url = textSelection(a, 'link')
    if (url):
        url = "Retrieved from: "+ url
    doi = textSelection(a, 'doi')
    if (doi):
        doi  = doi+'. '
    citation = '(' + year + month + "). " + title+ journal + volume + page + doi + url

    return citation

for i in output.entries_dict:
    a = output.entries_dict[i]
    a = str(a) # get information of each entry
    strname = textSelection(a,'author')
    if strname is not None:
        author = createAuthorCol(strname) # info in the first col
        name = count(strname)
    citation = name+generator(a)
    strlocation = textSelection(a, 'affiliation')
    location = locationCol(strlocation) # info in the second col
    print(citation)

    if author and location and citation:
        text.append((author, location, citation))


with open('a.csv', 'wb') as csvfile:

    writer = csv.writer(csvfile,  delimiter = ';')
    writer.writerow(['author','location', 'citation'])
    writer.writerows(text)
