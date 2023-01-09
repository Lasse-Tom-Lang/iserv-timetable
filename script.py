from requests import Session
import json
import os
from dotenv import load_dotenv
from datetime import datetime

def login(session: Session, iserv: str, username: str, password: str):
  """
    Login into a iserv account and saves session
  """
  session.post(
    f"https://{iserv}/iserv/auth/login",
    data={
      "_username": username,
      "_password": password
    }
  )

def getTimetable(session: Session, iserv: str, startDate: str, endDate: str, schoolClass: str) -> dict:
  requestString = (
  f'  https://{iserv}/iserv/timetable/data?'
  '     filter={'
  f'      "startDate": "{startDate}",'
  f'      "endDate": "{endDate}",'
  '       "changesUntil": null,'
  f'      "classes":["{schoolClass}"],'
  '       "teachers":["%"],'
  '       "rooms":["%"]'
  '     }'
  ).replace(" ", "")
  timetable = session.get(
    requestString
  )
  return json.loads(timetable.content)

def saveData(data: dict, fileName: str):
  """
    Saves a dictionary as a json file
  """
  with open(fileName, "w") as file:  
   file.write(json.dumps(data))

def timetableToString(timetable: dict):
  print(f'Timetable for {timetable["meta"]["filter"]["classes"][0]} at {timetable["meta"]["filter"]["startDate"]}')
  for hour in timetable["data"]["timetable"]:
    print(f'{hour["period"]}. Hour {hour["subject"]} at {hour["room"]}')

def main():
  load_dotenv()
  iserv = os.getenv("iserv")
  username = os.getenv("username")
  password = os.getenv("password")
  schoolClass = os.getenv("schoolClass")
  startDate = datetime.now().strftime('%d.%m.%Y')
  endDate = datetime.now().strftime('%d.%m.%Y')

  session = Session()

  login(session, iserv, username, password)

  timetable = getTimetable(session, iserv, startDate, endDate, schoolClass)

  saveData(timetable, "save.json")

  timetableToString(timetable)

if __name__ == "__main__":
  main()