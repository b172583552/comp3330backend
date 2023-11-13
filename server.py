import json
import sqlite3

import flask
app = flask.Flask(__name__)
#app.config["DEBUG"] = True # Enable debug mode to enable hot-reloader.
@app.route('/jobs')
def job():
    con = sqlite3.connect('caretaker.db')
    cursor = con.execute("SELECT * from JOBS;")
    allJobs = []
    for row in cursor:
        jobs = {}
        jobs["id"] = row[0]
        jobs["userid"] = row[1]
        jobs["jobtitle"] = row[2]
        jobs["place"] = row[3]
        jobs["jobdetails"] = row[4]
        jobs["jobtime"] = row[5]
        allJobs.append(jobs)
    con.close()
    outdata = json.dumps(allJobs)
    return outdata
# adds host="0.0.0.0" to make the server publicly available
app.run(host="0.0.0.0")
