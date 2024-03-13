import requests

url = 'https://lo2gdy.edupage.org/substitution/server/viewer.js?__func=getSubstViewerDayDataHtml'
body = {"__args": [None, {"date": "2024-03-08", "mode": "classes"}], "__gsh": "00000000"}

r = requests.post(url, json=body)

print(r.text)