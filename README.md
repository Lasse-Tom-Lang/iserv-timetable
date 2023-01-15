# Iserv Timetable

[Live demo](https://timetable-80-cdtsiupudi9mmk5gqh00.apps.playground.napptive.dev/getTimetable?iservName=ISERV_URL&username=ISERV_USERNAME&password=ISERV_PASSWORD&schoolClass=CLASS) 
Just add your account details

A script which creates an api server from which you can get your IServ timetable.

Requests:
`URL/getTimetable?iservName=ISERV_URL&username=ISERV_USERNAME&password=ISERV_PASSWORD&schoolClass=CLASS`

You can run the server by running:
`sudo uvicorn server:app --reload --port 80 --host 0.0.0.0`

or use the `Docker` image