from bs4 import BeautifulSoup
import requests
import json
import random


months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
days = [i for i in range(1, 32)]
horoscopes = []

for month in months:
    for day in days:
        # request
        url = "https://www.theglobeandmail.com/life/horoscopes/article-your-daily-horoscope-"+month+'-'+str(day)+"/"
        response = requests.get(url, timeout=random.randint(4,6))
        content = BeautifulSoup(response.content, "html.parser")

                # Append all horoscopes for that day
        for hscope in content.find_all('p', attrs={"class": "c-article-body__text"}):
            hscopeObject = {
                "text": hscope.text
            }

            horoscopes.append(hscopeObject)
            # Remove the last text which isn't a horoscope
        horoscopes.pop()
        # print(horoscopes[-1]["text"].encode())

with open('theglobeandmail.json', 'w') as outfile:
    json.dump(horoscopes, outfile)
