import csv
# csvFile = "current.csv"
# csv_path = "current.csv"
csvFile = "spring2020.csv"
csv_path = "spring2020.csv"
table = ''
with open(csv_path) as csvFile:
    reader = csv.DictReader(csvFile, delimiter=',')
    table = '<tr>{}</tr>'.format(''.join(['<td>{}</td>'.format(header) for header in reader.fieldnames]))
    for row in reader:
        table_row = '<tr>'
        for fn in reader.fieldnames:
            table_row += '<td>{}</td>'.format(row[fn])
        table_row += '</tr>'
        table += table_row

out = open("spring.html","w")
out.write(table)
out.close()
