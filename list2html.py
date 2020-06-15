from json2html import *
import json

papers = open("out.json","r")
json_list = json.loads(papers.read())
table = json2html.convert(json = json_list, table_attributes="class='table table-striped'",escape=False )
print(table)
