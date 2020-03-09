from tkinter import *
from tkinter import filedialog as fd
from bs4 import BeautifulSoup

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
        for i in data:
            self.lbox.insert(0, i)
        self.root.bind('<Double-Button-1>', self.getE)
        self.entry.bind('<KeyRelease>', self.OnClick)
        self.root.mainloop()

    def OnClick(self, event = 0):

        self.value  = self.sv.get().rstrip()
        self.entryQ.delete(0, END)
        self.entryQ.insert(0, len(self.value))

    def getE(self, event):
        self.e1 = self.lbox.curselection()[0]
        self.st = self.lbox.get(self.e1)

        self.entry.delete(0, END)
        self.entry.insert(0, self.st)

class Main_Menu():
    def __init__(self):
        self.window = Tk()
        self.label = Label(self.window, text='Файл HTML: ')
        self.label.grid(row=0, column=0)
        self.entry_html = Entry(self.window)
        self.entry_html.grid(row=0, column=1)
        self.btn_html = Button(text='Обзор')
        self.btn_html.grid(row=0, column=2)
        self.label_bom = Label(self.window, text='BOM: ')
        self.label_bom.grid(row=1, column=0)
        self.entry_bom = Entry(self.window)
        self.entry_bom.grid(row=1, column=1)
        self.btn_bom = Button(self.window, text='Обзор', command = GUI)
        self.btn_bom.grid(row=1, column=2)

        self.window.mainloop()

def open_html():
    filename = fd.askopenfilename()
    with open(filename, 'r') as html:
        data =

Main_Menu()


