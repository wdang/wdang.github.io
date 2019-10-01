from bs4 import BeautifulSoup
import os
import sys
from collections import namedtuple

NAMES = ["Akuma",
"Alisa Bosconovitch",
"Anna Williams",
"Armor King",
"Asuka Kazama",
"Bob Richards",
"Bryan Fury",
"Claudio Serafino",
"Craig Marduk",
"Devil Jin",
"Eddy Gordo",
"Eliza",
"Feng Wei",
"Geese Howard",
"Gigas",
"Heihachi Mishima",
"Hwoarang",
"Jack-7",
"Jin Kazama",
"Josie Rizal",
"Julia Chang",
"Katarina Alves",
"Kazumi Mishima",
"Kazuya Mishima",
"King",
"Kuma",
"Lars Alexandersson",
"Lee Chaolan",
"Lei Wulong",
"Leo Kliesen",
"Leroy Smith",
"Lili De Rochefort",
"Ling Xiaoyu",
"Lucky Chloe",
"Marshall Law",
"Master Raven",
"Miguel Caballero Rojo",
"Negan",
"Nina Williams",
"Noctis Lucis Caelum",
"Panda",
"Paul Phoenix",
"Sergei Dragunov",
"Shaheen",
"Steve Fox",
"Yoshimitsu",
"Zafina"
]
SHORT_NAMES = [
"Akuma",
"Alisa",
"Anna",
"Armor King",
"Asuka",
"Bob",
"Bryan",
"Claudio",
"Marduk",
"Devil Jin",
"Eddy",
"Eliza",
"Feng",
"Geese",
"Gigas",
"Heihachi",
"Hwoarang",
"Jack",
"Jin",
"Josie",
"Julia",
"Katarina",
"Kazumi",
"Kazuya",
"King",
"Kuma",
"Lars",
"Lee",
"Lei",
"Leo",
"Leroy",
"Lili",
"Ling",
"Lucky",
"Xiaoyu",
"Marshall",
"Law",
"Raven",
"Miguel",
"Negan",
"Nina",
"Noctis",
"Panda",
"Paul",
"Sergei",
"Shaheen",
"Steve",
"Yoshimitsu",
"Xiaoyu",
"Zafina"
]


'''
HEADERS = [
Command
Hit level
Damage
Start up frame
Block frame
Hit frame
Counter hit frame
]'''

fields = ("Input", "Level", "Damage", "Start", "Block", "Hit", "Counter", "Notes")

Move = namedtuple('Move', fields, defaults=None)

def printJSON(movelist):
    start = '{\n  \"data\": ['
    end = '  ]\n}'
    s = ("\"{}\":\"{{}}\",\n" * len(Move._fields))
    s = s.format(*Move._fields)
    s = s[: len(s) - 2]
    print('{\n  \"data\": [')
    print('{{{}}}'.format(s.format(*movelist[8])))
    print('  ]\n}')
    


def getHTMLFiles():
    htmlfilespath = os.getcwd() + '\\frames\\html'
    return (htmlfilespath + '\\' + name for root, dirs, files in os.walk(htmlfilespath) for name in files)
    

def parseHTMLFramesFile(filepath):
    with open(filepath) as f:
        soup = BeautifulSoup(f,'html.parser')
        rows = soup.find_all('tr')
        for r in soup.find_all('tr'):
            yield Move(*[''.join(n.strings) for n in r.find_all('td')])



if __name__ == '__main__':
    print(sys.version)
    getHTMLFiles()
    filespaths = list(getHTMLFiles())
    moves = list(parseHTMLFramesFile(filespaths[0]))
    printJSON(moves)



            
            
        
            

