import os
import sys
import json
import re
from collections import namedtuple
from bs4 import BeautifulSoup

NAMES = [
    "Akuma",
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
Incoming data HEADERS = [
Command
Hit level
Damage
Start up frame
Block frame
Hit frame
Counter hit frame
Notes
]'''

fields = ("Input", "Level", "Damage", "Startup",
          "Block", "Hit", "Counter", "Notes")

Move = namedtuple('Move', fields, defaults="")


def printJSON(movelist):
    s = ("\"{}\":\"{{}}\",\n" * len(Move._fields))
    s = s.format(*Move._fields)
    s = s[: len(s) - 2]
    print('{\n  \"data\": [')
    for m in movelist:
        print('{{\n{}\n}},'.format(s.format(*m)))
    print('  ]\n}')


def replaceNonAscii(s, replacement=''):
    return ''.join([c if ord(c) < 128 else replacement for c in s])

def getHTMLFiles():
    htmlfilespath = os.getcwd() + '\\frames\\html'
    return (htmlfilespath + '\\' + name for root, dirs, files in os.walk(htmlfilespath) for name in files)

def parseHTMLFramesFile(filepath):
    with open(filepath, encoding="utf8") as f:
        soup = BeautifulSoup(f, 'html.parser')
        rows = soup.find_all('tr')
        for r in rows:
            rowdata = [replaceNonAscii(''.join(td.strings)) for td in r.find_all('td')]            
            if len(rowdata) != 8:
                continue
            elif re.match('[Cc]ommand', rowdata[0]):
                continue
            else:
                yield Move(*rowdata)

def processHTMLFile(filepath):
    name = os.path.split(filepath)[1] + '.json'
    moves = sorted(list(filterDuplicateMoves(parseHTMLFramesFile(filepath))))
    with open(name, 'w') as f:
        f.write("{\"data\":")
        f.write(json.dumps(moves))
        f.write("}")
    print(name + " ...written. %d moves" % len(moves) )

def filterDuplicateMoves(moves):
    s = set()
    mvs = list(moves)
    for m in mvs:
        data = ''.join(m.Input+m.Level+m.Damage)
        if data not in s:
            s.add(data)
            yield m
    print("%d duplicates."% (len(list(mvs)) - len(list(s))))



def printSQLForCharInputs(tablename, moves):
    temp =\
'INSERT INTO `{}` (`input`,`startup`,`block`,`hit`,`counter`,`damage`,`level`)\
 VALUES (\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\");'
    for m in moves:
        print(temp.format(tablename, \
            m.Input,\
            m.Startup, \
            m.Block, \
            m.Hit, \
            m.Counter, \
            m.Damage, \
            m.Level))


def processHTMLFiles():
    for file in getHTMLFiles():
        processHTMLFile(file)

if __name__ == '__main__':
    print(sys.version)
    #processHTMLFiles()
    st = 'C:\\Users\\wdang\\Desktop\\wdang.github.io\\data\\frames\\html\\steve-t7-frames.html'    
    processHTMLFile(st)