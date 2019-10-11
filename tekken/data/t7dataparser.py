import os
import sys
import json
import re
from pprint import pprint
from collections import namedtuple
from bs4 import BeautifulSoup

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

Move = namedtuple('Move', fields, defaults=('',) * len(fields))


def processAnna(filepath):
    print('processAnna')


PARSING_RULES = {
    'anna-t7-frames.html': processAnna
}


def replaceNonAscii(s, replacement=''):
    return ''.join([c if ord(c) < 128 else replacement for c in s])


def extractMoveList(filepath):
    key = os.path.split(filepath)[1]
    if key in PARSING_RULES:
        PARSING_RULES[key](filepath)
    else:
        with open(filepath, encoding="utf8") as f:
            soup = BeautifulSoup(f, 'html.parser')
            rows = soup.find_all('tr')
            for r in rows:
                rowdata = [replaceNonAscii(''.join(td.stripped_strings))
                           for td in r.find_all('td')]
                if rowdata:
                    if re.match('[Cc]ommand', rowdata[0]):
                        continue

                    if len(rowdata) >= 8:
                        yield Move(*rowdata[:8])

                    else:
                        yield Move(*rowdata)
                else:
                    print("Entry not added:", rowdata)


def filterDuplicateMoves(moves):
    s = set()
    for m in moves:
        data = ''.join(m.Input+m.Level+m.Block)
        if data not in s:
            s.add(data)
            yield m


def printSQLForCharInputs(tablename, moves):
    temp =\
        'INSERT INTO `{}` (`input`,`startup`,`block`,`hit`,`counter`,`damage`,`level`)\
 VALUES (\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\");'
    for m in moves:
        print(temp.format(tablename,
                          m.Input,
                          m.Startup,
                          m.Block,
                          m.Hit,
                          m.Counter,
                          m.Damage,
                          m.Level))


def processHTMLFile(filepath):
    name = os.path.split(filepath)[1] + '.json'
    outpath = os.path.join(os.getcwd() + '\\frames\\json', name)
    moves = sorted(list(filterDuplicateMoves(extractMoveList(filepath))))
    print(outpath + " (%d moves)" % len(moves))
    with open(outpath, 'w') as f:
        f.write("{\"data\":")
        f.write(json.dumps(moves))
        f.write("}")


def getHTMLFiles():
    htmlfilespath = os.getcwd() + '\\frames\\html'
    return (htmlfilespath + '\\' + name for root, dirs, files in os.walk(htmlfilespath) for name in files)


def processMoveList(moves):
    moveprops = {}
    moves = list(moves)
    for m in moves:
        moveprops[m.Input] = []

    re_launcher = re.compile(r'[Ll]aunch|[Cc][Ss]|[Jj][Gg]')
    re_tailspin = re.compile(r'[Tt]ail')
    re_lowcrush = re.compile(r'[Tt][Jj]')
    re_highcrush = re.compile(r'[Tt][Cc]')
    re_tracking = re.compile(r'[Hh]om')
    re_wallbounce = re.compile(r'[Ww]all')
    re_forcecrouch = re.compile(r's')

    launchers = {m.Input for m in moves if re_launcher.search(m.Counter)}
    tailspins = {m.Input for m in moves if re_tailspin.search(m.Notes)}
    tracking = {m.Input for m in moves if re_tracking.search(m.Notes)}
    lc = {m.Input for m in moves if re_lowcrush.search(m.Level)}
    hc = {m.Input for m in moves if re_highcrush.search(m.Level)}
    wb = {m.Input for m in moves if re_wallbounce.search(m.Notes)}
    fc = {m.Input for m in moves if re_forcecrouch.search(m.Block)} |\
        {m.Input for m in moves if re_forcecrouch.search(m.Hit)} |\
        {m.Input for m in moves if re_forcecrouch.search(m.Counter)}

    for i in launchers:
        moveprops[i].append('Launch')
    for i in tailspins:
        moveprops[i].append('Tailspin')
    for i in lc:
        moveprops[i].append('Low Crush')
    for i in hc:
        moveprops[i].append('High Crush')
    for i in fc:
        moveprops[i].append('Crouch')

    print("Moves: %1d\nCH Launchers: %d\nTailspins: %d\nLowCrush: %d\nHighCrush: %d\nTracking: %d" % (
        len(moves), len(launchers), len(tailspins), len(lc), len(hc), len(tracking)))


def getMoveList(filepath):
    return filterDuplicateMoves(extractMoveList(filepath))


def processHTMLFiles():
    for file in getHTMLFiles():
        processHTMLFile(file)


'''
EXPECTED #'S
(LAUNCERS,TRAILSPINS,LOWCRUSH,HIGHCRUSH,TRACKING)
'''
EXPECTED = {'kazumi-t7-frames.html': (95, 12, 6, 11, 8, 4),
            'kazuya-t7-frames.html': (132, 28, 5, 14, 11, 4)}


def verifyParsing(fp, moves):
    moves = list(moves)

    re_launcher = re.compile(r'[Ll]aunch|[Cc][Ss]|[Jj][Gg]')
    re_tailspin = re.compile(r'[Tt]ail')
    re_lowcrush = re.compile(r'[Tt][Jj]')
    re_highcrush = re.compile(r'[Tt][Cc]')
    re_tracking = re.compile(r'[Hh]om')
    re_wallbounce = re.compile(r'[Ww]all')
    re_forcecrouch = re.compile(r's')

    launchers = {m.Input for m in moves if re_launcher.search(m.Counter)}
    tailspins = {m.Input for m in moves if re_tailspin.search(m.Notes)}
    tracking = {m.Input for m in moves if re_tracking.search(m.Notes)}
    lc = {m.Input for m in moves if re_lowcrush.search(m.Level)}
    hc = {m.Input for m in moves if re_highcrush.search(m.Level)}
    wb = {m.Input for m in moves if re_wallbounce.search(m.Notes)}
    fc = {m.Input for m in moves if re_forcecrouch.search(m.Block)} |\
        {m.Input for m in moves if re_forcecrouch.search(m.Hit)} |\
        {m.Input for m in moves if re_forcecrouch.search(m.Counter)}

    result = (len(moves), len(launchers), len(
        tailspins), len(lc), len(hc), len(tracking))

    key = EXPECTED[os.path.split(fp)[1]]
    try:
        assert (key == result)
    except AssertionError as e:
        print("(#LAUNCERS, #TRAILSPINS, #LOWCRUSH, #HIGHCRUSH, #TRACKING)")
        print("result:   ", result)
        print("expected: ", key)
        raise e


if __name__ == '__main__':
    fp = 'C:\\Users\\wdang\\Desktop\\wdang.github.io\\data\\frames\\html\\kazumi-t7-frames.html'
    mvs = sorted(list(getMoveList(fp)))
    processMoveList(mvs)
    verifyParsing(fp, mvs)


def hello():
    print('hello')
