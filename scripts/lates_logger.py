import os
import mysql_manager

lates = []

def save(name: str, minutes: int):
    saved = None

    for x in lates:
        if x.get("name") == name:
            saved = name
            break

    if saved == None:
        print(name + " arrived in time!" if minutes < 2 else name + " is " + str(minutes) + " minutes late!")
        lates.append({"name": name, "latency": minutes})

def log():
    f = open("lates.json", "w")

    f.write('{"lates": ' + str(lates).replace('\'', '"') + '}')
    f.close()