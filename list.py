#!/usr/bin/env python3
"""
This is a very unsophisticated code to generate static git pages from google sheet entries.
Please do not take it seriously. d.
"""
import arxiv
import os
import json
import pandas as pd


# Fancy colors
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


print(bcolors.WARNING + "Downloading data from google sheet" + bcolors.ENDC)
os.system("wget -q https://docs.google.com/spreadsheets/d/1T2TxmiCEq4Vs1g5RhN5_xfWbQqWLMo08J0AxkkvF4R0/gviz/tq\?tqx\=out:csv\&sheet\=Sheet1 -O list.csv")
entry = int(input("Enter n for last n entries:\t"))
data0 = pd.read_csv("list.csv", dtype=str)
data = data0.iloc[:, -entry:]
papers = []
people = {"j": "Jaffino", "hm": "Himanshu", "a": "Ankit",
          "d": "Dipayan", "h": "Harkirat", "k": "Kinjalk",
          "e": "★Everyone", "v": "Vikram", "db": "Debottam"}


print(bcolors.WARNING + "Creating JSON entry for the assignments" + bcolors.ENDC)

for j in data.columns:
    for k in data[j]:
        k = str(k)
        aamulti = "a"
        if k != 'nan':
            # print(type(k))
            ppd =k.split('|')
            # ppd = [ppd_l for ppd_l in ppd if ppd_l != 'nan']
            print(bcolors.WARNING + "Entry for\t{}".format(ppd[0]) + bcolors.ENDC)
            Q = arxiv.query(id_list=[ppd[0]])
            a_t = ppd[1].split(',')
            comment = ""
            if len(ppd) > 2:
                comment = ppd[2].replace("\n", "")
            if len(a_t) > 1:
                aamulti = "b" 
            for_l = [people[pp] for pp in a_t]
            ppda = {"ID": ppd[0], "Title":Q[0].get('title').replace("\n", "").replace("  "," "),
                    "For": for_l, "Aamulti": aamulti, "Authors":Q[0].get('authors'),
                    "url": "<a href='"+Q[0].get('links')[0].get('href')+"' target='_blank'>Link</a>",
                    "Comment": comment, "Date": j}
            papers.append(ppda)

# print(papers)

json_db = json.dumps(papers, indent=4, sort_keys=True)

print("Creating HTML table")
# # print(json_db)
with open('out.json', 'w') as fout_json:
    fout_json.write(json_db)

fout = open('tmp.html', 'w')
papersfile = open("out.json", "r")
json_list_t = json.loads(papersfile.read())
json_list = sorted(json_list_t, key = lambda i: i['For'])
papersfile.close()

date_list = data.columns.tolist()

for i in reversed(date_list):
    fout.write("<h1 class='menu'>"+i+"</h1>\n<table  style='margin-bottom: 3cm' class='table table-striped'>\n")
    fout.write("<tr><th>Assigned to</th><th>Title</th><th>Author(s)</th><th>ArXiv ID</th><th>Comments</th><th>ArXiv link</th></tr>\n")
    for j in json_list:
        if j["Date"] == i:
            if j["Aamulti"] == "a":
                authors = "<ul>"
                for au in j["Authors"]:
                    authors += "<li>"
                    authors += au
                    authors += "</li>"
                authors += "</ul>\n"
                a_ts = "<ul>"
                for a_t in j["For"]:
                    a_ts += "<li>"
                    a_ts += a_t
                    a_ts += "</li>"
                a_ts += "</ul>\n"

                table = "<tr><td>"+a_ts+"</td><td>" + \
                    j["Title"]+"</td><td>"+authors+"</td><td>" + \
                    j["ID"]+"</td><td>"+j["Comment"]+"</td><td>"+j["url"]+"</tr>\n"
                fout.write(table)

    for j in json_list:
        if j["Date"] == i:
            if j["Aamulti"] == "b":
                authors = "<ul>"
                for au in j["Authors"]:
                    authors += "<li>"
                    authors += au
                    authors += "</li>"
                authors += "</ul>\n"
                a_ts = "<ul>"
                for a_t in j["For"]:
                    a_ts += "<li>"
                    a_ts += a_t
                    a_ts += "</li>"
                a_ts += "</ul>\n"

                table = "<tr><td>"+a_ts+"</td><td>" + \
                    j["Title"]+"</td><td>"+authors+"</td><td>" + \
                    j["ID"]+"</td><td>"+j["Comment"]+"</td><td>"+j["url"]+"</tr>\n"
                fout.write(table)
    fout.write("</table>\n")
fout.write("\n")
fout.close()

with open('tmp.html', 'r') as new_stuff:
    newdata = new_stuff.read()
with open('assignments.html', 'r') as original:
    olddata = original.read()
with open('assignments.html', 'w') as modified:
    modified.write(newdata + olddata)

print(bcolors.OKGREEN + "Done! Preparing for GIT commit" + bcolors.ENDC)
os.system("notify-send 'Git commit' 'Enter commit response in the terminal'")

yes = input("Enter y to commit:\t")

if yes == "y":
    os.system("git add .")
    os.system("git commit -m 'New Assignments'")
    os.system("git push origin master")
    print(bcolors.OKGREEN + "Done! Website updated!" + bcolors.ENDC)
else:
    print(bcolors.OKGREEN + "Done!" + bcolors.ENDC)
