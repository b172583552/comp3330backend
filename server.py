import json
import sqlite3

import flask
from flask import jsonify, request




app = flask.Flask(__name__)
#app.config["DEBUG"] = True # Enable debug mode to enable hot-reloader.
@app.route('/jobs')
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


@app.route('/patients', methods=['GET'])
def get_patients():
    carer_id = request.args.get('carer_id', default=1, type=int)
    conn = sqlite3.connect('caretaker.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM Patients WHERE carer_id=?", (carer_id,))
    patients = cur.fetchall()
    conn.close()


    patients_list = []
    for patient in patients:
        patients_list.append(
            {
                "id": patient[0],
                "carer_id": patient[1],
                "name": patient[2],
                "sex": patient[3],
                "age": patient[4],
                "address": patient[5],
                "tel": patient[6],
                "emergency_contact": patient[7],
                "emergency_number": patient[8]
            }
        )

    return jsonify(patients_list)

@app.route('/health_statistics', methods=['GET'])
def get_health_statistics():
    carer_id = request.args.get('carer_id', default=1, type=int)
    conn = sqlite3.connect('caretaker.db')
    cur = conn.cursor()

    cur.execute('''SELECT * FROM HealthStatistics,Patients 
                    WHERE HealthStatistics.patient_id=Patients.patient_id AND carer_id=?''', (carer_id,))
    statistics = cur.fetchall()

    conn.close()
    health_statistics = []
    for stat in statistics:
        patient = {
            "id": str(stat[0]),
            "name": stat[9],
            "gender": stat[10],
            "age": str(stat[11]),
            "health_statistics": {
                "height": str(stat[1]),
                "weight": str(stat[2]),
                "blood_pressure": stat[3],
                "pulse_rate": str(stat[4]),
                "medical_history": json.loads(stat[5]),  # assuming medical_history is stored in json format
                "blood_oxygen": str(stat[6])
            }
        }
        health_statistics.append(patient)

    return jsonify(health_statistics)


@app.route('/update_health_statistics', methods=['GET'])
def update_health_statistics():
    patient_id = request.args.get('patient_id', default=1, type=int)
    conn = sqlite3.connect('caretaker.db')
    cur = conn.cursor()

    cur.execute('''SELECT * FROM HealthStatistics,Patients 
                        WHERE HealthStatistics.patient_id=Patients.patient_id AND Patients.patient_id=?''', (patient_id,))
    stat = cur.fetchall()[0]


    conn.close()
    import random
    delta1=random.randint(-4, 4)
    delta2 = random.randint(-3, 3)
    delta3 = random.randint(-3, 3)
    delta4 = random.randint(-3, 3)
    delta5 = random.randint(-5, 5)
    b = stat[3].split('/')
    b[0] = int(b[0]) + delta2
    b[1] = int(b[1]) + delta3
    b = str(b[0]) + '/' + str(b[1])
    patient = {
            "id": str(stat[0]),
            "name": stat[9],
            "gender": stat[10],
            "age": str(stat[11]),
            "health_statistics": {
                "height": str(stat[1]),
                "weight": str(stat[2]+delta1),
                "blood_pressure": b,
                "pulse_rate": str(stat[4]+delta4),
                "medical_history": json.loads(stat[5]),  # assuming medical_history is stored in json format
                "blood_oxygen": str(stat[6]+delta5)
            }
    }


    return jsonify(patient)
# adds host="0.0.0.0" to make the server publicly available
app.run(host="0.0.0.0")
