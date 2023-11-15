import json
import sqlite3

import flask
from flask import request, jsonify

app = flask.Flask(__name__)


# app.config["DEBUG"] = True # Enable debug mode to enable hot-reloader.
@app.route('/jobs', methods=["GET", "POST"])
def job():


    if request.method == "POST":
        con = sqlite3.connect('caretaker.db')
        print(request.form.values())
        userId = request.form.get('userId')
        print(userId)
        careTakingID = request.form.get('careTakingId')
        print(userId)
        cursor = con.execute("SELECT * FROM JOBS where UserID = " + userId +" and ID = " + careTakingID)
        row = cursor.fetchone()
        print(row)

        if row is None:
            sql = "UPDATE JOBS SET UserID = " + userId + " where ID = " + careTakingID +";"
            print(sql)
            cursor = con.execute(sql)
            con.commit()
            con.close()
            return jsonify(success=True), 200
        else:
            sql = "UPDATE JOBS SET UserID = NULL where ID = "+careTakingID+";"
            print(sql)
            cursor = con.execute(sql)
            con.commit()
            con.close()
            return jsonify(success=True), 200


    if request.method == "GET":
        con = sqlite3.connect('caretaker.db')
        cursor = con.execute("SELECT * from JOBS;")
        allJobs = []
        for row in cursor:
            jobs = {}
            jobs["id"] = row[0]
            jobs["userId"] = row[1]
            jobs["jobTitle"] = row[2]
            jobs["place"] = row[3]
            jobs["jobDetails"] = row[4]
            jobs["jobTime"] = row[5]
            jobs["salary"] = row[6]
            allJobs.append(jobs)
        outdata = json.dumps(allJobs)
        con.close()
        return outdata





# adds host="0.0.0.0" to make the server publicly available
app.run(host="0.0.0.0")
