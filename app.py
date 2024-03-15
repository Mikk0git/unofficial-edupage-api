import requests
import json
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify

app = Flask(__name__)


def get_substitutions(schoolName, date):
    url = f'https://{schoolName}.edupage.org/substitution/server/viewer.js?__func=getSubstViewerDayDataHtml'
    body = {"__args": [None, {"date": f"{date}",
                              "mode": "classes"}], "__gsh": "00000000"}

    res = requests.post(url, json=body)
    if res.status_code != 200:
        return {"error": "Error retrieving substitutions."}, 500

    data = json.loads(res.text)
    soup = BeautifulSoup(data["r"], "html.parser")

    finalJson = {"all_substitutions": []}

    classSubstitutions = soup.find_all("div", class_="print-nobreak")

    for classData in classSubstitutions:
        className = classData.find("div", class_="header").string
        substitutions = classData.find_all("div", class_="row")
        substitutionsArray = []
        for substitution in substitutions:
            hour = substitution.find("div", class_="period").string
            info = substitution.find("div", class_="info").string
            substitutionsArray.append({"hour": hour, "info": info})

        if className:
            finalJson["all_substitutions"].append({
                "name": className,
                "substitutions": substitutionsArray
            })

    return finalJson, 200


@app.route('/get_substitutions', methods=['GET'])
def substitutions_endpoint():
    school_name = request.args.get('school_name')
    date = request.args.get('date')

    if school_name is None or date is None:
        return jsonify({"error": "Please provide both 'school_name' and 'date' parameters."}), 400

    substitutions, status_code = get_substitutions(school_name, date)
    return jsonify(substitutions), status_code


if __name__ == '__main__':
    app.run(debug=True)  # You can set debug=False for production
