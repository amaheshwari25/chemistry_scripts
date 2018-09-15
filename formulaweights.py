from bs4 import BeautifulSoup as bs
import requests

#requisites: install bs4, requests packages
# a script that finds the formula weight in amu ( or equivalently molar mass in g/mol)

ptable = requests.get('https://ptable.com/')

soup = bs(ptable.text, 'html.parser')

print("format: separate each element with a space, "
      "put count of each element before that element (no space), "
      "type DONE (no spaces!) to exit")

elements = input("input compound?")

while not elements == 'DONE':
    elemlist = elements.split()

    weightSum = 0
    for elem in elemlist:
        numString = "1"
        while ord(elem[0]) < 65:
            numString += elem[0]
            elem = elem[1:]
        elembox = soup.find('acronym', text=elem)
        weight=elembox.findNext('i').text
        print("atomic weight: "+elembox.text+":"+weight)
        weightSum += float(weight)*int(numString)
    print(weightSum)
    elements = input("input compound?")



