"""
  An API to communicate with Iserv
"""

from requests import Session
import json

class IServ:
  """
    An IServ server
  """

  session: Session
  iserv: str

  def __init__(self, iservName) -> None:
    self.session = Session()
    self.iserv = iservName

  def login(self, username: str, password: str) -> None:
    """
      Login into a iserv account and saves session
    """
    self.session.post(
      f"https://{self.iserv}/iserv/auth/login",
      data={
        "_username": username,
        "_password": password
      }
    )

  def getTimetable(self, startDate: str, endDate: str, schoolClass: str) -> dict:
    """
      Gets the timetable from your Iserv account
    """
    requestString = (
    f'  https://{self.iserv}/iserv/timetable/data?'
    '     filter={'
    f'      "startDate": "{startDate}",'
    f'      "endDate": "{endDate}",'
    '       "changesUntil": null,'
    f'      "classes":["{schoolClass}"],'
    '       "teachers":["%"],'
    '       "rooms":["%"]'
    '     }'
    ).replace(" ", "")
    timetable = self.session.get(
      requestString
    )
    return json.loads(timetable.content)
  
  def logout(self) -> None:
    """
      Logs out of the account
    """
    self.session.post(f"https://{self.iserv}/iserv/auth/logout")