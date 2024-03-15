import requests
import json
from bs4 import BeautifulSoup

def get_substitutions(schoolName, date):
    url = f'https://{schoolName}.edupage.org/substitution/server/viewer.js?__func=getSubstViewerDayDataHtml'
    body = {"__args": [None, {"date": f"{date}", "mode": "classes"}], "__gsh": "00000000"}

    res = requests.post(url, json=body)

    data = json.loads(res.text)
    soup = BeautifulSoup( data["r"],"html.parser" )
    # print(soup.prettify())


    finalJson = {
        "absentTeachers":None,
        "absentClasses":None,
        "unavalibleClassRooms":None,
        "substitutions":[],
            }
    
    
    classSubstitutions = soup.find_all("div", class_="print-nobreak")


    for classData in classSubstitutions:

        className = classData.find("div", class_="header").string

        # print(className)

        substitutions = classData.find_all("div", class_="row")
        substitutionsArray = []
        for substitution in substitutions:

            hour = substitution.find("div", class_="period").string
            # print(hour)
        
            info = substitution.find("div", class_="info").string 
            # print(info)

            substitutionsArray.append({"hour":hour, "info":info})
           

        if className: 
          finalJson["substitutions"].append({
            "className": className,
            "substitutions":substitutionsArray
        })


    
    return finalJson
    
print(get_substitutions("", "2024-03-15"))
