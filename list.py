import arxiv
import csv
import os
import json
import pandas as pd
from json2html import *

print("Downloading raw data from google sheet")
os.system("wget https://docs.google.com/spreadsheets/d/1TqHu0Q3Fcvr1TxBKBN9V8zT78Wj9VFD9gbwj6Vt-c-I/gviz/tq\?tqx\=out:csv\&sheet\=Sheet1 -O list.csv")
data = pd.read_csv("list.csv",dtype=str)
papers = []

print("Creating JSON entry for the assignments")

for j in data.columns:
    if j!="Date":
        for m in range(len(data)):
            ppd = map(str.strip, str(data[j][m]).split(','))
            ppd = [ppd_l for ppd_l in ppd if ppd_l != 'nan']
            for k in ppd:
                Q = arxiv.query(id_list=[k])
                print("New entry for "+Q[0].get('title').replace("\n", "").replace("  "," ")+"\n")
                ppda = {"ID": k, "Date": data["Date"][m],"Title":Q[0].get('title').replace("\n", "").replace("  "," "),"Authors":Q[0].get('authors'), "url":"<a href='"+Q[0].get('links')[0].get('href')+"' target='_blank'>Link</a>", "For":j}
                papers.append(ppda)



# print(papers)

json_db = json.dumps(papers, indent=4, sort_keys=True)

print("Creating HTML table")
print(json_db)
with open('out.json', 'w') as fout_json:
    fout_json.write(json_db)



fout = open('assignments.html', 'w')
papersfile = open("out.json","r")
json_list = json.loads(papersfile.read())
papersfile.close()

date_list = data['Date'].tolist()  


for i in reversed(date_list):
    fout.write("<h1 class='menu'>"+i+"</h1><table  style='margin-bottom: 3cm' class='table table-striped'>")
    fout.write("<tr><th>Assigned to</th><th>Title</th><th>Author(s)</th><th>ArXiv ID</th><th>ArXiv link</th></tr>")
    for j in json_list:
        if j["Date"] ==  i:
            authors = "<ul>"
            for au in j["Authors"]:
                authors += "<li>" 
                authors += au
                authors += "</li>"
            authors += "</ul>"
            table = "<tr><td>"+j["For"]+"</td><td>"+j["Title"]+"</td><td>"+authors+"</td><td>"+j["ID"]+"</td><td>"+j["url"]+"</tr>" 
            fout.write(table)
    fout.write("</table>")


fout.close()

# os.system("cp assignments.html ../git-page/assignments.html")


print("Done! Preparing for GIT commit")
yes = input("Enter y to commit:\t")
if yes=="y":
    os.system("git add .")
    os.system("git commit -m 'New Assignments'")
    os.system("git push origin master")
