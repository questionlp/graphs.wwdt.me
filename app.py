# -*- coding: utf-8 -*-
# Copyright (c) 2018-2023 Linh Pham
# graphs.wwdt.me is released under the terms of the Apache License 2.0
"""Flask application startup file"""

from datetime import date
import json
from typing import Dict, List
import traceback

from flask import Flask, redirect, render_template, Response, url_for
from flask.logging import create_logger
import mysql.connector
import pytz
from slugify import slugify
from werkzeug.exceptions import HTTPException

from wwdtm import VERSION as WWDTM_VERSION
from wwdtm.panelist import info as pnl_info
from wwdtm.show import info as show_info
from graphs import utility
from reports.panel import aggregate_scores, gender_mix
from reports.show import (bluff_count as bluff,
                          dates,
                          scores as show_scores,
                          show_counts)

#region Global Constants
APP_VERSION = "1.16.0"

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
def load_config() -> Dict:
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
def retrieve_show_years(reverse_order: bool = True) -> List[int]:
    """Retrieve a list of available show years"""
    database_connection.reconnect()
    years = show_info.retrieve_years(database_connection)
    if years and reverse_order:
        years.reverse()

    return years

#endregion

#region Filters
@app.template_filter("pretty_jsonify")
def pretty_jsonify(data) -> str:
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

@app.errorhandler(404)
def not_found(error):
    """Handle resource not found conditions"""
    return render_template("errors/404.html",
                           error_description=error.description), 404

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
                              months=utility.month_names.keys(),
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
def panelists_appearances_by_year_details(panelist: str):
    """Panelists Appearances by Year Graph Page"""
    database_connection.reconnect()
    panelist_slug = slugify(panelist)
    if panelist and panelist != panelist_slug:
        return redirect(url_for("panelists_appearances_by_year_details",
                                panelist=panelist_slug))

    info = pnl_info.retrieve_by_slug(panelist, database_connection)
    appearances = pnl_info.retrieve_yearly_appearances_by_slug(panelist,
                                                               database_connection)
    if not info:
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
def panelists_score_breakdown_details(panelist: str):
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
    if not info:
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
def panelists_scores_by_appearance_details(panelist: str):
    """Panelists Scores by Appearance Graph Page"""
    database_connection.reconnect()
    panelist_slug = slugify(panelist)
    if panelist and panelist != panelist_slug:
        return redirect(url_for("panelists_scores_by_appearance_details",
                                panelist=panelist_slug))

    info = pnl_info.retrieve_by_slug(panelist, database_connection)
    scores = pnl_info.retrieve_scores_list_by_slug(panelist,
                                                   database_connection)

    if not info:
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

    all_scores = show_info.retrieve_scores_by_year(year,
                                                   database_connection)
    if not all_scores:
        return render_template("shows/all-scores/details.html",
                               year=year, shows=None)

    shows = []
    scores_1 = []
    scores_2 = []
    scores_3 = []
    for show in all_scores:
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

@app.route("/shows/bluff-counts")
def shows_bluff_counts():
    """Show Bluff the Listener Counts Graph"""
    database_connection.reconnect()
    show_years = retrieve_show_years()
    if not show_years:
        return redirect(url_for('shows_index'))

    return render_template("shows/bluff-counts/index.html",
                           show_years=show_years)

@app.route("/shows/bluff-counts/all")
def shows_bluff_counts_all():
    """Show Bluff the Listener Counts by Month Line Graph for all
    years"""
    database_connection.reconnect()
    bluff_data = bluff.retrieve_all_bluff_counts(database_connection)

    if not bluff_data:
        return redirect(url_for("shows_bluff_counts"))

    dates = list(bluff_data.keys())
    correct = []
    incorrect = []
    for month_year in dates:
        correct.append(bluff_data[month_year]["correct"])
        incorrect.append(bluff_data[month_year]["incorrect"])

    return render_template("shows/bluff-counts/all.html",
                           dates=dates,
                           correct=correct,
                           incorrect=incorrect)

@app.route("/shows/bluff-counts/<int:year>")
def shows_bluff_counts_by_year(year: int):
    """Show Bluff the Listener Counts by Month Bar Graph for the
    requested year"""
    database_connection.reconnect()
    show_years = retrieve_show_years()
    if year not in show_years:
        return redirect(url_for("shows_bluff_counts"))

    bluff_data = bluff.retrieve_bluff_count_year(year=year,
                                                 database_connection=database_connection)

    if not bluff_data:
        return render_template("shows/bluff-counts/details.html",
                               year=year,
                               months=None,
                               correct=None,
                               incorrect=None)

    months = list(bluff_data.keys())
    correct = []
    incorrect = []
    for month in bluff_data:
        correct.append(bluff_data[month]["correct"])
        incorrect.append(bluff_data[month]["incorrect"])

    return render_template("shows/bluff-counts/details.html",
                           year=year,
                           months=months,
                           correct=correct,
                           incorrect=incorrect)

@app.route("/shows/counts-by-day-month")
def shows_counts_by_day_of_month_index():
    """Counts by Day of Month Graph Index Page"""
    database_connection.reconnect()
    return render_template("shows/counts-by-day-month/index.html",
                           months=utility.month_names)

@app.route("/shows/counts-by-day-month/<int:month>")
def shows_counts_by_day_of_month(month: int):
    """Counts by Day of Month Graph"""
    database_connection.reconnect()

    # Validate that the month number is valid
    if not month in range(1, 13):
        return redirect(url_for("shows_counts_by_day_of_month_index"))

    shows_month = dates.retrieve_show_counts_by_month_day(month,
                                                          database_connection)

    if not shows_month:
        return redirect(url_for("shows_counts_by_day_of_month_index"))

    days = []
    regular_shows = []
    best_of_shows = []
    repeat_shows = []
    repeat_best_of_shows = []
    for day, value in shows_month.items():
        days.append(day)
        regular_shows.append(value["regular"])
        best_of_shows.append(value["best_of"])
        repeat_shows.append(value["repeat"])
        repeat_best_of_shows.append(value["best_of_repeat"])

    return render_template("shows/counts-by-day-month/details.html",
                           month=utility.month_names[month],
                           days=days,
                           regular_shows=regular_shows,
                           best_of_shows=best_of_shows,
                           repeat_shows=repeat_shows,
                           repeat_best_of_shows=repeat_best_of_shows)

@app.route("/shows/counts-by-day-month/all")
def shows_counts_by_day_of_month_all():
    """Counts by Day of Month for all Months Graph"""
    database_connection.reconnect()

    days_info = dates.retrieve_show_counts_by_month_day_all(database_connection)

    if not days_info:
        return redirect(url_for("shows_counts_by_day_of_month_index"))

    days = []
    regular_shows = []
    best_of_shows = []
    repeat_shows = []
    repeat_best_of_shows = []
    for day, value in days_info.items():
        days.append(day)
        regular_shows.append(value["regular"])
        best_of_shows.append(value["best_of"])
        repeat_shows.append(value["repeat"])
        repeat_best_of_shows.append(value["best_of_repeat"])

    return render_template("shows/counts-by-day-month/all.html",
                           days=days,
                           regular_shows=regular_shows,
                           best_of_shows=best_of_shows,
                           repeat_shows=repeat_shows,
                           repeat_best_of_shows=repeat_best_of_shows)

@app.route("/shows/monthly-aggregate-score-heatmap")
def shows_monthly_aggregate_score_heatmap():
    """Monthly Aggregate Score Heatmap Graph"""
    database_connection.reconnect()
    all_scores = show_scores.retrieve_monthly_aggregate_scores(database_connection)

    if not all_scores:
        return render_template("shows/monthly-aggregate-score-heatmap/graph.html",
                               years=None,
                               scores=None)

    scores_list = []
    years = list(all_scores.keys())
    for year in all_scores:
        scores_list.append(list(all_scores[year].values()))

    return render_template("shows/monthly-aggregate-score-heatmap/graph.html",
                           years=years,
                           scores=scores_list)

@app.route("/shows/monthly-average-score-heatmap")
def shows_monthly_average_score_heatmap():
    """Monthly Average Score Heatmap Graph"""

    database_connection.reconnect()
    all_scores = show_scores.retrieve_monthly_average_scores(database_connection)

    if not all_scores:
        return render_template("shows/monthly-average-score-heatmap/graph.html",
                               years=None,
                               scores=None)

    scores_list = []
    years = list(all_scores.keys())
    for year in all_scores:
        scores_list.append(list(all_scores[year].values()))

    return render_template("shows/monthly-average-score-heatmap/graph.html",
                           years=years,
                           scores=scores_list)

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

@app.route("/shows/show-counts-by-year")
def shows_counts_by_year():
    """Show Counts by Year Graph"""
    database_connection.reconnect()
    counts = show_counts.retrieve_show_counts_by_year(database_connection=database_connection)

    if not counts:
        return redirect(url_for("shows_index"))

    years = []
    regular = []
    best_ofs = []
    repeats = []
    repeat_best_ofs = []

    for year in counts:
        years.append(year)
        regular.append(counts[year]["regular"])
        best_ofs.append(counts[year]["best_of"])
        repeats.append(counts[year]["repeat"])
        repeat_best_ofs.append(counts[year]["repeat_best_of"])

    return render_template("shows/counts-by-year/graph.html",
                           years=years,
                           regular=regular,
                           best_ofs=best_ofs,
                           repeats=repeats,
                           repeat_best_ofs=repeat_best_ofs)

#endregion

#region Application Initialization
config = load_config()
app_time_zone = config["settings"]["app_time_zone"]
time_zone_name = config["settings"]["time_zone"]
app.jinja_env.globals["app_version"] = APP_VERSION
app.jinja_env.globals["libwwdtm_version"] = WWDTM_VERSION
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
app.jinja_env.globals["repo_url"] = config["settings"]["repo_url"]

database_connection = mysql.connector.connect(**config["database"])
database_connection.autocommit = True

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port="9257")

#endregion
