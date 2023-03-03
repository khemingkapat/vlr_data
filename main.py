import httpx
from selectolax.parser import HTMLParser
import re

base_url = 'https://www.vlr.gg'

event_url = '/event/matches/1188/champions-tour-2023-lock-in-s-o-paulo/?series_id=all'

res = httpx.get(base_url+event_url)

html = HTMLParser(res.text)

matches = html.css('a.wf-module-item')

completed_matches = [match for match in matches if match.css_first('div.ml-status').text() == 'Completed']

for match in completed_matches:
    match_res = httpx.get(f'{base_url}{match.attributes["href"]}')

    match_html = HTMLParser(match_res.text)

    match_name = match_html.css_first('title').text().strip().split(' | ')[0].split(' vs. ')

    messy_match_result = match_html.css_first('div.js-spoiler').text()
    match_result = ' ' + ''.join(re.findall("[^\s-]",messy_match_result)) + ' '

    print(match_sum:=match_result.join(match_name))
