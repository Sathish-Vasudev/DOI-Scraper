#IMPORTS
import os
import requests
import pandas as pd
from bs4 import BeautifulSoup 


#DECLARATIONS
doislist = list()
doislistf = list()
titlelist = list()
filelist = list()
filepathlist = list()
urllist = list()
filepath = os.getcwd()

#FUNCTIONS
#PRINTLINKS FUNCTION
def printlinks(strt,stp):
    print("\nThe URLs to process are as follows:")
    Linkcount = 0
    for l in doislist[strt:stp]:
        Linkcount = Linkcount + 1
        print(Linkcount, l)

#MAIN CODE
while True:
    
    #GETTING THE FILE NAME WITH DOI LINKS
    linksfile = input("Enter the name of the text file that contains the DOI links or enter the full file location: \n")
    doislist.clear()
    titlelist.clear()
    try:
        fileh = open(linksfile)
        for line in fileh :
            line = line.replace('DOI: ', '')
            line = line.strip()
            doislist.append(line)
    except:
        print("An Error occured, please check the file name/location")
    totlinksinfile = len(doislist)
    print("Number of links found in the file:", totlinksinfile)

    #GETTING NUMBER OF LINKS TO PROCESS
    noflinks2process = input("\nHow many links from the first would you like to process? \n[Use N or N-N Format or Use 'A' for All Links(Time Consuming, More Computation)] \n")
    n2nfrmt = noflinks2process.find("-")
    if n2nfrmt == -1 :
        if noflinks2process == 'A':
            nofl2pstrt = 0
            nofl2pstp = len(linkslist)
            print("The number of links to be processed is" ,nofl2pstp)
            printlinks(0,nofl2pstp)
        elif int(noflinks2process) < totlinksinfile:
            nofl2pstrt = 0
            nofl2pstp = int(noflinks2process)
            print("The number of links to be processed is" ,nofl2pstp)
            printlinks(0,nofl2pstp)
        elif int(noflinks2process) == len(linkslist):
            nofl2pstrt = 0
            nofl2pstp = int(noflinks2process)
            print("The number of links to be processed is" ,nofl2pstp)
            printlinks(0,nofl2pstp)
        else:    
            print("ERROR: The number of links provided are greater than the number of links in the file.")
            continue
    else:
        nofl2pstrt = int(noflinks2process[0:n2nfrmt])
        nofl2pstp = int(noflinks2process[n2nfrmt+1:len(noflinks2process)])
        if nofl2pstp < nofl2pstrt:
            print("ERROR: The number of links to stop the process is less than the number of link to start the process.")
            continue
        elif nofl2pstrt == 1:
            nofl2pstrt = 0
            print("Start of the link to process is", int(nofl2pstrt))
            print("End of the link to process is", int(nofl2pstp))
            printlinks(nofl2pstrt,nofl2pstp)
        else:    
            print("Start of the link to process is", int(nofl2pstrt))
            print("End of the link to process is", int(nofl2pstp))
            printlinks(nofl2pstrt,nofl2pstp)

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
    selecteddois = doislist[nofl2pstrt:nofl2pstp]
    for doi in selecteddois:
    
        #ACCESSING THE LINKS
        try:
            url="https://sci-hub.se/"+ doi
            response = requests.get(url).text
            soup = BeautifulSoup(response, 'html.parser')
            
            #GET TITLE
            titl = soup.find("div", id ="citation").text
            titlelist.append(titl)
            
            #GET ARTICLE
            artcl = soup.find("iframe", id ="pdf")
            artlnk = artcl['src']
            artlnki = artlnk.rindex('f')
            artlnk = artlnk[0:artlnki+1:]
            artnami = artlnk.rindex('/')
            artname = artlnk[artnami+1::]
            filelist.append(artname)
            doislistf.append(doi)
        except:
            print("ERROR with DOI: ",doi)
            continue
    
        #DOWNLOAD PDF
        try:
            with open(filepath + foldrname + artname, "wb") as file:
                response = requests.get(artlnk)
                file.write(response.content)
                print("RETRIEVED: ",artlnk, ", DOI :",doi)
                urllist.append(artlnk)
                filepathlist.append(filepath + foldrname + artname)
        except:
            try:
                with open(filepath + foldrname + artname, "wb") as file:
                    response = requests.get("https:"+artlnk)
                    file.write(response.content)
                    print("RETRIEVED: ","https:"+artlnk, ", DOI :",doi)
                    urllist.append("https:"+artlnk)
                    filepathlist.append(filepath + foldrname + artname)
            except:
                print("ERROR: ",artlnk, ", DOI :",doi)
                os.remove(filepath + foldrname + artname)
                continue   

    print("Generating Excel file...")
    dat = {'DOI':doislistf,'TITLE':titlelist,'URL':urllist,
       'FILE NAME':filelist,'FILE PATH':filepathlist}
    datf = pd.DataFrame(dat,columns = ['DOI','TITLE','FILE NAME','URL','FILE PATH'])
    excelw = pd.ExcelWriter(filepath + foldrname + "downloadedfiles.xlsx", engine='xlsxwriter')
    datf.to_excel(excelw,sheet_name='Sheet1',index = False)
    workbook = excelw.book
    worksheet =  excelw.sheets['Sheet1']
    format = workbook.add_format({'text_wrap': True,'valign':'vcenter', 'align':'center','font_size':12})
    worksheet.set_column('A:A', 15, format)
    worksheet.set_column('B:E',35,format)
    excelw.save()
    print("ALL DONE")
