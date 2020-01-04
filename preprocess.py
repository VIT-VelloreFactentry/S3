from pdf2image import convert_from_path
import pytesseract
from date_extractor import extract_dates
import glob
import os
import shutil

path = "/home/rosguy/AIML_PDF/CA136375CR16.pdf"
pages = convert_from_path(path,500)


for filename in glob.glob("/home/rosguy/AIML_PDF/*"):
    if("pdf" in filename):
        p_counter=1
        f_name = filename.split("/")[-1].split(".")[0]
        path_save = "/home/rosguy/AIML_PDF/"+f_name
        os.makedirs(path_save)
        pages = convert_from_path(filename,500)
        for page in pages:
            s_name = f_name+"/Page_"+str(p_counter)+".jpg"
            page.save(s_name,"JPEG")
            p_counter+=1
   
p_counter=1
os.makedirs("/home/rosguy/AIML_PDF/CA136375CR16")

for page in pages:
    s_name = "/home/rosguy/AIML_PDF/CA136375CR16"+"/Page_"+str(p_counter)+".jpg"
    page.save(s_name,"JPEG")
    p_counter+=1
           

def listtoLower(ls):
    for i in range(len(ls)):
        ls[i] = ls[i].lower()
    return ls
   
def date_extract(ls):
    date = []
    for i in ls:
        if "issue date" in i:
            print(i)
            doc = nlp(i)
            for j in doc.ents:
                if j.label_=="DATE":
                    print(j)
                    date.append(j)
    return date
       

date_list = []
for filename in glob.glob("/home/rosguy/AIML_PDF/CA136375CR16/*"):
    print(filename)
            
    text = pytesseract.image_to_string(filename)
    ls = text.split("\n")
    ls = listtoLower(ls)
    temp_list = date_extract(ls)
    date_list.extend(temp_list)
    




    
import spacy
nlp = spacy.load('en_core_web_sm')

        
       


date = str(date[0].date())



