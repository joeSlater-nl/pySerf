import csv
from tkinter import *
from tkinter import filedialog as fd
from bs4 import BeautifulSoup

data_html = []

def open_html():
    global data_html
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



open_html()
print(data_html)


