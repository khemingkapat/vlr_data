import httpx
from selectolax.parser import HTMLParser
import re
import pandas as pd
from classes import Event,Match


base_url = 'https://www.vlr.gg'

event_url = '/event/matches/1188/champions-tour-2023-lock-in-s-o-paulo/?series_id=all'

url = base_url + event_url

lock_in = Event(url)

lock_in.get_matches(3)
