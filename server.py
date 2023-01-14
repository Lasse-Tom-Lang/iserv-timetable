from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import json
import datetime
from iserv import IServ

def hourToName(hour: str) -> str:
  fachListe = {
    "M": "Mathe",
    "E": "Englisch",
    "C": "Chemie",
    "F": "Französisch",
    "S J": "Sport Jungs",
    "S M": "Sport Mädchen",
    "S": "Sport",
    "Et": "Ethik",
    "Re": "Religion evangelisch",
    "Rk": "Religion katholisch",
    "G": "Geschichte",
    "NwT": "NwT",
    "P": "Physik",
    "D": "Deutsch",
    "B": "Biologie",
    "PXE": "PX Englisch",
    "PXM": "PX Mathe",
    "PXD": "PX Deutsch",
    "Geo": "Geographie",
    "Gk": "Gemeinschaftskunde",
    "WBS": "Wirtschaft",
    "Sp": "Spanisch",
    "Mu": "Musik"
  }
  if (hour in fachListe):
    return fachListe[hour]
  else:
    return hour

def saveData(data: dict, fileName: str):
  """
    Saves a dictionary as a json file
  """
  with open(fileName, "w") as file:  
   file.write(json.dumps(data))

def timetableToString(timetable: dict) -> str:
  text = ""
  text += f'Stundenplan für {timetable["meta"]["filter"]["classes"][0]} am {timetable["meta"]["filter"]["startDate"]}<br><br><br>'
  currentHour = 0
  for hour in timetable["data"]["timetable"]:
    fach = hourToName(hour["subject"])
    try:
      hour["change"]
      if ("0" not in hour["change"]["change_types"]):
        if (hour["change"]["substitutionSubject"] != ""):
          fach = hourToName(hour["change"]["substitutionSubject"])
        if (currentHour == hour["period"]):
          text += f'und Änderung {fach} in Raum {hour["change"]["substitutionRoom"]}<br><br>'
        else:
          text += f'{hour["period"]}. Stunde Änderung {fach} in Raum {hour["change"]["substitutionRoom"]}<br><br>'
      else:
        if (currentHour == hour["period"]):
          text += f'und {fach} in Raum {hour["room"]} entfällt<br><br>'
        else:
          text += f'{hour["period"]}. Stunde {fach} in Raum {hour["room"]} entfällt<br><br>'
    except:
      if (currentHour == hour["period"]):
        text += f'und {fach} in Raum {hour["room"]}<br><br>'
      else:
        text += f'{hour["period"]}. Stunde {fach} in Raum {hour["room"]}<br><br>'
    currentHour = hour["period"]
  return text

def getDate() -> tuple[str, str]:
  date = datetime.datetime.now().strftime('%d.%m.%Y')
  if (datetime.datetime.now().weekday() == 5):
      date = (datetime.datetime.now() + datetime.timedelta(days=2)).strftime('%d.%m.%Y')
  if (datetime.datetime.now().weekday() == 6):
    date = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%d.%m.%Y')
  if (datetime.datetime.now().hour >= 17):
    if (datetime.datetime.now().weekday() == 4):
      date = (datetime.datetime.now() + datetime.timedelta(days=3)).strftime('%d.%m.%Y')
    elif (datetime.datetime.now().weekday() == 5):
      date = (datetime.datetime.now() + datetime.timedelta(days=2)).strftime('%d.%m.%Y')
    else:
      date = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%d.%m.%Y')
  return date, date

def main(iservName: str, username: str, password: str, schoolClass: str):
  startDate, endDate = getDate()
  
  try:
    iserv = IServ(iservName)

    iserv.login(username, password)

    timetable = iserv.getTimetable(startDate, endDate, schoolClass)

    iserv.logout()

    #saveData(timetable, "save.json")

    return timetableToString(timetable)
  except:
    return "Etwas ist schiefgelaufen"

app = FastAPI()

@app.get("/getTimetable")
async def getTimetable(iservName: str = "", username: str = "", password: str = "", schoolClass: str = ""):
    return HTMLResponse(main(iservName, username, password, schoolClass))