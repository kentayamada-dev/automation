import re
import datetime
import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from google.auth import load_credentials_from_file

SCOPES = ["https://www.googleapis.com/auth/calendar"]
CALENDAR_ID = "5bcee2db8b6795c4bfb39a7b44bf14097532baf03054ef1611ef16950f9fd71d@group.calendar.google.com"
gapi_creds = load_credentials_from_file("credentials.json", SCOPES)[0]
service = build("calendar", "v3", credentials=gapi_creds)

events = []

one_week_economic_events = BeautifulSoup(
    requests.get("https://fx.minkabu.jp/indicators", timeout=10).content, "html5lib"
)

for each_day_economic_events in one_week_economic_events.find_all("table"):
    raw_date = each_day_economic_events.find("caption")
    if raw_date:
        date = raw_date.get_text().strip()
        economic_events = each_day_economic_events.find_all("tr")
        for economic_event in economic_events:
            economic_event_data = economic_event.find_all("td")
            time = economic_event_data[0].get_text().strip()
            if time == "未定":
                continue
            name = (
                economic_event_data[1]
                .get_text()
                .strip()
                .replace(" ", "")
                .replace("\n", " ")
            )
            regex = re.compile(r"((19|20)\d\d)[-/年]((0|1)?\d)[-/月]((0|1|2|3)?\d)日?")
            formattedDate = re.sub(
                r"\([^)]*\)", "", regex.sub(r"\1/\3/\5", date)
            ).replace("/", "-")
            date_time = formattedDate + " " + time
            date_obj = next((x for x in events if x["date"] == date_time), None)
            if date_obj is None:
                events.append({"date": date_time, "events": [name]})
            else:
                date_obj["events"].append(name)

for event in events:
    countries = []
    for event_name in event["events"]:
        idx = event_name.find("・")
        countries.append(event_name[:idx])
    countries = list(set(countries))

    body = {
        "summary": "・".join(countries),
        "start": {
            "dateTime": datetime.datetime.strptime(
                event["date"], "%Y-%m-%d %H:%M"
            ).isoformat(),
            "timeZone": "Japan",
        },
        "end": {
            "dateTime": datetime.datetime.strptime(
                event["date"], "%Y-%m-%d %H:%M"
            ).isoformat(),
            "timeZone": "Japan",
        },
        "description": "\n\n".join(event["events"]),
    }

    service.events().insert(calendarId=CALENDAR_ID, body=body).execute()
