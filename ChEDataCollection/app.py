

from flask import Flask, render_template, request, make_response, redirect
import PIconnect as PI
import pandas as pd

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/download', methods=["POST"])
def download():
    project = request.form.get("project")
    date = request.form.get("start")
    start_time = request.form.get("starttime")
    end_time = request.form.get("endtime")
    interval = request.form.get("interval")

    project_num = "*" + project + "*"
    project_start = date + " " + start_time
    project_end = date + " " + end_time


    PI.PIConfig.DEFAULT_TIMEZONE = 'America/Indianapolis'
    with PI.PIServer() as server:
        if project_num == "*300*":
            points = server.search("*300*") + server.search("*301*") + server.search("*303*") + server.search("*321*") + server.search("*331*") + server.search("*332*") + server.search("*333*") + server.search("*334*")
        else:
            points = server.search(project_num)


    df = pd.concat([point.interpolated_values(project_start, project_end, interval).to_frame(point.name + ' ' + point.units_of_measurement) for point in points], axis = 1)

    df.index.rename('Timestamp', inplace = True)

    response=make_response(df.to_csv())
    cd = 'attachment; filename=CHE Lab Data.csv'
    response.headers['Content-Disposition'] = cd
    response.mimetype = 'text/csv'

    return response


if __name__ == '__main__':
    app.run()


