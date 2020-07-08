
from bs4 import BeautifulSoup
import re

data_html = []
global_list_top = []
global_list_bot = []

EXCLUDE_REFDES = ['REFDES', 'BRG']
INCLUDE_REFDES = []

# regular = re.compile(r'[.0\*]+$')
regular_zero = re.compile(r'\.{0,1}0*$')
regular_alpha = re.compile(r'^[a-zA-Z]+')

angles = {'180': '0', '0': '180', '270': '90', '90': '270'}


def check_refdes(data):
    # paste here your some code
    #print('check '+data)
    #res1 = data in EXCLUDE_REFDES
    res2 = re.match(regular_alpha, data).group(0) in INCLUDE_REFDES
    #return not res1 and res2
    return not res2

def cut_zeros(data):
    res = re.sub(regular_zero, '', data)
    # paste here your some code
    return res


def open_html():
    global data_html, reference, mirror
    filename = 'Prog_ORIG_Topaz20a.htm'

    with open(filename, 'r') as dataHtml:
        content = dataHtml.read()
        soup = BeautifulSoup(content, 'lxml')

    number = 0

    for i in soup.findAll('tr'):
        temp_list = []
        for j in enumerate(i.findAll('td')):
            tl = j[1].text
            index = j[0]
            #print(tl)
            if index == 0:
                if check_refdes(tl) == False:
                    break

            elif index == 2:
                tl = tl.split('@')[0].rstrip()

            elif index == 6:
                if tl in 'YES':
                    global_list_top.append(temp_list)
                else:
                    #print(temp_list[5])
                    temp_list[5] = angles[temp_list[5]]
                    global_list_bot.append(temp_list)
                break

            elif index >= 3 and index < 6:
                tl = cut_zeros(tl)

            temp_list.append(tl)

    print('TOP')
    print(global_list_top)
    print('BOT')
    print(global_list_bot)


if __name__ == '__main__':
    open_html()
