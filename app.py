# -*- coding: utf-8 -*-
# Copyright (c) 2018-2020 Linh Pham
# graphs.wwdt.me is relased under the terms of the Apache License 2.0
"""Flask application startup file"""

from datetime import date
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
from wwdtm.show import info as show_info
from graphs import utility
from reports.panel import aggregate_scores, gender_mix

#region Global Constants
APP_VERSION = "1.5.0.1"

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

    if "time_zone" in config_dict["settings"] and config_dict["settings"]["time_zone"]:
        time_zone = config_dict["settings"]["time_zone"]
        time_zone_object, time_zone_string = utility.time_zone_parser(time_zone)

        config_dict["settings"]["app_time_zone"] = time_zone_object
        config_dict["settings"]["time_zone"] = time_zone_string
        config_dict["database"]["time_zone"] = time_zone_string
    else:
        config_dict["settings"]["app_time_zone"] = pytz.timezone("UTC")
        config_dict["settings"]["time_zone"] = "UTC"
        config_dict["database"]["time_zone"] = "UTC"

    return config_dict

#endregion

#region Common Functions
def retrieve_show_years(reverse_order: bool = True):
    """Retrieve a list of available show years"""
    database_connection.reconnect()
    years = show_info.retrieve_years(database_connection)
    if years and reverse_order:
        years.reverse()

    return years

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

#region Default Route
@app.route("/")
def index():
    """Default page that includes details for recent shows"""
    return render_template("pages/index.html")

#endregion

#region Sitemap XML Route
@app.route("/sitemap.xml")
def sitemap_xml():
    """Default Sitemap XML"""
    database_connection.reconnect()
    show_years = retrieve_show_years(reverse_order=False)
    panelists = pnl_info.retrieve_all(database_connection)
    sitemap = render_template("core/sitemap.xml",
                              show_years=show_years,
                              panelists=panelists)
    return Response(sitemap, mimetype="text/xml")

#endregion

#region Panelist Routes
@app.route("/panelists")
def panelists_index():
    """Panelists Index Page"""
    return render_template("panelists/index.html")

@app.route("/panelists/aggregate-scores")
def panelists_aggregate_scores():
    """Panelists Aggregate Scores Graph Page"""
    database_connection.reconnect()
    agg_scores = aggregate_scores.retrieve_score_spread(database_connection)
    return render_template("panelists/aggregate-scores/graph.html",
                           aggregate_scores=agg_scores)

@app.route("/panelists/appearances-by-year")
def panelists_appearances_by_year_index():
    """Panelists Appearances by Year Index Page"""
    database_connection.reconnect()
    panelists = pnl_info.retrieve_all(database_connection)
    return render_template("panelists/appearances-by-year/index.html",
                           panelists=panelists)

@app.route("/panelists/appearances-by-year/<string:panelist>")
def panelists_appearances_by_year_details(panelist: Text):
    """Panelists Appearances by Year Graph Page"""
    database_connection.reconnect()
    panelist_slug = slugify(panelist)
    if panelist and panelist != panelist_slug:
        return redirect(url_for("panelists_appearances_by_year_details",
                                panelist=panelist_slug))

    info = pnl_info.retrieve_by_slug(panelist, database_connection)
    appearances = pnl_info.retrieve_yearly_appearances_by_slug(panelist,
                                                               database_connection)
    if not appearances:
        return redirect(url_for("panelists_appearances_by_year_index"))

    years = list(appearances.keys())
    count = list(appearances.values())

    return render_template("panelists/appearances-by-year/details.html",
                           info=info,
                           years=years,
                           count=count)

@app.route("/panelists/score-breakdown")
def panelists_score_breakdown_index():
    """Panelists Score Breakdown Index Page"""
    database_connection.reconnect()
    panelists = pnl_info.retrieve_all(database_connection)
    return render_template("panelists/score-breakdown/index.html",
                           panelists=panelists)

@app.route("/panelists/score-breakdown/<string:panelist>")
def panelists_score_breakdown_details(panelist: Text):
    """Panelists Score Breakdown Graph Page"""
    database_connection.reconnect()
    panelist_slug = slugify(panelist)
    if panelist and panelist != panelist_slug:
        return redirect(url_for("panelists_score_breakdown_details",
                                panelist=panelist_slug))

    info = pnl_info.retrieve_by_slug(panelist, database_connection)
    scores = pnl_info.retrieve_scores_grouped_list_by_slug(panelist,
                                                           database_connection)
    agg_scores = aggregate_scores.retrieve_score_spread(database_connection)
    if not info and not scores and not agg_scores:
        return redirect(url_for("panelists_score_breakdown_index"))

    return render_template("panelists/score-breakdown/details.html",
                           info=info,
                           scores=scores,
                           aggregate_scores=agg_scores)

@app.route("/panelists/scores-by-appearance")
def panelists_scores_by_appearance_index():
    """Panelists Scores by Appearance Index Page"""
    database_connection.reconnect()
    panelists = pnl_info.retrieve_all(database_connection)
    return render_template("panelists/scores-by-appearance/index.html",
                           panelists=panelists)

@app.route("/panelists/scores-by-appearance/<string:panelist>")
def panelists_scores_by_appearance_details(panelist: Text):
    """Panelists Scores by Appearance Graph Page"""
    database_connection.reconnect()
    panelist_slug = slugify(panelist)
    if panelist and panelist != panelist_slug:
        return redirect(url_for("panelists_scores_by_appearance_details",
                                panelist=panelist_slug))

    info = pnl_info.retrieve_by_slug(panelist, database_connection)
    scores = pnl_info.retrieve_scores_list_by_slug(panelist,
                                                   database_connection)

    if not info and not scores:
        return redirect(url_for("panelists_scores_by_appearance_index"))

    if scores:
        shows_json = json.dumps(scores["shows"])
        scores_json = json.dumps(scores["scores"])

        return render_template("panelists/scores-by-appearance/details.html",
                               info=info,
                               shows=shows_json,
                               scores=scores_json)

    return render_template("panelists/scores-by-appearance/details.html",
                           info=info,
                           shows=None,
                           scores=None)
#endregion

#region Show Routes
@app.route("/shows")
def shows_index():
    """Shows Index Page"""
    return render_template("shows/index.html")

@app.route("/shows/all-scores")
def shows_all_scores():
    """Shows All Scores Page"""
    database_connection.reconnect()
    show_years = retrieve_show_years()

    if not show_years:
        return redirect(url_for('shows_index'))

    return render_template("shows/all-scores/index.html",
                           show_years=show_years)

@app.route("/shows/all-scores/<int:year>")
def shows_all_scores_by_year(year: int):
    """Panelists All Scores Page"""
    database_connection.reconnect()
    show_years = retrieve_show_years()
    if year not in show_years:
        return redirect(url_for("shows_all_scores"))

    show_scores = show_info.retrieve_scores_by_year(year,
                                                    database_connection)
    if not show_scores:
        return render_template("shows/all-scores/details.html",
                               year=year, shows=None)

    shows = []
    scores_1 = []
    scores_2 = []
    scores_3 = []
    for show in show_scores:
        shows.append(show[0])
        scores_1.append(show[1])
        scores_2.append(show[2])
        scores_3.append(show[3])

    return render_template("shows/all-scores/details.html",
                           year=year,
                           shows=shows,
                           scores_1=scores_1,
                           scores_2=scores_2,
                           scores_3=scores_3)

@app.route("/shows/panel-gender-mix")
def shows_panel_gender_mix():
    """Show Panel Gender Mix Graph"""
    database_connection.reconnect()
    panel_mix = gender_mix.panel_gender_mix_breakdown(gender="female",
                                                      database_connection=database_connection)

    if not panel_mix:
        return redirect(url_for("shows_index"))

    years = []
    panel_0f = []
    panel_1f = []
    panel_2f = []
    panel_3f = []

    for year in panel_mix:
        years.append(year)
        panel_0f.append(panel_mix[year]["0F"])
        panel_1f.append(panel_mix[year]["1F"])
        panel_2f.append(panel_mix[year]["2F"])
        panel_3f.append(panel_mix[year]["3F"])

    return render_template("shows/panel-gender-mix/graph.html",
                           years=years,
                           panel_0f=panel_0f,
                           panel_1f=panel_1f,
                           panel_2f=panel_2f,
                           panel_3f=panel_3f)

#endregion

#region Application Initialization
config = load_config()
app_time_zone = config["settings"]["app_time_zone"]
time_zone_name = config["settings"]["time_zone"]
app.jinja_env.globals["app_version"] = APP_VERSION
app.jinja_env.globals["current_date"] = date.today()
app.jinja_env.globals["ga_property_code"] = config["settings"]["ga_property_code"]
app.jinja_env.globals["time_zone"] = app_time_zone
app.jinja_env.globals["rendered_at"] = utility.generate_date_time_stamp
app.jinja_env.globals["current_year"] = utility.current_year

app.jinja_env.globals["api_url"] = config["settings"]["api_url"]
app.jinja_env.globals["blog_url"] = config["settings"]["blog_url"]
app.jinja_env.globals["reports_url"] = config["settings"]["reports_url"]
app.jinja_env.globals["site_url"] = config["settings"]["site_url"]
app.jinja_env.globals["stats_url"] = config["settings"]["stats_url"]

database_connection = mysql.connector.connect(**config["database"])
database_connection.autocommit = True

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port="9257")

#endregion
