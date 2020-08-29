import csv
# csvFile = "current.csv"
# csv_path = "current.csv"
csvFile = "monsoon2020.csv"
csv_path = "monsoon2020.csv"
table = ''
with open(csv_path) as csvFile:
    reader = csv.DictReader(csvFile, delimiter=',')
    table = '<tr>{}</tr>\n'.format(''.join(['<td>{}</td>\n'.format(header) for header in reader.fieldnames]))
    for row in reader:
        table_row = '<tr>'
        for fn in reader.fieldnames:
            table_row += '<td>{}</td>\n'.format(row[fn])
        table_row += '</tr>\n'
        table += table_row

out = open("monsoon2020.html", "w")
out.write(table)
out.close()
