import sys
# setting path
sys.path.append('../data-curation')
datacuration = __import__("data-curation")
import importlib
# mod = importlib.import_module("../data-curation")

import configparser
from flask import (
    Flask,
    request,
    render_template,
    session,
    send_file,
    send_from_directory,
    make_response,
    Blueprint,
    url_for,
)
import os
from os import path


from src.OwkinDataFrame import OwkinDataFrame
from src.Validator import Validator
from src.ValidatorCol import ValidatorCol
from src.ValidatorRow import ValidatorRow

# basedir = path.abspath(path.dirname(__file__))
app = Flask(__name__, template_folder='template')


@app.route("/")
def index():
    data_folder = "../data/"
    first_file = os.listdir(data_folder)[0]
    data_report = OwkinDataFrame(data_folder + first_file, row_threshold=0.2)
    data_report.cure_dataframe()

    return render_template(
        "index.html",
        data_report = data_report.get_dataset_metadata()
    )


if __name__ == '__main__':
    app.run(debug=True)