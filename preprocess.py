from pdf2image import convert_from_path

from date_extractor import extract_dates
import glob
import os
import shutil
import spacy
import re
import PyPDF2


def listtoLower(ls):
    '''
    Function to convert list of words to lower case
    :param ls: list of words
    :return: list of words in lower case
    '''
    for i in range(len(ls)):
        ls[i] = ls[i].lower()
    return ls


def date_extract(ls):
    '''
    Function to extract dates from a list of words
    :param ls: list of words
    :return: dates extracted via two sources
    '''
    date_ner = []
    date_extractor = []
    for i in ls:
        if "issue date" in i:
            print(i)
        dates = extract_dates(i)
        if (len(dates) != 0):
            print("Date Extractor:", str(dates[0].date()))
            date_extractor.append(dates[0])
        doc = nlp(i)
        for j in doc.ents:
            if j.label_ == "DATE":
                print("Issue date: ",j)
                date_ner.append(j)

    return date_ner, date_extractor

if __name__=="__main__":
    filename = 'US17324CED48.pdf'
    pdfFileObj = open(filename, 'rb')

    # creating a pdf reader object
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    # printing number of pages in pdf file
    #print(pdfReader.numPages)

    # creating a page object
    nlp = spacy.load('en_core_web_sm')


    ## Define regex for cusip
    regex = "[0-9]{5}[a-z]{3}[0-9]{1}"





    flag = 0
    flag_issue = 0
    date_list = []

    for i in range(pdfReader.numPages):
        pageObj = pdfReader.getPage(i)
        text = pageObj.extractText()

        ls = text.split("\n")
        #print(ls)
        for word in  ls:
            if (flag == 0):
                date = extract_dates(word)
                #if(len(date)>0):
                #    print("Doc date: ",date)
                doc = nlp(word)
                for j in doc.ents:
                    if j.label_ == "DATE":
                        print("DOC DATE:",j)
                        date_list.append(j)
                        flag = 1
                        #date_ner.append(j)
                        break


        ls = listtoLower(ls)
        for index in range(len(ls)):
           if("issue date" in ls[index]):
               #print(ls[index])
               #temp_list_ner, temp_list_extract = date_extract(ls[index+1:index+5])
               for i in ls[index+1:index+5]:
                   doc = nlp(i)
                   if(flag_issue==1):
                       break
                   for j in doc.ents:
                       if j.label_ == "DATE":
                           print("Issue date: ", j)
                           date_list.append(j)
                           if(len(j)>0):
                                #date_ner.append(j)
                                print("Issue Date: ",j)
                                date_list.append(j)
                                flag_issue = 1
                                break






        for i in ls:

            if len(re.findall(regex,i))>0:
                print("CUSIP: ",re.findall(regex, i))

    print("All the dates found: ",date_list)



    # closing the pdf file object
    pdfFileObj.close()



