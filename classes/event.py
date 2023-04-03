import httpx
from selectolax.parser import HTMLParser
import pandas as pd
from ./match import Match

class Event:
    def __init__(self,url:str) -> None:
        self.url = url
        self.html = HTMLParser(httpx.get(url).text)
        header = self.html.css('div.event-desc-item-value')
        
        self.info = pd.DataFrame({
            'dates' : header[0].text().strip(),
            'prize_pool' : header[1].text().strip(),
            'location' : header[2].text().strip()
        },index=['Info'])
        
        
        
    def get_matches(self,head=None):
        if hasattr(self,'matches'):
            return self.matches
        
            
        completed_matches = [Match(match) for match in self.html.css('a.wf-module-item')[slice(head)]
                                if match.css_first('div.ml-status').text() == 'Completed']
        self.matches = completed_matches
        return completed_matches
        
