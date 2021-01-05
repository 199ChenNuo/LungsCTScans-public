import xlwt

f = open('similarity.txt', encoding='utf-8')

output = 'data.xls'

sheetName = 'sheet3'

start_row = 0
start_col = 1

wb = xlwt.Workbook(encoding = 'utf-8')
ws = wb.add_sheet(sheetName, cell_overwrite_ok=True)

count = 0
row_excel = start_row
for line in f:
    if count == 5:
        count = 0
    line = line.strip('\n')
    line = line.split(' ')
    # file name
    if (count == 0):
        ws.write(row_excel, 1, line[0])
    # both_count
    if (count == 1):
        ws.write(row_excel, 3, line[1])
    # count
    if count == 2:
        ws.write(row_excel, 5, line[1])
    # truth count
    if count == 3:
        ws.write(row_excel, 1, line[1])
    # result count
    if count == 4:
        ws.write(row_excel, 2, line[1])
        row_excel += 1
    wb.save(output)
    count += 1  

f.close()



