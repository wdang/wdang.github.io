from collections import namedtuple
import requests
import bs4
import csv
import sys
import os
import functools
from bs4 import UnicodeDammit
from concurrent.futures import ProcessPoolExecutor
# LISTS OF SITES AND SEARCH PARAMETERS (OPTIONS?)

HEADERS = [
    ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
    ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.3'),
    ('Accept-Encoding', 'gzip,deflate,sdch'),
    ('Accept-Language', 'en-US,en;q=0.8'),
    ('Connection', 'keep-alive'),
    ('Referer', 'http://msdn.microsoft.com/en-us/library/aa383749(v=vs.85).aspx'),
    ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.41 \
        Safari 537.1')
]

SEARCH_SITES = [
    ('Metacritic', 'https://www.metacritic.com/search/all/%s/results')
]


SearchItem = namedtuple('SearchItem', [
    'title',
    'stats',
    'score',
])


def writefile(contents, path='default'):
    path = os.path.join(os.getcwd() + path)
    with open(path, 'wb') as f:
        f.write(contents)


def metacritic(query, media_type='all'):
    search_options = ['all', 'movie', 'game']
    assert media_type in search_options

    site = 'https://www.metacritic.com/search/%s/%s/results'
    site= 'http://geppopotamus.info/game/tekken7fr/steve/data_en.htm'
    req = requests.get(site % (media_type, query), headers=dict(HEADERS))
    soup = bs4.BeautifulSoup(req.text, 'html.parser')
    results = soup.find_all(class_="result_wrap")
    if results is None:
        yield
#    urls = []
#    for r in results:
#        urls.append(baseurl + r.select('a[href]')[0].get('href'))

    for r in results:
        title = [text for text in r.find(
            class_='product_title').stripped_strings]
        title = ' '.join(title)

        stats = [text for text in r.find('p').stripped_strings]
        stats = ' '.join(stats)

        score = r.find(class_='metascore_w')
        score = '' if score is None else score.text

        yield SearchItem(title, stats, score)


def getcsvcontents(filename):
    f = open(filename)
    return csv.reader(f)


def metacriticgames(query):
    result = metacritic(query, 'game')
    result = [r for r in result if "PS4" in r.stats]
    if len(result) < 1:
        print(query, "No Results.")
    else:
        print(query, result[0].score)




def multiproc():
    os.chdir("D:\\OneDrive")
    outputs = []
    csvdata = csv.reader(open('PSN SUMMER SALES.csv'))
    titles = [item[0] for item in csvdata]
    pool = ProcessPoolExecutor(max_workers=4)
    results = list(pool.map(metacriticgames, titles))
     # csvwriter = csv.writer(open('example.csv', 'w'))
    # csvwriter.writerows(outputs)

if __name__ == '__main__':
    name = "Lee Chaolan"
    csvdata = csv.reader(open('frames/' + name + '.csv'))
    data = "[\
    \"{0}\",\n\
    \"{1}\",\n\
    \"{2}\",\n\
    \"{3}\",\n\
    \"{4}\",\n\
    \"{5}\",\n\
    \"{6}\"\n\
]"  

    with open(name + ".json",'w') as f:
        f.write("{\"data\":[")
        for row in csvdata:
            f.write(data.format(*row) + ',')
        f.write("]}")
