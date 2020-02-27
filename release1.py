import csv
from tkinter import *
from tkinter import filedialog as fd
from bs4 import BeautifulSoup
import xlrd

data_html = []
reference = []
reference_excel = []
res = []
mirrorNew = []
bot = []
top = []
def open_html():
    global data_html ,reference, mirror
    filename = fd.askopenfilename(filetypes = [('HTM files', '*.htm'), ('ALL files', '*.*')])

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

    filenameXL = fd.askopenfilename()

    df = xlrd.open_workbook(filenameXL)
    sheet = df.sheet_by_index(0)
    row_num = sheet.nrows

    for row in range(0, row_num):
        reference_excel.append(str(sheet.row(row)[4]).replace('text:', '').replace("'Part Reference'",'').replace("'", ' '))
    reference_excel =''.join(reference_excel)
    reference_excel = reference_excel.split()





# НУЖНО ИСОЛЬЗОВАТЬ БИНАРНЫЙ ПОИСК


def comparison():
    global res, data_html, reference, reference_excel
    j = 0
    k = 0

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


def saveCsv():


root = Tk()

buttonProg = Button(text = 'Открыть файл программы', command = open_html).grid(row = 0, column = 0)
entyProg = Entry().grid(row = 0 , column = 1, columnspan = 10)
buttonExcel = Button(text = 'Отрыть файл Эксель', command = openEXCEL).grid(row = 1, column = 0)
entryExcel = Entry().grid(row = 1, column = 2, columnspan = 10)
buttonComparison = Button (text = 'получение программ' , command = comparison).grid(row = 2, column = 8)



root = mainloop()

print(len(res))
print(len(bot))
print(len(top))