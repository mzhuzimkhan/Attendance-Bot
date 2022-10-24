from pymongo import MongoClient
from fastapi import FastAPI

app = FastAPI()
connection_string = "mongodb://localhost:27017"
client = MongoClient(connection_string)
db = client["telegram_bot"]
users = db["users"] 
attendance = db["attendance"]


@app.get("/worked_days")
def get_workdays(name: str, date: str = "2022-06"):
    
    n = attendance.find({},{"_id":0})
    list_of_attendance = []
    for nm in n:
        dt = nm["date"][0:7]
        if name == nm["name"] and dt == date:
            list_of_attendance.append(nm)
    return list_of_attendance

@app.get("/usernames")
def get_usernames():
    n = attendance.find({},{"_id":0})
    list_of_usernames = []
    for nm in n:
        list_of_usernames.append(nm["name"])
    return list_of_usernames


@app.get("/monthly_attendance")
def monthly_attendance(name: str, date: str):
    n = attendance.find({},{"_id":0})
    worked_days = 0
    little_late_days = 0
    super_late_days = 0
    late = '11:00:00'
    factors = (60, 1, 1/60)
    for nm in n:
        dt = nm["date"][0:7]
        if name == nm["name"] and dt == date:
            worked_days += 1
            my_time = nm["time"]
            t1 = sum(i*j for i, j in zip(map(int, my_time.split(':')), factors))
            t2 = sum(i*j for i, j in zip(map(int, late.split(':')), factors))

            if 0<t1 - t2 <= 30:
                little_late_days += 1
            if t1 - t2 > 30 :
                super_late_days += 1
                
    list_of_attendance = {
        "Worked days" : worked_days,
        "Little late days" : little_late_days,
        "Super late days" : super_late_days
    }
    return list_of_attendance