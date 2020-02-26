from bs4 import BeautifulSoup


dataHtml = []
#value = []


with open('Prog_ORIG_Topaz20a.htm', 'r') as f:
    content = f.read()
    soup = BeautifulSoup(content, 'lxml')
    for tag in soup.find_all('td'):
        dataHtml.append('{0}'.format(tag.text))

dataHtml = dataHtml[7:]
value = dataHtml[2::7]

for i, data in enumerate(value):
    value[i]=data.split('@')[0]

del dataHtml[2::7]

index = 2
k=0
while k <len(value):
    dataHtml.insert(index, value[k])
    index+=7
    k+=1

def splitT(arr, size):
    arrs = []
    while len(arr)>size:
        pice = arr[:size]
        arrs.append(pice)
        arr = arr[size:]
    arrs.append(arr)
    return arrs

del dataHtml[6::7]
dataHtml = splitT(dataHtml, 6)

print(dataHtml)
print(len(value))