from pdf2image import convert_from_path
import pytesseract
from date_extractor import extract_dates
import glob
import os
import shutil
import spacy
nlp = spacy.load('en_core_web_sm')


path = "/home/rosguy/AIML_PDF/US17324CED48.pdf"
pages = convert_from_path(path,500)

folder_name = path.split("/")[-1].split(".")[0]



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
os.makedirs("/home/rosguy/AIML_PDF/"+folder_name)

for page in pages:
    s_name = "/home/rosguy/AIML_PDF/"+folder_name+"/Page_"+str(p_counter)+".jpg"
    page.save(s_name,"JPEG")
    p_counter+=1
           

def listtoLower(ls):
    for i in range(len(ls)):
        ls[i] = ls[i].lower()
    return ls
   
def date_extract(ls):
    date_ner = []
    date_extractor = []
    for i in ls:
        if "issue date" in i:
            print(i)
            dates = extract_dates(i)
            if(len(dates)!=0):
                print("Date Extractor:",str(dates[0].date()))
                date_extractor.append(dates[0])
            doc = nlp(i)
            for j in doc.ents:
                if j.label_=="DATE":
                    print(j)
                    date_ner.append(j)
    
    return date_ner,date_extractor
       

date_list = []
for filename in glob.glob("/home/rosguy/AIML_PDF/"+folder_name+"/*"):
    print(filename)
            
    text = pytesseract.image_to_string(filename)
    ls = text.split("\n")
    ls = listtoLower(ls)
    temp_list_ner,temp_list_extract = date_extract(ls)
    if(len(temp_list_ner)!=0 and len(temp_list_extract)!=0):
        date_list.append([temp_list_ner,temp_list_extract])
    
print(date_list)    




    

        
       




