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
                ppda = {"id": k, "date": data["Date"][m],"title":Q[0].get('title').replace("\n", "").replace("  "," "),"authors":Q[0].get('authors'), "url":"<a href='"+Q[0].get('links')[0].get('href')+"' target='_blank'>Link</a>", "assigned_to":j}
                papers.append(ppda)



print(papers)

json_db = json.dumps(papers, indent=4, sort_keys=True)

print("Creating HTML table")
print(json_db)
with open('out.json', 'w') as fout:
    fout.write(json_db)
fout.close()



papers = open("out.json","r")
json_list = json.loads(papers.read())
table = json2html.convert(json = json_list, table_attributes="class='table table-striped'",escape=False )
# print(table)

with open('assignments.html', 'w') as fout:
    fout.write(table)
fout.close()

os.system("cp assignments.html ../git-page/assignments.html")

print("Done! Commit git to update website")
