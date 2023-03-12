import re
import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from google.auth import load_credentials_from_file
from google_calender import GoogleCalender

if __name__ == "__main__":
    SCOPES = ["https://www.googleapis.com/auth/calendar"]
    CALENDAR_ID = "94e385f65940aa9dfb1b2cd2d929e7f67741440aa0d43c98f837620793cd4631@group.calendar.google.com"
    TARGETS = ["豪", "日本", "ユーロ", "英国", "アメリカ", "カナダ"]
    gapi_creds = load_credentials_from_file("credentials.json", SCOPES)[0]
    service = build("calendar", "v3", credentials=gapi_creds)

    gcal = GoogleCalender()
    gcal.delete_events("2023-03-12 00:00","2023-03-18 00:00")

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
                idx = name.find("・")
                country = name[:idx]
                if country in TARGETS:
                    if date_obj is None:
                        events.append(
                            {
                                "date": date_time,
                                "events": [name],
                                "countries": [country],
                            }
                        )
                    else:
                        date_obj["events"].append(name)
                        if country not in date_obj["countries"]:
                            date_obj["countries"].append(country)

    for event in events:
        gcal.add_events(
            "🗓️"+"・".join(event["countries"]),
            event["date"],
            event["date"],
            "\n\n".join(event["events"]),
        )
