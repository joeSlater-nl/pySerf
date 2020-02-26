import csv
from tkinter import *
from tkinter import filedialog as fd
from typing import List, Any

from bs4 import BeautifulSoup
import  xlrd

data_list_html = [] #все данные из htm table

#списки из html table для создания csv
ref_from_html = []
package = []
val = []
sym_center_X = []
sym_center_Y = []
sym_rotate = []
sym_mirror = []

#отфильрованные списки для bot и top
bot_ref = []; bot_rotate = []; bot_value = []; bot_package = []; bot_center_X = []; bot_center_Y = []
top_ref = []; top_rotate = []; top_value = []; top_package = []; top_center_X = []; top_center_Y = []


ref_BOM = []
ref_BOM_join= []

value = []

top_release = []



def openBom():
    global ref_BOM, ref_BOM_join

    filename = fd.askopenfilename()
    df = xlrd.open_workbook(filename)
    sheet = df.sheet_by_index(0)
    row_num = sheet.nrows

    for row in range(0, row_num):
        ref_BOM.append(str(sheet.row(row)[4]).replace('text:', '').replace("'", ''))
        ref_BOM_join =''.join(ref_BOM)

def comparing():
    i = 0
    while i<len(top_ref):
        if top_ref[i] in ref_BOM_join:
            top_release.append(top_ref[i]+';'+top_package[i]+';'+top_value[i]+';'+top_center_X[i]+';'+top_center_Y[i]+';'+top_rotate[i])
    i+=1






root = Tk()

b1 = Button(text = 'Open PROGROGORGOROG', command = openProg).grid(row = 0, column = 0)
e1 = Entry()
e1.grid(row = 0, column = 1, columnspan = 5)
e2 = Entry()
e2.grid(row = 1 , column = 1, columnspan = 5)
b2 = Button(text = 'Open BOMBOBMBOM', command = openBom).grid(row = 1, column = 0)
b3 = Button (text = 'EXTRAXT', command = comparing).grid(row = 2, column = 0)






root.mainloop()


print(top_release)