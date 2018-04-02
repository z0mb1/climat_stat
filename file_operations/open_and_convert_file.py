from datetime import datetime
import xlrd
import re

def open_and_convert(filename, first_year, last_year, first_month, last_month):
    '''подготовка входного файла в формат {'д.м.г': [список зафиксированных температур], ...} '''
    rb = xlrd.open_workbook(filename, formatting_info=True)
    sheet = rb.sheet_by_index(0)
    days_temp = {}
    for rownum in range(sheet.nrows):
        row = sheet.row_values(rownum)
        date_find = re.search(r'\d{2}[./-]\d{2}[./-]\d{4}', row[0])
        if date_find:
            day = datetime.strptime(date_find.group(), '%d.%m.%Y').date()
        if day.year >= first_year and day.year <= last_year and day.month >= first_month and day.month <= last_month:
            if not days_temp.get(day):
                days_temp[day] = []
            if row[1]:
                days_temp[day].append(float(row[1]))
    return(days_temp)
    
def find_available_date(filename):
    ''' определение доступного диапазона годов и месяцев'''
    rb = xlrd.open_workbook(filename, formatting_info=True)
    sheet = rb.sheet_by_index(0)
    available_years = []
    available_months = []
    for rownum in range(sheet.nrows):
        row = sheet.row_values(rownum)
        if row[0]:
            date_find = re.search(r'\d{2}[./-]\d{2}[./-]\d{4}', row[0])
            day = datetime.strptime(date_find.group(), '%d.%m.%Y').date()
            if day.year not in available_years:
                available_years.append(day.year)
            if day.month not in available_months:
                available_months.append(day.month)

    return(available_years, available_months)
            
       

if __name__ == '__main__':
    settings = {'filename': '/home/zmb/python_projects/climate_stat/input_files/spb.xls',
                'first_year': 2015,
                'last_year': 2017,
                'first_month': 7,
                'last_month': 7}
                
    #open_and_convert test
    days_temp = open_and_convert(**settings)
    for k in sorted(days_temp.keys())[:100]:
        print(k, days_temp[k])
        
    #find_available_date test
    print(find_available_date(settings['filename']))
