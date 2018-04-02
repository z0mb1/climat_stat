#import csv
import xlwt

def write_output_file(data, name, t):
    '''Запись в файл
        данные передаются в виде списка, каждый элемент которого помещается в отдельную строку'''

    filename = 'output_files/{}_{}град.xls'.format(name, str(t).replace('.', '_'))
    book = xlwt.Workbook('utf8')
    sheet = book.add_sheet('result')
    
    row = 0
    for dataline in data:
        col = 0
        for d in dataline:
            sheet.write(row, col, d)
            col += 1
        row += 1
    book.save(filename)
    
    ''' #for csv output
    filename = 'output_files/{}_{}град.csv'.format(name, str(t).replace('.', '_'))
    output_file = open(filename, 'w')
    wrtr = csv.writer(output_file)
    for day in data:
        wrtr.writerow(day)
    output_file.close()'''
