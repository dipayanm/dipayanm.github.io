from json2html import *
import json
import csv
import pandas as pd

papers = open("out.json","r")
json_list = json.loads(papers.read())
# table = json2html.convert(json = json_list, table_attributes="class='table table-striped'",escape=False )
# print(json_list[0])

data = pd.read_csv("list.csv",dtype=str)
# print(data)
date_list = data['Date'].tolist()  

# for i in data[['']]:
#     date_list.append(i)

# print(date_list)

for i in reversed(date_list):
    print("<h1 class='menu'>"+i+"</h1><table  style='margin-bottom: 3cm' class='table table-striped'>")
    print("<tr><th>Assigned to</th><th>Title</th><th>Author(s)</th><th>ArXiv ID</th><th>ArXiv link</th></tr>")
    for j in json_list:
        if j["Date"] ==  i:
            authors = "<ul>"
            for au in j["Authors"]:
                authors += "<li>" 
                authors += au
                authors += "</li>"
            authors += "</ul>"
            table = "<tr><td>"+j["For"]+"</td><td>"+j["Title"]+"</td><td>"+authors+"</td><td>"+j["ID"]+"</td><td>"+j["url"]+"</tr>" 
            print(table)
    print("</table>")
