from datetime import datetime, timedelta
from time import strftime

class TempAnalysis():
    ''' Класс включает в себя методы расчета статистики температуры 
        и методы представления полученной информации в формат для записи в excel'''
    def __init__(self, days_dict, days_dict_result, temperature, min_or_max, time_interval):
        # словарь формата {'д.м.г': [список зафиксированных температур], ...}
        self.days_dict = days_dict
        # рассматриваемые года
        self.years = list(range(sorted(days_dict.keys())[0].year, sorted(days_dict.keys())[-1].year+1))
        #print(self.years)
        # max
        self.max_temp = max(max(x) for x in self.days_dict.values())
        # min
        self.min_temp = min(min(x) for x in self.days_dict.values())
        # словарь формата {'д.м.г': максимальная(минимальная) температура, ...}
        self.days_dict_result = days_dict_result
        # температура, относительно которой проводятся расчеты
        self.t = temperature
        # настройка, определяющая характер расчета: поиск температур выше заданной (max) или ниже заданной (min)
        self.min_or_max = min_or_max
        # интервал измерения температуры (через какие промежутки времени представлены данные во входном файле)
        self.time_interval = time_interval
         
        # словарь формата {'день начала промежутка': 'количество дней в промежутке', ...}
        self.day_temp_intervals_dict = self.day_temp_intervals_count()
        # словарь формата {'год': 'количество дней', ...}
        self.days_per_year_dict = self.days_per_year_count()
        # список формата [['день', 'количество часов за день с температурой выше(ниже) указанной']...]
        self.hours_per_day_list = self.hours_per_day_count()
        
        #
        # представление результатов в виде списка для записи результатов в excel 
        #
        
        # список формата [['год'], ['дата начала промежутка', 'количество дней']
        self.day_temp_intervals = self.day_temp_intervals_result()
        # статистика по количеству дней за каждый год (за весь период, в среднем)
        self.days_per_year = self.days_per_year_result()
        # список формата [['день', 'количество часов за день'] , ...]
        # дата в отформатированном виде
        self.hours_per_day = self.hours_per_day_result()
        # часовая статистика
        self.hours_per_day_summary = self.hours_per_day_summary_count()

    def day_temp_intervals_count(self):
        '''Определяет промежутки дней, когда была зафиксирована указанная температура, с указанием даты начала периода
           на вход поступает словарь формата {'день': макс_темп , ...}
           на выходе словарь формата {'день начала промежутка': 'количество дней в промежутке', ...}'''
    
        # оставляем в словаре только дни с температурой равной и выше(ниже) заданной
        if self.min_or_max == 'max':
            days_dict = {k: v for k, v in self.days_dict_result.items() if v >= self.t}
        elif self.min_or_max == 'min':
            days_dict = {k: v for k, v in self.days_dict_result.items() if v <= self.t}
        
        result = {}
        if days_dict:
            current_day = sorted(days_dict.keys())[0]
            result[current_day] = 1
            for k in sorted(days_dict.keys()):
                day = k
                # если разность соседних дней равна промежутку текщего периода, увеличить промежуток на 1 день
                if day - current_day == timedelta(result[current_day]):
                    result[current_day] += 1
                # иначе начать новый промежуток, присвоить ему значение 1
                else:
                    result[day] = 1
                    current_day = day
        '''for k in sorted(result.keys()):
            print(k, result[k])'''
        return result

    def day_temp_intervals_result(self):
        ''' представление результатов в виде списка
         [['год'],
          ['дата начала промежутка', 'количество дней'],
         ...]'''
        days_result = []
        if self.day_temp_intervals_dict:
            current_year = sorted(self.day_temp_intervals_dict.keys())[0].year
            days_result.append([current_year])
            for k in sorted(self.day_temp_intervals_dict.keys()):
                if k.year != current_year:
                    current_year = k.year
                    days_result.append([current_year])
                days_result.append([k.strftime('%d.%m.%Y'), self.day_temp_intervals_dict[k]])
            #print(days_result)
        return days_result

    def days_per_year_count(self):
        '''Подсчет количества дней с заданной температурой за год и за весь период'''
        days_per_year_dict = dict.fromkeys(self.years, 0)
        # если список интервалов не пуст
        if self.day_temp_intervals_dict:
            for k in sorted(self.day_temp_intervals_dict.keys()):
                days_per_year_dict[k.year] = days_per_year_dict.get(k.year, 0) + self.day_temp_intervals_dict[k]
        return days_per_year_dict
    
    def days_per_year_result(self):
        ''' Представление статистики по годам в виде списка для записи в excel'''
        days_stat = []
        days_stat = [[k, self.days_per_year_dict[k]] for k in sorted(self.days_per_year_dict.keys())]
        all_days = sum([x[1] for x in days_stat])
        # все дни за период наблюдений с заданной температурой
        days_stat.append(['Всего за {} лет'.format(len(self.days_per_year_dict.keys())), all_days])
        # среднее значение за все года 
        average = all_days / len(self.days_per_year_dict.keys()) 
        days_stat.append(['В среднем', round(average, 1)])
        '''for x in days_stat:
            print(x)'''
        days_stat.insert(0, ['Год', 'Количество дней'])
        days_stat.append(['Максимальная температура', self.max_temp])
        days_stat.append(['Минимальная температура', self.min_temp])
        return days_stat
        
    def hours_per_day_count(self):
        '''Функция определения продолжительности температуры в течение суток с температурой выше/ниже и равной заданной
           на вход поступает словарь days_dict формата {'день': [список зафиксированных температур], ...}
           на выходе список hours_list формата [['день', 'количество часов за день'] , ...]'''
        hours_list = []
        for k in sorted(self.days_dict.keys()):
                n = 0
                for t in self.days_dict[k]:
                    if self.min_or_max == 'max':
                        if t >= self.t:
                            n += 1
                    elif self.min_or_max == 'min':
                        if t <= self.t:
                            n += 1
                # температура измерялась каждые 3 часа (по умолчанию, можно изменить в форме)
                hours_list.append([k, n*self.time_interval])
        return hours_list
        
    def hours_per_day_result(self):
        ''' представление результатов с форматированной датой'''
        return [[date.strftime('%d.%m.%Y'), n] for date, n in self.hours_per_day_list]
        
    def hours_per_day_summary_count(self):
        ''' Часовая статистика, поиск дней подряд, в которые температура не опускалась ниже заданной'''     
        hours_line = [x[1] for x in self.hours_per_day_list if x[1] != 0]
        hours = sum(hours_line)
        average_per_year = hours / len(self.years)
        if hours == 0:
            average_per_day = 0
            min_hours = 0
            max_hours = 0
        else:
            average_per_day = hours / len(hours_line)
            min_hours = min(hours_line)
            max_hours = max(hours_line)
        stat_list = [['Часовая статистика для температуры {} град С'.format(self.t)],
                     ['Cумма часов за {} лет'.format(len(self.years)), hours],
                     ['В среднем за год, часов', round(average_per_year, 1)],
                     ['В среднем в сутки, часов', round(average_per_day, 1)],
                     ['Минимум часов в сутки', min_hours],
                     ['Максимум часов в сутки', max_hours]]
                     
        all_day_temp = []
        for n in self.hours_per_day_list:
            if n[1] == 24:
                all_day_temp.append([n[0], n[1]])
        result = []
        count = 1
        for n in all_day_temp[1:]:
            if n[0] - all_day_temp[all_day_temp.index(n)-1][0] == timedelta(1):
                count += 1
            else:
                if count != 1:
                    result.append([all_day_temp[all_day_temp.index(n)-1][0] - timedelta(count-1), count])
                    count = 1
        #если промежуток будет включать последний член
        if count != 1:
            result.append([all_day_temp[-1][0] - timedelta(count-1), count])
            
        if result:
            stat_list.append(['Количество дней подряд, когда температура не {} {} град C'
                                .format('опускалась ниже' if self.min_or_max == 'max' else 'поднималась выше', self.t)])
            stat_list.append(['Дата начала промежутка', 'Количество дней'])
            for d in result:
                stat_list.append([d[0].strftime('%d.%m.%Y'), d[1]])
    
        return stat_list


