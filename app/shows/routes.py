# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2023 Linh Pham
# graphs.wwdt.me is released under the terms of the Apache License 2.0
"""Shows Routes for Wait Wait Graphs Site"""
from flask import Blueprint, current_app, render_template, url_for
import mysql.connector
from wwdtm.show import Show

from app.reports.show import (
    bluff_count as bluff,
    dates,
    gender_mix,
    scores as show_scores,
    show_counts,
)
from app.utility import redirect_url, month_names

blueprint = Blueprint("shows", __name__, template_folder="templates")


def retrieve_show_years(reverse_order: bool = True):
    """Retrieve a list of available show years"""
    database_connection = mysql.connector.connect(**current_app.config["database"])
    show = Show(database_connection=database_connection)
    years = show.retrieve_years()
    database_connection.close()

    if years and reverse_order:
        years.reverse()

    return years


@blueprint.route("/")
def index():
    """View: Shows Index"""
    return render_template("shows/index.html")


@blueprint.route("/all-scores")
def all_scores():
    """View: All Scores"""
    show_years = retrieve_show_years()

    if not show_years:
        return redirect_url(url_for("shows_index"))

    return render_template("shows/all-scores/index.html", show_years=show_years)


@blueprint.route("/all-scores/<int:year>")
def all_scores_by_year(year: int):
    """View: All Scores by Year"""
    show_years = retrieve_show_years()
    if year not in show_years:
        return redirect_url(url_for("shows_all_scores"))

    database_connection = mysql.connector.connect(**current_app.config["database"])
    show = Show(database_connection=database_connection)
    all_scores = show.retrieve_scores_by_year(year)
    database_connection.close()

    if not all_scores:
        return render_template("shows/all-scores/details.html", year=year, shows=None)

    shows = []
    scores_1 = []
    scores_2 = []
    scores_3 = []
    for show in all_scores:
        shows.append(show[0])
        scores_1.append(show[1])
        scores_2.append(show[2])
        scores_3.append(show[3])

    return render_template(
        "shows/all-scores/details.html",
        year=year,
        shows=shows,
        scores_1=scores_1,
        scores_2=scores_2,
        scores_3=scores_3,
    )


@blueprint.route("/bluff-counts")
def bluff_counts():
    """View: Bluff the Listener Counts"""
    show_years = retrieve_show_years()
    if not show_years:
        return redirect_url(url_for("shows.index"))

    return render_template("shows/bluff-counts/index.html", show_years=show_years)


@blueprint.route("/bluff-counts/all")
def bluff_counts_all():
    """View: All Bluff the Listener Counts"""
    bluff_data = bluff.retrieve_all_bluff_counts()

    if not bluff_data:
        return redirect_url(url_for("shows_bluff_counts"))

    _dates = list(bluff_data.keys())
    correct = []
    incorrect = []
    for month_year in _dates:
        correct.append(bluff_data[month_year]["correct"])
        incorrect.append(bluff_data[month_year]["incorrect"])

    return render_template(
        "shows/bluff-counts/all.html",
        dates=_dates,
        correct=correct,
        incorrect=incorrect,
    )


@blueprint.route("/bluff-counts/<int:year>")
def bluff_counts_by_year(year: int):
    """View: Bluff the Listener Counts by Year"""
    show_years = retrieve_show_years()
    if year not in show_years:
        return redirect_url(url_for("shows_bluff_counts"))

    bluff_data = bluff.retrieve_bluff_count_year(year=year)

    if not bluff_data:
        return render_template(
            "shows/bluff-counts/details.html",
            year=year,
            months=None,
            correct=None,
            incorrect=None,
        )

    months = list(bluff_data.keys())
    correct = []
    incorrect = []
    for month in bluff_data:
        correct.append(bluff_data[month]["correct"])
        incorrect.append(bluff_data[month]["incorrect"])

    return render_template(
        "shows/bluff-counts/details.html",
        year=year,
        months=months,
        correct=correct,
        incorrect=incorrect,
    )


@blueprint.route("/counts-by-day-month")
def counts_by_day_of_month():
    """View: Counts by Day of Month"""
    return render_template("shows/counts-by-day-month/index.html", months=month_names)


@blueprint.route("/counts-by-day-month/all")
def counts_by_day_of_month_all():
    """View: All Counts by Day of Month"""
    days_info = dates.retrieve_show_counts_by_month_day_all()

    if not days_info:
        return redirect_url(url_for("shows.counts_by_day_of_month"))

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

    return render_template(
        "shows/counts-by-day-month/all.html",
        days=days,
        regular_shows=regular_shows,
        best_of_shows=best_of_shows,
        repeat_shows=repeat_shows,
        repeat_best_of_shows=repeat_best_of_shows,
    )


@blueprint.route("/counts-by-day-month/<int:month>")
def counts_by_day_of_month_by_month(month: int):
    """View: Counts by Day of Month by Month"""
    # Validate that the month number is valid
    if month not in range(1, 13):
        return redirect_url(url_for("shows.counts_by_day_of_month"))

    shows_month = dates.retrieve_show_counts_by_month_day(month)

    if not shows_month:
        return redirect_url(url_for("shows.counts_by_day_of_month"))

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

    return render_template(
        "shows/counts-by-day-month/details.html",
        month=month_names[month],
        days=days,
        regular_shows=regular_shows,
        best_of_shows=best_of_shows,
        repeat_shows=repeat_shows,
        repeat_best_of_shows=repeat_best_of_shows,
    )


@blueprint.route("/counts-by-year")
def counts_by_year():
    """View: Show Counts by Year"""
    counts = show_counts.retrieve_show_counts_by_year()

    if not counts:
        return redirect_url(url_for("shows_index"))

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

    return render_template(
        "shows/counts-by-year/graph.html",
        years=years,
        regular=regular,
        best_ofs=best_ofs,
        repeats=repeats,
        repeat_best_ofs=repeat_best_ofs,
    )


@blueprint.route("/monthly-aggregate-score-heatmap")
def monthly_aggregate_score_heatmap():
    """View: Monthly Aggregate Score Heatmap"""
    all_scores = show_scores.retrieve_monthly_aggregate_scores()

    if not all_scores:
        return render_template(
            "shows/monthly-aggregate-score-heatmap/graph.html", years=None, scores=None
        )

    scores_list = []
    years = list(all_scores.keys())
    for year in all_scores:
        scores_list.append(list(all_scores[year].values()))

    return render_template(
        "shows/monthly-aggregate-score-heatmap/graph.html",
        years=years,
        scores=scores_list,
    )


@blueprint.route("/monthly-average-score-heatmap")
def monthly_average_score_heatmap():
    """View: Monthly Average Score Heatmap"""
    all_scores = show_scores.retrieve_monthly_average_scores()

    if not all_scores:
        return render_template(
            "shows/monthly-average-score-heatmap/graph.html", years=None, scores=None
        )

    scores_list = []
    years = list(all_scores.keys())
    for year in all_scores:
        scores_list.append(list(all_scores[year].values()))

    return render_template(
        "shows/monthly-average-score-heatmap/graph.html",
        years=years,
        scores=scores_list,
    )


@blueprint.route("/panel-gender-mix")
def panel_gender_mix():
    """View: Panel Gender Mix"""
    panel_mix = gender_mix.panel_gender_mix_breakdown(gender="female")

    if not panel_mix:
        return redirect_url(url_for("shows_index"))

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

    return render_template(
        "shows/panel-gender-mix/graph.html",
        years=years,
        panel_0f=panel_0f,
        panel_1f=panel_1f,
        panel_2f=panel_2f,
        panel_3f=panel_3f,
    )
