from bs4 import BeautifulSoup as bs
import requests

#requisites: install bs4, requests packages
# a script that finds the formula weight in amu ( or equivalently molar mass in g/mol)

ptable = requests.get('https://ptable.com/')

soup = bs(ptable.text, 'html.parser')

print("format: separate each element with a space, "
      "put count of each element after that element (no space), "
      "type DONE (no spaces!) to exit")

elements = input("input compound?")

while not elements == 'DONE':
    elemlist = elements.split()

    weightSum = 0
    for elem in elemlist:
        elemSymb = ""
        while len(elem) > 0 and ord(elem[0]) >= 65:
            elemSymb += elem[0]
            elem = elem[1:]
        if elem == "":
            numString = "1"
        else:
            numString = elem
        elembox = soup.find('acronym', text=elemSymb)
        weight=elembox.findNext('i').text
        print("atomic weight: "+elembox.text+":"+weight)
        weightSum += float(weight)*int(numString)
    print(weightSum)
    elements = input("input compound?")



