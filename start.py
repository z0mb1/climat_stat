'''программа позволяет:
1. рассчитать количество дней за период наблюдений,
когда температура воздуха достигала определенного значения.
2. определить количество денй подряд, когда была зафиксирована указанная температура,
с указанием даты начального дня
3. получить статистику количества дней по годам
4. получить статистику по часам

результаты вычислений записываются в файлы формата .xls в папке output_files'''

#my modules
from file_operations.output import write_output_file
from file_operations.open_and_convert_file import open_and_convert, find_available_date
from basic_calculations import TempAnalysis
from time import strftime

def day_temp_result(days_dict):
    result = []
    for k in sorted(days_dict.keys()):
        result.append([k.strftime('%d.%m.%Y'), days_dict[k]])
    result.insert(0, ['Дата', 'Температура'])
    return result

month_dict = {1: 'январь',
              2: 'февраль',
              3: 'март',
              4: 'апрель',
              5: 'май',
              6: 'июнь',
              7: 'июль',
              8: 'август',
              9: 'сентбрь',
              10: 'октябрь',
              11: 'ноябрь',
              12: 'декабрь'}

def make_result(filename, required_temperature, first_year, last_year, first_month, last_month, min_or_max, time_interval):
    # подготовка входного файла в формат {'день': [список зафиксированных температур], ...}
    days_dict = open_and_convert(filename, first_year, last_year, first_month, last_month)
    
    # подготовить словарь для анализа только максимальной температуры
    if min_or_max == 'max':
        days_dict_result = {k: max(v) for k, v in days_dict.items()}
    elif min_or_max == 'min':
        days_dict_result = {k: min(v) for k, v in days_dict.items()}
    
    '''for k in sorted(day_dict.keys())[:30]:
        print(k, day_temp[k])'''
    
    # записать результат минимум/максимуум температур
    write_output_file(day_temp_result(days_dict_result), 
                      '1_{}_суточная_температура'.format('максимальная' if min_or_max == 'max' else 'минимальная'), '')
    
    # подготовка результатов для списка значений температур
    text_result = []
    for t in required_temperature:
        
        TempStat = TempAnalysis(days_dict, days_dict_result, t, min_or_max, time_interval)
        
        write_output_file(TempStat.day_temp_intervals, '2_интервалы_температур_{}'.format(min_or_max), t)
        write_output_file(TempStat.days_per_year, '3_количество_дней_по_годам_{}'.format(min_or_max), t)
        write_output_file(TempStat.hours_per_day , '4_количество_часов_по_дням_{}'.format(min_or_max), t)
        write_output_file(TempStat.hours_per_day_summary, '5_статистика_по_количеству_часов_{}'.format(min_or_max), t)
        
        # форматирование результата для вывода в текстовое поле приложения
        text_result.extend(['\n'+'-'*60,
                            '\nРезультаты расчета для температуры {} и равной {} град\n'.format('больше' if min_or_max == 'max' else 'меньше', t),
                            'С {} по {} год, для периода {} - {}\n'.format(first_year, last_year, month_dict[first_month], month_dict[last_month]),
                            '-'*60+'\n',
                            'Максимльная температура {} град С\n'.format(TempStat.max_temp),
                            'Минимальная температура {} град С\n'.format(TempStat.min_temp),
                            '-'*30+'\n'])
        # Добавление статистики по годам
        for line in TempStat.days_per_year[1:-2]:
            if type(line[0]) == int:
                text_result.append('В {} году {} дн.\n'.format(line[0], line[1]))
            else:
                text_result.append('{} {} дн.\n'.format(line[0], line[1]))
        text_result.append('-'*30)

        # Добавление часовой статистики
        for line in TempStat.hours_per_day_summary:
            if len(line) == 1:
                text_result.append('\n{}\n'.format(line[0]))
            elif len(line) == 2:
                text_result.append('{}: {}\n'.format(line[0], line[1]))
    
    return ''.join(text_result)
    




if __name__ == '__main__':
    # Настройки
    # Файл, в котором в первой колонке дата формата дд.мм.ГГГГ, во второй - температура, заголовки удалить
    filename = '/home/zmb/python_projects/climate_stat/input_files/spb.xls'
    # Интересуемое значение температуры
    required_temperature = [19, 22]
    #['19', '22.5', '27.5', '31']
    #Интервал годов
    first_year = 2012
    last_year = 2016
    first_month = 6
    last_month = 8
       
    min_or_max = 'max'
    time_interval = 3
    
    print(make_result(filename, required_temperature, first_year, last_year, first_month, last_month, min_or_max, time_interval))
    
'''для преобразования csv файла в excel:
данные - из текста - выбрать необходимый файл - импорт -
шаг 1:  Укажите формат данных - с разделителями
шаг 2: Символом разделителем является - запятая
готово - ок '''
