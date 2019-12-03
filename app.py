# -*- coding: utf-8 -*-
# Copyright (c) 2018-2019 Linh Pham
# graphs.wwdt.me is relased under the terms of the Apache License 2.0
"""Flask application startup file"""

from collections import OrderedDict
from datetime import date, datetime
import json
from typing import Text
import traceback

from dateutil import parser
from flask import Flask, redirect, render_template, Response, url_for
from flask.logging import create_logger
import mysql.connector
import pytz
from slugify import slugify
from werkzeug.exceptions import HTTPException

#region Global Constants
APP_VERSION = "0.1.0"

#endregion

#region Flask App Initialization
app = Flask(__name__)
app.url_map.strict_slashes = False
app_logger = create_logger(app)

# Override base Jinja options
app.jinja_options = Flask.jinja_options.copy()
app.jinja_options.update({"trim_blocks": True, "lstrip_blocks": True})
app.create_jinja_environment()

#endregion

#region Bootstrap Functions
def load_config():
    """Load configuration settings from config.json"""
    with open("config.json", "r") as config_file:
        config_dict = json.load(config_file)

    return config_dict

#endregion

#region Common Functions
def generate_date_time_stamp(time_zone: pytz.timezone = pytz.timezone("UTC")):
    """Generate a current date/timestamp string"""
    now = datetime.now(time_zone)
    return now.strftime("%Y-%m-%d %H:%M:%S %Z")

#endregion

#region Filters
@app.template_filter("pretty_jsonify")
def pretty_jsonify(data):
    """Returns a prettier JSON output for an object than Flask's default
    tojson filter"""
    return json.dumps(data, indent=2)

#endregion

#region Error Handlers
@app.errorhandler(Exception)
def handle_exception(error):
    """Handle exceptions in a slightly more graceful manner"""
    # Pass through any HTTP errors and exceptions
    if isinstance(error, HTTPException):
        return error

    # Handle everything else with a basic 500 error page
    error_traceback = traceback.format_exc()
    app_logger.error(error_traceback)
    return render_template("errors/500.html",
                           error_traceback=error_traceback), 500

#endregion

#region General Redirect Routes


#endregion

#region Default Route
@app.route("/")
def index():
    """Default page that includes details for recent shows"""
    database_connection.reconnect()

#endregion

#region Sitemap XML Route


#endregion

#region Panelist Routes


#endregion

#region Show Routes


#endregion

#region Application Initialization
config = load_config()
app.jinja_env.globals["app_version"] = APP_VERSION
app.jinja_env.globals["current_date"] = date.today()
app.jinja_env.globals["ga_property_code"] = config["settings"]["ga_property_code"]
app.jinja_env.globals["rendered_at"] = generate_date_time_stamp
database_connection = mysql.connector.connect(**config["database"])
database_connection.autocommit = True

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port="9257")


#endregion
