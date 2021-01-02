#IMPORTS
import os
import requests
from bs4 import BeautifulSoup 


#DECLARATIONS
doislist = list()
filepath = os.getcwd()

#MAIN CODE

#GETTING THE FILE NAME WITH DOI LINKS
linksfile = input("Enter the name of the text file that contains the DOI links or enter the full file location: \n")
try:
    fileh = open(linksfile)
    for line in fileh :
        line = line.replace('DOI: ', '')
        line = line.strip()
        doislist.append(line)       
except:
    print("An Error occured, please check the file name/location")

for doi in doislist :
    print(doi)
totlinksinfile = len(doislist)
print("Number of links found in the file:", totlinksinfile)

#GETTING THE FOLDER NAME AND CREATING FOLDER FOR DOWNLOADS
foldrname = input("Enter the name of the folder to download the pdfs: \n")
if foldrname == "" :
    foldrname = "\\PDFs\\"
else:
    foldrname = "\\" + foldrname + "\\"
    
if not os.path.exists(filepath + foldrname):
    os.makedirs(filepath + foldrname)
print("Filepath for saving the pdfs: ", filepath + foldrname)

#GET THE DOI FILES
for doi in doislist:
    
    #ACCESSING THE LINKS
    try:
        url="https://sci-hub.se/"+ doi
        response = requests.get(url).text
        soup = BeautifulSoup(response, 'html.parser')
        
        #GET TITLE
        titl = soup.find("div", id ="citation").text
        
        #GET ARTICLE
        artcl = soup.find("iframe", id ="pdf")
        artlnk = artcl['src']
        artlnki = artlnk.rindex('f')
        artlnk = artlnk[0:artlnki+1:]
        artnami = artlnk.rindex('/')
        artname = artlnk[artnami+1::]
    except:
        print("ERROR with DOI: ",doi)
        continue
    
    #DOWNLOAD PDF
    try:
        with open(filepath + foldrname + artname, "wb") as file:
            response = requests.get(artlnk)
            file.write(response.content)
            print("RETRIEVED: ",artlnk, ", DOI :",doi)
    except:
        try:
            with open(filepath + foldrname + artname, "wb") as file:
                response = requests.get("https:"+artlnk)
                file.write(response.content)
                print("RETRIEVED: ","https:"+artlnk, ", DOI :",doi)
        except:
            print("ERROR: ",artlnk, ", DOI :",doi)
            os.remove(filepath + foldrname + artname)
            continue   
print("ALL DONE")
