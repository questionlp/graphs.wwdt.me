# -*- coding: utf-8 -*-
# Copyright (c) 2018-2019 Linh Pham
# graphs.wwdt.me is relased under the terms of the Apache License 2.0
"""Flask application startup file"""

from datetime import date, datetime
import json
from typing import Text
import traceback

from flask import Flask, redirect, render_template, Response, url_for
from flask.logging import create_logger
import mysql.connector
import pytz
from slugify import slugify
from werkzeug.exceptions import HTTPException
from wwdtm.panelist import info as pnl_info

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
    return render_template("pages/index.html")

#endregion

#region Sitemap XML Route


#endregion

#region Panelist Routes
@app.route("/panelists")
def panelists_index():
    """Panelists Index Page"""
    return render_template("panelists/index.html")

@app.route("/panelists/score-breakdown")
def panelists_score_breakdown_index():
    """Panelists Score Breakdown Index Page"""
    database_connection.reconnect()
    panelists = pnl_info.retrieve_all(database_connection)
    return render_template("panelists/score-breakdown/index.html",
                           panelists=panelists)

@app.route("/panelists/score-breakdown/<string:panelist>")
def panelists_score_breakdown_details(panelist: Text):
    """Panelists Score Breakdown Index Page"""
    database_connection.reconnect()
    panelist_slug = slugify(panelist)
    if panelist and panelist != panelist_slug:
        return redirect(url_for("panelists_score_breakdown_details",
                                panelist=panelist_slug))

    info = pnl_info.retrieve_by_slug(panelist, database_connection)
    scores = pnl_info.retrieve_scores_grouped_list_by_slug(panelist,
                                                           database_connection)
    return render_template("panelists/score-breakdown/details.html",
                           panelist_info=info,
                           panelist_slug=panelist_slug,
                           scores=scores)

@app.route("/panelists/scores-by-appearance")
def panelists_scores_by_appearance_index():
    """Panelists Scores by Appearance Index Page"""
    database_connection.reconnect()
    return render_template("panelists/scores-by-appearance/index.html")

@app.route("/panelists/scores-by-appearance/<string:panelist>")
def panelists_scores_by_appearance_details(panelist: Text):
    """Panelists Scores by Appearance Index Page"""
    database_connection.reconnect()
    panelist_slug = slugify(panelist)
    if panelist and panelist != panelist_slug:
        return redirect(url_for("panelists_scores_by_appearance_details",
                                panelist=panelist_slug))

    scores = pnl_info.retrieve_scores_ordered_pair_by_slug(panelist,
                                                           database_connection)
    return render_template("panelists/scores-by-appearance/details.html",
                           scores=scores)

#endregion

#region Show Routes


#endregion

#region Application Initialization
config = load_config()
app.jinja_env.globals["app_version"] = APP_VERSION
app.jinja_env.globals["current_date"] = date.today()
app.jinja_env.globals["ga_property_code"] = config["settings"]["ga_property_code"]
app.jinja_env.globals["rendered_at"] = generate_date_time_stamp

app.jinja_env.globals["api_url"] = config["settings"]["api_url"]
app.jinja_env.globals["blog_url"] = config["settings"]["blog_url"]
app.jinja_env.globals["reports_url"] = config["settings"]["reports_url"]
app.jinja_env.globals["stats_url"] = config["settings"]["stats_url"]

database_connection = mysql.connector.connect(**config["database"])
database_connection.autocommit = True

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port="9257")


#endregion
