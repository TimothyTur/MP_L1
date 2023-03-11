"""! @brief СКБ201 Тур ТВ Методы Программирования ЛР1"""

##
# @mainpage MPLab1
#
# @brief СКБ201 Тур ТВ Методы Программирования ЛР1
#
# @section intro Введение
# Лабораторная работа номер 1 по курсу "Методы программирования". Выполнена студентом Туром Тимофем Владимировичем группы СКБ201.
#
# @section description Описание
# В данной лабораторной работе тредуется сгенерировать выборки по заданным параметрам, применить несколько сортировок к ней и привести графики по времени их работы.
# Мой вариант - 24. Требуется реализовать класс с информацией о постояльцах некоторой гостинницы: ФИО, занимаемый номер, дата приезда, дата отъезда, сумма оплаты проживания; с функицями сравнения по полям дата приезда, занимаемый номер и ФИО. Требуемые сортировки: сортировка простыми вставками, шейкер-сортировка и быстрая сортировка.
#
# @section link Ссылка на репозиторий
# В репозитории github хранятся данный проект: https://github.com/TimothyTur/MP_L1
# В силу явной ненужности многих данных doxygen, они будут отсутствовать там (кроме явно нужных, например как этот отчет).
#
# @section diagram График времени работы сортировок
# Чтобы не добавлять требуемый график просто приклеив его снизу, добавлю его тут. На графике отображено время выполнения сортировки в зависимости от числа элементов для сортировок простыми вставками, шейкер и быстрой.
# @image latex mpLab1Graph1.png "График работы сортировок"
# Быстрая сортировка в каждой точке измерения справляется меньше чем за секунду. Мне показалось это странным, но множественные проверки показали что это действительно так и что она реально быстрая. Линяя, соответствующая быстрой сортировке выглядит прямой, но только из-за соотношения по высотам с другими линиями. Хоть и совершенно небольшое, но время у нее тоже есть.
#

##
# @file full_code.py
#

# Imports
import random as rnd
import time
import numpy as np
import matplotlib.pyplot as plt

# Основа классовых генераторов
def str_time_prop(start, end, time_format, prop):
    """! Берет точку prop в отрезке [start, end] времени, заданным строкой формата time_format.
    
    @param start       Начало отрезка.
    @param end         Конец отрезка.
    @param time_format Формат строки.
    @param prop        Процентная точка интервала.
    
    @return            Дату между start и end по сдвигу prop.
    """
    
    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))
    
    ptime = stime+prop*(etime-stime)
    
    return time.strftime(time_format, time.localtime(ptime))

def random_date(start, end, prop):
    """! Выбирает случайную точку времени в отрезке [start, end] формата "%Y/%m/%d" по генератору prop.
    
    @param start       Начало отрезка.
    @param end         Конец отрезка.
    @param prop        Генератор случайных числел на отрезке [0, 1].
    
    @return            Случайная дата между start и end.
    """
    return str_time_prop(start, end, "%Y/%m/%d", prop)
# Данные для построения ФИО
## Выборка фамилий
surnames =  ["Абдуллабеков", "Богов", "Григорьян", "Грицун", "Гришаев",
             "Друх", "Зильберштейн", "Кашинцев", "Коников", "Красов",
             "Кузьмина", "Курмашева", "Магамедов", "Недомолкин",
             "Никитченко", "Онищенко", "Осипова", "Парфенюк", "Самунин",
             "Сарибекян", "Сергеев", "Смирнов", "Ташлыков", "Тур",
             "Ушаков", "Фролов", "Черников", "Яськов"]
## Выборка имен
names =     ["Тимур", "Мурат", "Андрей", "Тимофей", "Ростислав", "Радомир",
             "Павел", "Илья", "Максим", "Артём", "Ксения", "Татьяна",
             "Артур", "Илья", "Александр", "Елизавета", "Анастасия",
             "Михаил", "Роман", "Гор", "Никита", "Данила", "Григорий",
             "Тимофей", "Александр", "Олег", "Евгений", "Александр"]
## Выборка отчеств
lastnames = ["Мугутдинович", "Русланович", "Ашотович", "Юрьевич",
             "Алексеевич", "Вадимович", "Евгеньевич", "Константинович",
             "Павлович", "Сергеевич", "Дмитриевна", "Александровна",
             "Мирзоевич", "Эдуардович", "Сергеевич", "Григорьевна",
             "Николаевна", "Денисович", "Олегович", "Эдикович", "Игоревич",
             "Андреевич", "Александрович", "Владимирович", "Николаевич",
             "Витальевич", "Сергеевич", "Семенович"]

class MyObject:
    """! Класс объектов, требуемых по заданию лабораторной работы.
    """
    def __init__(self, *args):
        """! Конструктор класса
        Позволяет несколько реализаций.
        Использования конструктора без аргументов сгенерирует парамента случайно.
        Использование 5 аргументов позволит однозначно задать данные объекта.
        
        @param fio ФИО.
        @param num Занимаемый номер.
        @param din Дата приезда.
        @param dou Дата отъезда.
        @param pay Сумма оплаты проживания.
        """
        if(len(args)==0) :
            self.fio = rnd.choice(surnames)+' '+rnd.choice(names)+' '+\
                       rnd.choice(lastnames)
            self.num = rnd.randint(1, 100)
            self.din = random_date('2004/1/1', '2014/12/31', rnd.random())
            self.dou = random_date('2004/1/1', '2014/12/31', rnd.random())
            if(self.dou<self.din) :
                self.dou, self.din = self.din, self.dou
            self.pay = rnd.randint(1000, 100000)
        elif(len(args)==5):
            self.fio, self.num, self.din, self.dou, self.pay = \
                args[0], args[1], args[2], args[3], args[4]
        else:
            raise AttributeError
            
    def __eq__(self, other):
        """! Проверка на равенство.
        
        @param other Объект сравнения класса MyObject.
        
        @return bool.
        """
        return self.din==other.din and self.num==other.num and \
            self.fio==other.fio
    #>=
    def __ge__(self, other):
        """! Проверка на больше или равно.
        
        @param other Объект сравнения класса MyObject.
        
        @return bool.
        """
        if(self.din==other.din):
            if(self.num==other.num):
                return self.fio>=other.fio
            else:
                return self.num>other.num
        else:
            return self.din>other.din
    #>
    def __gt__(self, other):
        """! Проверка на больше.
        
        @param other Объект сравнения класса MyObject.
        
        @return bool.
        """
        if(self.din==other.din):
            if(self.num==other.num):
                return self.fio>other.fio
            else:
                return self.num>other.num
        else:
            return self.din>other.din
    #<=
    def __le__(self, other):
        """! Проверка на меньше или равно.
        
        @param other Объект сравнения класса MyObject.
        
        @return bool.
        """
        if(self.din==other.din):
            if(self.num==other.num):
                return self.fio<=other.fio
            else:
                return self.num<other.num
        else:
            return self.din<other.din
    #<
    def __lt__(self, other):
        """! Проверка на меньше.
        
        @param other Объект сравнения класса MyObject.
        
        @return bool.
        """
        if(self.din==other.din):
            if(self.num==other.num):
                return self.fio<other.fio
            else:
                return self.num<other.num
        else:
            return self.din<other.din
    #!=
    def __ne__(self, other):
        """! Проверка на не равно.
        
        @param other Объект сравнения класса MyObject.
        
        @return bool.
        """
        return not(self.__eq__(other))
    
    def __str__(self):
        """! Выводит содержимое класса в строке через пробел.
        
        @return fio, num, din, dou, pay.
        """
        return ' '.join([self.fio, str(self.num),
                         self.din, self.dou, str(self.pay)])
    
    def writeOpenedFile(self, file):
        """! Функция записи образа объекта в открытый файл.
        
        @param file открытый файл, куда будет записан образ.
        """
        file.write(str(self)+'\n')
    
    def readOpenedFile(self, file):
        """! Функция чтения образа объекта с открытого файла.
        
        @param file открытый файл, откуда будет прочтен образ.
        """
        data = file.readline()[:-1].split(' ');
        self.fio = ' '.join(data[0:3])
        self.num = int(data[3])
        self.din = data[4]
        self.dou = data[5]
        self.pay = int(data[6])
        return self
        
# Рассматриваемые длины выборок
ns = [100, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000]

# Генерация выборок и сохранение их в файл
for length in ns:
    with open('mpLab1Sample'+str(length)+'.txt', 'w') as file:
        for i in range(length):
            MyObject().writeOpenedFile(file)
            
# Чтение выборок из файлов
samples = []
for i in range(len(ns)):
    samples.append([])
    with open('mpLab1Sample'+str(ns[i])+'.txt', 'r') as file:
        for j in range(ns[i]):
            samples[i].append(MyObject().readOpenedFile(file))
            
# Массив, в котором будет отслеживаться время выполнения
t = [[],[],[]]
# вставки[ns], шейкер[ns], быстрая[ns]
def checkSorted(mass):
    """! Функция, проверяющая отсортированность массива.
    
    @param mass Массив для проверки.
    
    @return "sorted" или "not sorted" соответственно
    """
    flag = 0
    for i in range(len(mass)-1):
        if mass[i]>mass[i+1]:
            return "not sorted"
    return 'sorted'

def myInsertSort(mass):
    """! Сортировка простыми вставками
    
    @param mass Массив к сортировке
    """
    elem = None
    for i in range(1, len(mass)):
        elem = mass[i]
        j = i-1
        while(j>=0 and mass[j]>elem):
            mass[j+1] = mass[j]
            j-=1
        mass[j+1]=elem
        
## Тесты вставок
# Мои результаты (в секундах):
# 0.00099945068359375 sorted
# 0.00999760627746582 sorted
# 0.06201767921447754 sorted
# 0.1869981288909912 sorted
# 1.3099727630615234 sorted
# 5.157149791717529 sorted
# 22.87809109687805 sorted
# 197.90494179725647 sorted
# 857.611848115921 sorted
t[0] = [0]*len(ns)
for i in range(len(ns)):
    start = time.time()
    myInsertSort(samples[i])
    t[0][i] = time.time() - start
    print(t[0][i], checkSorted(samples[i]))
    with open('mpLab1Insert'+str(ns[i])+'.txt', 'w') as file:
        for j in range(ns[i]):
            samples[i][j].writeOpenedFile(file)

            
# Обнуление предыдущих результатов (пересччитывание)
samples = []
for i in range(len(ns)):
    samples.append([])
    with open('mpLab1Sample'+str(ns[i])+'.txt', 'r') as file:
        for j in range(ns[i]):
            samples[i].append(MyObject().readOpenedFile(file))
            
def myShakerSort(mass):
    """! Шейкер-сортировка
    
    @param mass Массив к сортировке
    """
    lb = 0
    ub = len(mass)-1
    while(lb<ub):
        for i in range(lb, ub, 1):
            if(mass[i]>mass[i+1]):
                mass[i], mass[i+1] = mass[i+1], mass[i]
        ub = ub-1
        for i in range(ub-1, lb-1, -1):
            if(mass[i]>mass[i+1]):
                mass[i], mass[i+1] = mass[i+1], mass[i]
        lb = lb+1

## Тесты шейкера
# Мои результаты (в секундах):
# 0.0009984970092773438 sorted
# 0.023984193801879883 sorted
# 0.0969991683959961 sorted
# 0.4080338478088379 sorted
# 2.623000144958496 sorted
# 10.752975702285767 sorted
# 48.14202809333801 sorted
# 381.2530007362366 sorted
# 1642.778974533081 sorted
t[1] = [0]*len(ns)
for i in range(len(ns)):
    start = time.time()
    myShakerSort(samples[i])
    t[1][i] = time.time() - start
    print(t[1][i], checkSorted(samples[i]))
    with open('mpLab1Shaker'+str(ns[i])+'.txt', 'w') as file:
        for j in range(ns[i]):
            samples[i][j].writeOpenedFile(file)


# Обнуление предыдущих результатов (пересччитывание)
samples = []
for i in range(len(ns)):
    samples.append([])
    with open('mpLab1Sample'+str(ns[i])+'.txt', 'r') as file:
        for j in range(ns[i]):
            samples[i].append(MyObject().readOpenedFile(file))


def myQuickSort(mass, lb=0, ub=None):
    """! Быстрая сортировка
    
    @param mass Массив к сортировке
    @param lb   Нижняя граница сортировки (по умолчанию 0)
    @param ub   Верхняя граница сортировки (по умолчанию len(mass)-1)
    """
    if(ub==None):
        ub = len(mass)-1
    def _myQuickSort(mass, lb, ub):
        if(lb>=ub): return
        devider = lb
        for i in range(lb+1, ub+1):
            if(mass[i]<=mass[lb]):
                devider+=1
                mass[i], mass[devider] = mass[devider], mass[i]
        mass[devider], mass[lb] = mass[lb], mass[devider]
        _myQuickSort(mass, lb, devider-1)
        _myQuickSort(mass, devider+1, ub)
    return _myQuickSort(mass, lb, ub)

## Тесты быстрой
# Мои результаты (в секундах):
# 0.0 sorted
# 0.0010008811950683594 sorted
# 0.00402379035949707 sorted
# 0.007001161575317383 sorted
# 0.015002250671386719 sorted
# 0.03199958801269531 sorted
# 0.08599495887756348 sorted
# 0.24699020385742188 sorted
# 0.5119972229003906 sorted
t[2] = [0]*len(ns)
for i in range(len(ns)):
    start = time.time()
    myQuickSort(samples[i])
    t[2][i] = time.time() - start
    print(t[2][i], checkSorted(samples[i]))
    with open('mpLab1Quick'+str(ns[i])+'.txt', 'w') as file:
        for j in range(ns[i]):
            samples[i][j].writeOpenedFile(file)

# Построение графиков
plt.plot(ns, t[0], marker='.')
plt.plot(ns, t[1], marker='.')
plt.plot(ns, t[2], marker='.')
plt.xticks(np.arange(0, 100001, 10000), rotation=30)
plt.yticks(rotation=70)
plt.xlabel("Число элементов, ед.")
plt.ylabel("Время вычисления, сек.")
plt.title("Графики времени сортировок")
plt.legend(["Сортировка простыми вставками",
            "Шейкер-сортировка", "Быстрая сортировка"],
           loc = "upper left")
plt.grid(True, alpha = 0.5, ls = "dotted")

plt.savefig('mpLab1Graph1.png', bbox_inches='tight')`