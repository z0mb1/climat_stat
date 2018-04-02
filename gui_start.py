import sys
import os
import webbrowser

from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showwarning
#mymodules
from file_operations.open_and_convert_file import find_available_date
from start import make_result
from tkinter_modules.ScrolledText import ScrolledText


# Settings
base_dir = os.path.dirname(os.path.abspath(__file__))
input_file_dir = os.path.join(base_dir, 'input_files')
output_file_dir = os.path.join(base_dir, 'output_files')


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

month_number = {v:k for k, v in month_dict.items()}


class Variables():
    '''Класс для хранения переменных, получаемые из файлов, форм,
       которые в дальнейшем используются в рассчетах'''
    def __init__(self, parent=None):
        self.filename = StringVar(root)
        self.first_year = IntVar(root)
        self.last_year = IntVar(root)
        self.first_month = StringVar(root)
        self.last_month = StringVar(root)
        self.available_years = []
        self.available_months = []
        self.temp = DoubleVar(root)
        self.temp_list = StringVar(root)
        self.required_temperature = []
        self.textfield = ['результат расчета']
        self.interval = IntVar(root)
        self.interval.set(3)
        self.min_or_max = StringVar(root)

#
# Встариваемые элементы
#

# Кнопки
class MyButton(Button):
    def __init__(self, parent=None, **config):
        self.frame = parent
        Button.__init__(self, parent, **config)
        self.config(command=self.callback)
        self.pack(side=LEFT)
    def callback(self):
        pass

class OpenFileButton(MyButton):
    def __init__(self, parent=None, **config):
        MyButton.__init__(self, parent, **config)
        self.config(text='Открыть')
        self.pack(side=TOP)
        self.filedir = input_file_dir
    def callback(self):
        # добавить в вызов аргумент filetypes
        name = askopenfilename(initialdir=self.filedir)
        var = Variables(root)
        # создание настроек формы
        var.available_years, var.available_months = find_available_date(name)
        var.filename.set(name)
        var.first_year.set(min(var.available_years))
        var.last_year.set(max(var.available_years))
        var.first_month.set(month_dict[min(var.available_months)])
        var.last_month.set(month_dict[max(var.available_months)])
        #print(var.filename.get(), var.first_year.get(), var.last_year.get(), var.available_years, var.available_months)
        self.frame.destroy()
        MainFrame(variables = var, parent=root)

class AddTempButton(MyButton):
    def __init__(self, var, parent=None, **config):
        MyButton.__init__(self, parent, **config)
        self.config(text='Добавить температуру')
        self.var = var
    def callback(self):
        self.var.color_temp_list = 'green'
        current_temp = float(self.var.temp.get())
        if current_temp not in self.var.required_temperature:
            self.var.required_temperature.append(float(self.var.temp.get()))
            self.var.temp_list.set(self.var.required_temperature)
        print('{} was append'.format(self.var.temp.get()))
        print(self.var.required_temperature)

class ClrTempButton(MyButton):
    def __init__(self, var, parent=None, **config):
        MyButton.__init__(self, parent, **config)
        self.config(text='Очистить список')
        self.var = var
    def callback(self):
        self.var.required_temperature.clear()
        self.var.temp_list.set(self.var.required_temperature)
        print('cleared')
        
# Спинбоксы
class YearSpinbox(Spinbox):
    '''Done '''
    def __init__(self, years, parent=None, **config):
        Spinbox.__init__(self, parent, **config)
        self.config(width=4)
        self.config(from_=min(years), to=max(years))
        self.pack(side=LEFT)

class TempSpinbox(Spinbox):
    '''Done '''
    def __init__(self, parent=None, **config):
        Spinbox.__init__(self, parent, **config)
        self.config(width=4)
        self.config(from_=-100, to=100)
        self.pack(side=LEFT)
        
class TimeIntSpinbox(Spinbox):
    '''...'''
    def __init__(self, parent=None, **config):
        Spinbox.__init__(self, parent, **config)
        self.config(width=2)
        self.config(from_=1, to=24)
        self.pack(side=LEFT)

# Радио

class MinMaxRadioFrame(Frame):
    def __init__(self, var, parent=None, **config):
        Frame.__init__(self, parent, **config)
        self.pack(side=LEFT)
        self.var = var
        min_or_max = {'min': 'минимальной',
                  'max': 'максимальной'}
        for key in sorted(min_or_max.keys()):
            Radiobutton(self, text=min_or_max[key],
                              variable=self.var,
                              value=key).pack(side=LEFT)
        self.var.set('max')
                              
# Выпадающее меню
class MonthOptionMenu(OptionMenu):
    '''Done '''
    def __init__(self, var, months, parent=None):
        months_names = [month_dict[x] for x in months]
        OptionMenu.__init__(self, parent, var, *months_names)
        self.pack(side=LEFT)

# Текстовые поля
class TextLabel(Label):
    def __init__(self, parent=None, **config):
        Label.__init__(self, parent, **config)
        self.pack(side=LEFT)

class GroupLabel(Label):
    def __init__(self, parent=None, **config):
        Label.__init__(self, parent, **config)
        self.config(bg='black', fg='yellow')
        self.config(font=('times', 14, 'bold'))
        self.pack(side=TOP, expand=YES, fill=X)

class MyMessage(Message):
    def __init__(self, parent=None, **config):
        Message.__init__(self, parent, **config)
        self.config(background='green', aspect=5000)
        self.pack(side=LEFT)

# Группировка фрэймов
class GroupFrame(Frame):
    def __init__(self, name, parent=None, **config):
        Frame.__init__(self, parent, **config)
        self.pack(expand=YES, fill=X)
        GroupLabel(self, text=name)
        
#
# Основные классы графического интерфейса
#
class OpenFileFrame(Frame):
    '''Начальное окно для открытия файла, данные полученные из которого 
       будут использлваны для заполнения настроек формы основного окна приложения'''
    def __init__(self, parent=None, **config):
        Frame.__init__(self, parent, **config)
        self.pack(expand=YES, fill=X)
        text = '''Программа предназначена для рачета следующих параметров:\n
                1) Максимальной/минимальной дневной температуры. в формате: Дата - Значение температуры\n
                2) Интервалов дней с максимальной/минимальной температурой в формате: Дата начала промежутка - Количество дней\n
                3) Статистики по годам в формате: Год - Количество дней\n
                4) Продолжительности температуры в течение суток в формате: День - Количество часов\n
                5) Статистики по часам. За весь период, за год, в среднем в сутки, максимум, минимум\n
                Для проведения расчетов требуется открыть файл excel без заголовков с записями данных в двух колонках:\n
                в первой - дата в формате дд.мм.ГГГГ, во второй - температура\n
                Плученные результаты сохраняются в файлы .xls в папке output_files\n
                Краткая статисктика выводится в текстовое поле программы\n
                '''
        message = Message(self, text=text)
        message.config(aspect=5000)
        message.pack(side=TOP)
        Label(self, text='Для запуска сценария необходимо выбрать файл').pack(side=LEFT)
        OpenFileButton(parent=self)

class MainFrame(Frame):
    '''Основное окно приложения, создается после открытия файла и получения из него необходимых данных'''
    def __init__(self, variables, parent=None, **config):
        Frame.__init__(self, parent, **config)
        self.pack(expand=YES, fill=X)
        var = variables
        
        def make_row(elements, frame):
            '''конструктор виджетов в одну строку'''
            row = Frame(frame)
            row.pack(side=TOP, fill=X)
            for widget in elements:
                if widget[0] == 'lbl':
                    TextLabel(row, text=widget[1])
                elif widget[0] == 'yspn':
                    YearSpinbox(parent=row, textvariable=widget[1], years=var.available_years)
                elif widget[0] == 'optm':
                    MonthOptionMenu(parent=row, var=widget[1], months=var.available_months)
                elif widget[0] == 'tspn':
                    TempSpinbox(row, textvariable=widget[1])
                elif widget[0] == 'tbtn_add':
                    AddTempButton(parent=row, var=var)
                elif widget[0] == 'msg':
                    MyMessage(parent=row, textvariable=widget[1])
                elif widget[0] == 'tbtn_clr':
                    ClrTempButton(parent=row, var=var)
                elif widget[0] == 'chck':
                    MyCheckbutton(row, variable=widget[1], text=widget[2])
                elif widget[0] == 'intspn':
                    TimeIntSpinbox(row, textvariable=widget[1])
                elif widget[0] == 'rbtn':
                    MinMaxRadioFrame(parent=row, var=widget[1])
        
        # родительским элементом кнопки должно быть главное окно, чтобы создать его заново при открытии дургого файла
        OpenFileButton(parent=self)
        
        current_file_row = [['lbl', 'Текущий файл: '],
                            ['msg', var.filename]]
        time_interval_row = [['lbl', 'Интервал измерения температуры'],
                             ['intspn', var.interval]]
        for row in [current_file_row, time_interval_row]:
            make_row(elements=row, frame=self)

        # Настройки расчета
        settings_frame = GroupFrame(name='Параметры', parent=self)
        
        # первая строка настроек (выбор Годов)
        years_setting_row = [['lbl', 'Статистика погоды за период с'],
                             ['yspn', var.first_year],
                             ['lbl', 'по'],
                             ['yspn', var.last_year],
                             ['lbl', 'год']]

        # вторая строка настроек (выбор Месяцев)
        months_setting_row = [['lbl', 'Начальные месяц'],
                             ['optm', var.first_month],
                             ['lbl', 'Конечный месяц'],
                             ['optm', var.last_month]]
                             
        # третья строка выбор расчета максимальной или минимальной температуры
        min_or_max_row = [['lbl', 'Выполнить расчеты для'],
                       ['rbtn', var.min_or_max],
                       ['lbl', 'температуры']]

        # четвертая строка настроек (выбор Температуры)
        add_temp_row = [['lbl', 'Температура'],
                        ['tspn', var.temp],
                        ['lbl', 'град C'],
                        ['tbtn_add', '']] 
                   
        # пятая строка Вывод списка температуры
        show_temp_row = [['lbl', 'Расчетные значения температур:'],
                         ['msg', var.temp_list],
                         ['tbtn_clr', '']] 
        
        # Варианты расчетов
        for row in [years_setting_row, months_setting_row, min_or_max_row, add_temp_row, show_temp_row]:
            make_row(elements=row, frame=settings_frame)

        
        param_frame = GroupFrame(name='Рассчитываемые показатели', parent=self) 
        solutions_list = ['1) Максимальная/минимальная дневная температура. Дата - значение температуры',
                          '2) Интервалы дней с максимальной/минимальной температурой. Дата начала промежутка - Количество дней',
                          '3) Статистика по годам. Год - Количество дней',
                          '4) Продолжительность температуры в течение суток. День - Количество часов',
                          '5) Статистика по часам. За весь период, за год, в среднем в сутки, максимум, минимум']
        for s in solutions_list:
            make_row([['lbl', s]], param_frame)


        btn = MyButton(parent=param_frame, text='Рассчитать')
        def calculate():
            if var.required_temperature:
                # Настройки
                settings = {'filename': var.filename.get(),
                            'required_temperature': var.required_temperature,
                            'first_year': var.first_year.get(),
                            'last_year': var.last_year.get(),
                            'first_month': month_number[var.first_month.get()],
                            'last_month': month_number[var.last_month.get()],
                            'min_or_max': var.min_or_max.get(),
                            'time_interval': var.interval.get()}
                result = make_result(**settings)
                var.textfield = result
                result_field.settext(text=var.textfield)
                # открыть папку после завершения расчетов
                webbrowser.open(output_file_dir)
            else:
                showwarning('Недостаточно данных для расчета', 'Введите расчетное значение температуры')

        btn.config(command=lambda: calculate())

        
        result_field = ScrolledText(parent=self, text=var.textfield)
        
if __name__ == '__main__':
    root = Tk()
    OpenFileFrame(root)
    root.mainloop()

