# Copyright (c) 2018-2025 Linh Pham
# graphs.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Shows Routes for Wait Wait Graphs Site."""

from flask import Blueprint, Response, current_app, render_template, url_for
from mysql.connector import connect
from wwdtm.show import Show

from app.reports.show import bluff_count, dates, gender_mix, scores, show_counts
from app.utility import month_names, redirect_url

blueprint = Blueprint("shows", __name__, template_folder="templates")


def retrieve_show_years(reverse_order: bool = True) -> list[int]:
    """Retrieve a list of available show years."""
    database_connection = connect(**current_app.config["database"])
    show = Show(database_connection=database_connection)
    years = show.retrieve_years()
    database_connection.close()

    if years and reverse_order:
        years.reverse()

    return years


@blueprint.route("/")
def index() -> str:
    """View: Shows Index."""
    return render_template("shows/index.html")


@blueprint.route("/all-scores")
def all_scores() -> Response | str:
    """View: All Scores."""
    show_years = retrieve_show_years()

    if not show_years:
        return redirect_url(url_for("shows_index"))

    return render_template("shows/all-scores/index.html", show_years=show_years)


@blueprint.route("/all-scores/<int:year>")
def all_scores_by_year(year: int) -> Response | str:
    """View: All Scores by Year."""
    show_years = retrieve_show_years()
    if year not in show_years:
        return redirect_url(url_for("shows_all_scores"))

    database_connection = connect(**current_app.config["database"])
    _show = Show(database_connection=database_connection)
    _all_scores = _show.retrieve_scores_by_year(
        year,
        use_decimal_scores=current_app.config["app_settings"]["use_decimal_scores"],
    )
    database_connection.close()

    if not _all_scores:
        return render_template("shows/all-scores/details.html", year=year, shows=None)

    shows = []
    scores_1 = []
    scores_2 = []
    scores_3 = []
    for show in _all_scores:
        shows.append(show[0])
        if current_app.config["app_settings"]["use_decimal_scores"]:
            scores_1.append(float(show[1]))
            scores_2.append(float(show[2]))
            scores_3.append(float(show[3]))
        else:
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
def bluff_counts() -> Response | str:
    """View: Bluff the Listener Counts."""
    show_years = retrieve_show_years()
    if not show_years:
        return redirect_url(url_for("shows.index"))

    return render_template("shows/bluff-counts/index.html", show_years=show_years)


@blueprint.route("/bluff-counts/all")
def bluff_counts_all() -> Response | str:
    """View: All Bluff the Listener Counts."""
    bluff_data = bluff_count.retrieve_all_bluff_counts()

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
def bluff_counts_by_year(year: int) -> Response | str:
    """View: Bluff the Listener Counts by Year."""
    show_years = retrieve_show_years()
    if year not in show_years:
        return redirect_url(url_for("shows.bluff_counts"))

    bluff_data = bluff_count.retrieve_bluff_count_year(year=year)

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
def counts_by_day_of_month() -> str:
    """View: Counts by Day of Month."""
    return render_template("shows/counts-by-day-month/index.html", months=month_names)


@blueprint.route("/counts-by-day-month/all")
def counts_by_day_of_month_all() -> Response | str:
    """View: All Counts by Day of Month."""
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
def counts_by_day_of_month_by_month(month: int) -> Response | str:
    """View: Counts by Day of Month by Month."""
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
def counts_by_year() -> Response | str:
    """View: Show Counts by Year."""
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
def monthly_aggregate_score_heatmap() -> str:
    """View: Monthly Aggregate Score Heatmap."""
    _all_scores = scores.retrieve_monthly_aggregate_scores(
        use_decimal_scores=current_app.config["app_settings"]["use_decimal_scores"]
    )

    if not _all_scores:
        return render_template(
            "shows/monthly-aggregate-score-heatmap/graph.html", years=None, scores=None
        )

    scores_list = []
    years = list(_all_scores.keys())
    for year in _all_scores:
        scores_list.append(list(_all_scores[year].values()))

    return render_template(
        "shows/monthly-aggregate-score-heatmap/graph.html",
        years=years,
        scores=scores_list,
    )


@blueprint.route("/monthly-average-score-heatmap")
def monthly_average_score_heatmap() -> str:
    """View: Monthly Average Score Heatmap."""
    _all_scores = scores.retrieve_monthly_average_scores(
        use_decimal_scores=current_app.config["app_settings"]["use_decimal_scores"]
    )

    if not _all_scores:
        return render_template(
            "shows/monthly-average-score-heatmap/graph.html", years=None, scores=None
        )

    scores_list = []
    years = list(_all_scores.keys())
    for year in _all_scores:
        scores_list.append(list(_all_scores[year].values()))

    return render_template(
        "shows/monthly-average-score-heatmap/graph.html",
        years=years,
        scores=scores_list,
    )


@blueprint.route("/panel-gender-mix")
def panel_gender_mix() -> Response | str:
    """View: Panel Gender Mix."""
    panel_mix = gender_mix.panel_gender_mix_breakdown(gender="female")

    if not panel_mix:
        return redirect_url(url_for("shows_index"))

    years = []
    panel_0f = []
    panel_1f = []
    panel_2f = []
    panel_3f = []

    # pylint: disable=C0206
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
