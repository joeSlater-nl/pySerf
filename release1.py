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
bot32 = []
top32 = []

def open_html():
    global data_html, reference, mirror
    filename = fd.askopenfilename(filetypes=[('HTM files', '*.htm'), ('ALL files', '*.*')])
    #entyProg.delete(0, END)
    #entyProg.insert(0, filename)
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
        value[i] = data.split('@')[0].rstrip()
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
    filenameXL = fd.askopenfilename(filetypes=[('EXCEL file', '*.xls'), ('ALL files', '*.*')])
    #entryExcel.delete(0, END)
    #entryExcel.insert(0, filenameXL)

    df = xlrd.open_workbook(filenameXL)
    sheet = df.sheet_by_index(0)
    row_num = sheet.nrows

    for row in range(0, row_num):
        reference_excel.append(
            str(sheet.row(row)[4]).replace('text:', '').replace("'Part Reference'", '').replace("'", ' '))
    reference_excel = ''.join(reference_excel)
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
        j += 1
    while k < len(res):
        if 'YES' in mirrorNew[k]:
            bot.append(res[k])
        else:
            top.append(res[k])
        k += 1

    # переварачиваем углы на боте
    while rb < len(bot):
        if bot[rb][5] == '180.000':
            bot[rb][5] = '0'
        elif bot[rb][5] == '0.000':
            bot[rb][5] = '180'
        elif bot[rb][5] == '270.000':
            bot[rb][5] = '90'
        elif bot[rb][5] == '90.000':
            bot[rb][5] = '270'
        rb += 1
    # приводим топ к виду без *.000
    while rt < len(top):
        if top[rt][5] == '180.000':
            top[rt][5] = '180'
        elif top[rt][5] == '0.000':
            top[rt][5] = '0'
        elif top[rt][5] == '90.000':
            top[rt][5] = '90'
        elif top[rt][5] == '270.000':
            top[rt][5] = '270'
        rt += 1

    # проверка на 32 символа
    while b32 < len(bot):
        if len(bot[b32][1] + bot[b32][2]) > 32:
            bot32.append(bot[b32])
        b32 += 1

    if len(bot32) > 0:

        save_responce = mb.askyesno('проверка на 32 символа', 'изменить??')
        if save_responce is True:
            GUI()
        if save_responce is False:
            pass

def savePath(data, path):
    with open(path, 'w', newline='') as csv_res:
        writer = csv.writer(csv_res, delimiter=';')
        for line in data:
            writer.writerows(line)

def saveTop():
    data = [top]
    path = fd.asksaveasfilename(filetypes=[('CSV files', '*.csv'), ('ALL files', '*.* ')], defaultextension='.csv')
    savePath(data, path)

def saveBot():
    data = [bot]
    path = fd.asksaveasfilename(filetypes=[('CSV files', '*.csv'), ('ALL files', '*.* ')], defaultextension='.csv')
    savePath(data, path)

def saveChange():
    pass

class GUI():
    def __init__(self):
        self.root = Tk()
        self.sv = StringVar(self.root)
        self.lbox = Listbox(self.root)
        self.entry = Entry(self.root, textvariable = self.sv)
        self.entry.grid(row=0, column=0)
        self.lbox.grid(row=1, column=0)
        self.entryQ = Entry(self.root, width=5)
        self.entryQ.grid(row=0, column=1)
        self.btn_exit = Button(self.root, text='Выйти', command=self.root.destroy).grid(row=0, column=2)
        self.btn_save_change = Button(self.root, text='сохранить изменения').grid(row=1, column=2)
        for i in bot32:
            self.lbox.insert(0, i)
        self.root.bind('<Double-Button-1>', self.getE)
        self.entry.bind('<KeyRelease>', self.OnClick)
        self.root.mainloop()

    def OnClick(self, event = 0):

        self.value  = self.sv.get().split()
        self.entryQ.delete(0, END)
        self.entryQ.insert(0, len(self.value[1]+self.value[2]))
    def getE(self, event):
        self.e1 = self.lbox.curselection()[0]
        self.st = self.lbox.get(self.e1)

        self.entry.delete(0, END)
        self.entry.insert(0, self.st)

class Main_Menu():
    def __init__(self):
        self.window = Tk()
        self.label = Label(self.window, text='Файл HTML: ').grid(row=0, column=0)
        self.entry_html = Entry(self.window)
        self.entry_html.grid(row=0, column=1)
        self.btn_html = Button(text='Обзор', command=open_html).grid(row=0, column=2)
        self.label_bom = Label(self.window, text='BOM: ').grid(row=1, column=0)
        self.entry_bom = Entry(self.window)
        self.entry_bom.grid(row=1, column=1)
        self.btn_bom = Button(self.window, text='Обзор', command=openEXCEL).grid(row=1, column=2)
        self.btn_save_top = Button(text='Сохранить TOP', command=saveTop).grid(row=2, column=10)
        self.btn_save_bot = Button(text='сохранить BOT', command=saveBot).grid(row=2, column=11, pady=10, padx=10)
        self.btn_comparison = Button(text='получение программ', command=comparison).grid(row=2, column=9)

        self.window.mainloop()


Main_Menu()