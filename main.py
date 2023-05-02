from classes import Event


base_url = "https://www.vlr.gg"

event_url = "/event/matches/1188/champions-tour-2023-lock-in-s-o-paulo/?series_id=all"

url = base_url + event_url

lock_in = Event(url)

for match in lock_in.get_matches(3):
    print(match.get_scoreboard())
