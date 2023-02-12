from datetime import datetime
from googleapiclient.discovery import build
from google.auth import load_credentials_from_file


class GoogleCalender:
    __CALENDAR_ID = "94e385f65940aa9dfb1b2cd2d929e7f67741440aa0d43c98f837620793cd4631@group.calendar.google.com"
    __service = build(
        "calendar",
        "v3",
        credentials=load_credentials_from_file(
            "credentials.json", ["https://www.googleapis.com/auth/calendar"]
        )[0],
    )

    def __init__(self, time_zone: str = "+09:00"):
        self.__time_zone = time_zone

    def __get_converted_date_time(self, date_time: str):
        return (
            datetime.strptime(date_time, "%Y-%m-%d %H:%M").isoformat()
            + self.__time_zone,
        )[0]

    def add_events(
        self, title: str, start_date_time: str, end_date_time: str, description: str
    ):
        body = {
            "summary": title,
            "start": {"dateTime": self.__get_converted_date_time(start_date_time)},
            "end": {"dateTime": self.__get_converted_date_time(end_date_time)},
            "description": description,
        }

        self.__service.events().insert(  # pylint: disable=maybe-no-member
            calendarId=self.__CALENDAR_ID, body=body
        ).execute()

    def delete_events(self, start_date_time: str, end_date_time: str):
        events = (
            self.__service.events()  # pylint: disable=maybe-no-member
            .list(
                calendarId=self.__CALENDAR_ID,
                timeMin=self.__get_converted_date_time(start_date_time),
                timeMax=self.__get_converted_date_time(end_date_time),
            )
            .execute()
        )

        for item in events["items"]:
            self.__service.events().delete(  # pylint: disable=maybe-no-member
                calendarId=self.__CALENDAR_ID, eventId=item["id"]
            ).execute()
