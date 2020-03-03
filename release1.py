#!/usr/local/bin/python3
import csv
from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from bs4 import BeautifulSoup
import xlrd

data_html = []
reference = []
reference_excel = []
res = []
mirrorNew = []
bot = []
top = []
bot32=[]
top32 = []
def open_html():
    global data_html ,reference, mirror
    filename = fd.askopenfilename(filetypes = [('HTM files', '*.htm'), ('ALL files', '*.*')])
    entyProg.delete(0, END)
    entyProg.insert(0, filename)
    with open(filename, 'r') as dataHtml:
        content = dataHtml.read()
        soup = BeautifulSoup(content, 'lxml')
        for tag in soup.find_all('td'):
            data_html.append('{0}'.format(tag.text))

    # отбрасываем хэд
    data_html = data_html[7::]

    # получем значение mirror для составления файлов top, bot
    mirror = data_html[6::7]

    # reference для сравнения с бомом, для составления итоговой программы
    reference = data_html[0::7]

    # получем и обрабатываем значение value, приводим к виду без @
    value = data_html[2::7]
    for i, data in enumerate(value):
        value[i]=data.split('@')[0].rstrip()
    # заменяем value формата 'value @package' на 'value'
    del data_html[2::7]
    index = 2
    i = 0
    while i < len(value):
        data_html.insert(index, value[i])
        index += 7
        i += 1
    # удаляем mirror и делим список на листы по 6 значений
    del data_html[6::7]
    def split_for_csv(arr, size):
        arrs = []
        while len(arr) > size:
            pice = arr[:size]
            arrs.append(pice)
            arr = arr[size:]
        arrs.append(arr)
        return arrs
    data_html = split_for_csv(data_html, 6)

def openEXCEL():
    global reference_excel
    filenameXL = fd.askopenfilename(filetypes = [('EXCEL file', '*.xls'),('ALL files', '*.*')] )
    entryExcel.delete(0, END)
    entryExcel.insert(0, filenameXL)

    df = xlrd.open_workbook(filenameXL)
    sheet = df.sheet_by_index(0)
    row_num = sheet.nrows

    for row in range(0, row_num):
        reference_excel.append(str(sheet.row(row)[4]).replace('text:', '').replace("'Part Reference'",'').replace("'", ' '))
    reference_excel =''.join(reference_excel)
    reference_excel = reference_excel.split()

def comparison():
    global res, data_html, reference, reference_excel, bot
    j = 0
    k = 0
    rb = 0
    rt = 0
    b32 = 0
    t32 = 0
    while j < len(reference):
        if reference[j] in reference_excel:
            res.append(data_html[j])
            mirrorNew.append(mirror[j])
        j+=1
    while k <len(res):
        if 'YES' in mirrorNew[k]:
            bot.append(res[k])
        else:
            top.append(res[k])
        k+=1

    #переварачиваем углы на боте
    while rb < len(bot):
        if bot[rb][5] == '180.000':
            bot[rb][5] = '0'
        elif bot[rb][5] == '0.000':
            bot[rb][5] = '180'
        elif bot[rb][5] == '270.000':
            bot[rb][5] = '90'
        elif bot[rb][5] == '90.000':
            bot[rb][5] = '270'
        rb+=1
    #приводим топ к виду без *.000
    while rt < len(top):
        if top[rt][5] == '180.000':
            top[rt][5] = '180'
        elif top[rt][5] == '0.000':
            top[rt][5] = '0'
        elif top[rt][5] == '90.000':
            top[rt][5] = '90'
        elif top[rt][5] == '270.000':
            top[rt][5] = '270'
        rt+=1

    #проверка на 32 символа

    while b32 < len(bot):
        if len(bot[b32][1]+bot[b32][2]) > 32:
            mb.showwarning('Внимание', bot[b32])
        b32+=1

        

def savePath(data, path):
    with open(path, 'w', newline='') as csv_res:
        writer = csv.writer(csv_res, delimiter = ';')
        for line in data:
            writer.writerows(line)
            
def resTop():
    data = [top]
    path = fd.asksaveasfilename(filetypes = [('CSV files', '*.csv'), ('ALL files', '*.* ')], defaultextension ='.csv')
    savePath(data, path)

def resBot():
    data = [bot]
    path = fd.asksaveasfilename(filetypes = [('CSV files', '*.csv'), ('ALL files', '*.* ')], defaultextension ='.csv')
    resBot(data, path)



root = Tk()

buttonProg = Button(text = 'Открыть файл программы', command = open_html).grid(row = 0, column = 0)
entyProg = Entry()
entyProg.grid(row = 0 , column = 1, columnspan = 15)
buttonExcel = Button(text = 'Отрыть файл Эксель', command = openEXCEL).grid(row = 1, column = 0)
entryExcel = Entry()
entryExcel.grid(row = 1, column = 2, columnspan = 15)
buttonComparison = Button (text = 'получение программ' , command = comparison).grid(row = 2, column = 8)
buttonSaveTop = Button (text ='сохранить TOP' , command = saveTop).grid(row = 2, column = 9)
buttonSaveBot = Button (text = 'сохранить BOT', command = saveBot).grid(row = 2, column = 10)

root = mainloop()
