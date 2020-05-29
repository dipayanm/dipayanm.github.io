import csv
csvFile = "meets.csv"
csv_path = "meets.csv"
table = ''
with open(csv_path) as csvFile:
    reader = csv.DictReader(csvFile, delimiter=';')
    table = '<tr>{}</tr>'.format(''.join(['<td>{}</td>'.format(header) for header in reader.fieldnames]))
    for row in reader:
        table_row = '<tr>'
        for fn in reader.fieldnames:
            table_row += '<td>{}</td>'.format(row[fn])
        table_row += '</tr>'
        table += table_row

out = open("tab-1.html","w")
out.write(table)
out.close()
