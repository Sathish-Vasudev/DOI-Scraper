# DOI-Scraper
This program can be used to get educational articles/papers from internet with an input of set DOI links in a text file. The retrieved data can be downloaded in a specified folder. The downloaded files and their details are saved in an **Excel file**. This program uses ***Beautifulsoup*** to get response from ***Sci-Hub*** site.

## DOI-Scraper v1
This program allows the user to get educational articles/papers from internet and download the pdf files to a mentioned folder.<br/> The input is given in the form of a text file containing **DOI links** ***(one link per line)***. The output details are recorded in an **Excel file**.
The following details are retrieved and recorded in the process:
1. DOI
2. Title
3. Author
4. Publisher
5. Year
6. URL
7. File Name
8. File Path
9. Citation

#### INSTRUCTIONS
1. Collect the DOIs of the articles you want to obtain and list them one DOI per line in a Text file *(*.txt)*.
2. Now, initiate the program. Provide the location or the name of the text file that contains the DOIs.
3. Select a set of DOI links to process or select all depending upon your need. Larger number of <br/>DOIs *(i.e. >10)* might take longer. So, it is ideal to split and process. 
4. Provide a folder name where the pdf files can be downloaded ***(Currently a subfolder in the working directory)***.
5. Once the process is completed, the retrieved DOIs will be listed after downloading the same  <br/> to the given location.
6. The details of the downloaded files are stored in an **Excel file**.
