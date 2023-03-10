import httpx
from selectolax.parser import HTMLParser
import re
import pandas as pd

base_url = 'https://www.vlr.gg'

event_url = '/event/matches/1188/champions-tour-2023-lock-in-s-o-paulo/?series_id=all'

res = httpx.get(base_url+event_url)

html = HTMLParser(res.text)

matches = html.css('a.wf-module-item')

completed_matches = [match for match in matches if match.css_first('div.ml-status').text() == 'Completed']

for match in completed_matches[:2]:
    match_res = httpx.get(match_url := f'{base_url}{match.attributes["href"]}')

    match_html = HTMLParser(match_res.text)

    match_name = match_html.css_first('title').text().strip().split(' | ')[0].split(' vs. ')

    messy_match_result = match_html.css_first('div.js-spoiler').text()
    match_result = ' ' + ''.join(re.findall("\S+",messy_match_result)) + ' '

    print(match_sum:=match_result.join(match_name))

    tables = match_html.css('table.wf-table-inset')

    for table in tables:
        for t in pd.read_html(table.html):
            t.iloc[:,2:] = t.iloc[:,2:].applymap(lambda r : r.split(' ')[0])
            t = t.dropna(axis='columns',how='all')
            print(t)


