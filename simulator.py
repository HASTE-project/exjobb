"""This module gives the simulator an interface. By starting simulator.py a Flask app is started and from the
web UI the user can change settings for the microscope simulator. The result is the same as starting
simulatorNoFlask.get_file(*args*)."""

from flask import Flask, render_template, request

import simulator_no_flask

app = Flask(__name__)


@app.route("/fileWalk")
def file_walk():
    return render_template('file_walk_page.html')


@app.route("/fileWalk", methods=['POST'])
def file_walk_post():
    file_path = request.form["file_path"]
    period = request.form["period"]
    binning = int(request.form["binning"])
    color_channel = request.form.getlist("color_channel")
    connect_kafka = request.form["kafka"] # Review: better to parse to a boolean here,
    #  rather than checking against a string in the other places
    # Review2: better to spec which streaming fw to use? 
    period = float(period)
    simulator_no_flask.get_files(file_path, period, binning, color_channel, connect_kafka)
    return "You have now streamed all your files"


if __name__ == "__main__":
    app.run(debug=True)
