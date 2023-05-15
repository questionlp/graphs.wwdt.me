# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2023 Linh Pham
# graphs.wwdt.me is released under the terms of the Apache License 2.0
"""Panelists Routes for Wait Wait Graphs Site"""
import json

from flask import Blueprint, current_app, render_template, url_for
import mysql.connector
from slugify import slugify

from wwdtm.panelist import (
    Panelist,
    PanelistAppearances,
    PanelistScores,
)

from wwdtm.show import Show

from app.reports.panel import aggregate_scores as agg
from app.reports.panel import average_scores as avg
from app.utility import redirect_url

blueprint = Blueprint("panelists", __name__, template_folder="templates")


@blueprint.route("/")
def index():
    """View: Panelists Index"""
    return render_template("panelists/index.html")


@blueprint.route("/aggregate-scores")
def aggregate_scores():
    """View: Aggregate Scores"""
    _aggregate_scores = agg.retrieve_score_spread()
    return render_template(
        "panelists/aggregate-scores/graph.html", aggregate_scores=_aggregate_scores
    )


@blueprint.route("/appearances-by-year")
def appearances_by_year():
    """View: Appearances by Year"""
    database_connection = mysql.connector.connect(**current_app.config["database"])
    _panelist = Panelist(database_connection=database_connection)
    all_panelists = _panelist.retrieve_all()
    database_connection.close()
    return render_template(
        "panelists/appearances-by-year/index.html", panelists=all_panelists
    )


@blueprint.route("/appearances-by-year/<string:panelist>")
def appearances_by_year_details(panelist: str):
    """View: Appearances by Year Details"""
    panelist_slug = slugify(panelist)
    if panelist and panelist != panelist_slug:
        return redirect_url(
            url_for("panelists.appearances_by_year_details", panelist=panelist_slug)
        )

    database_connection = mysql.connector.connect(**current_app.config["database"])
    _panelist = Panelist(database_connection=database_connection)
    _appearances = PanelistAppearances(database_connection=database_connection)
    info = _panelist.retrieve_by_slug(panelist)

    if not info:
        return redirect_url(url_for("panelists.appearances_by_year"))

    appearances = _appearances.retrieve_yearly_appearances_by_slug(panelist)
    database_connection.close()

    years = list(appearances.keys())
    count = list(appearances.values())

    return render_template(
        "panelists/appearances-by-year/details.html",
        info=info,
        years=years,
        count=count,
    )


@blueprint.route("/average-scores-by-year")
def average_scores_by_year():
    """View: Average Scores by Year"""
    database_connection = mysql.connector.connect(**current_app.config["database"])
    average_scores = avg.retrieve_panelist_yearly_average()
    _show = Show(database_connection=database_connection)
    years = _show.retrieve_years()
    if average_scores and years:
        panelists = [scores["name"] for scores in average_scores]
        panelists.reverse()
        averages = [list(scores["averages"].values()) for scores in average_scores]
        averages.reverse()
        return render_template(
            "panelists/average-scores-by-year/graph.html",
            averages=averages,
            panelists=panelists,
            years=years,
        )
    else:
        return render_template("panelists/templates/average-scores-by-year/graph.html")


@blueprint.route("/score-breakdown")
def score_breakdown():
    """View: Score Breakdown"""
    database_connection = mysql.connector.connect(**current_app.config["database"])
    _panelist = Panelist(database_connection=database_connection)
    panelists = _panelist.retrieve_all()
    database_connection.close()
    return render_template("panelists/score-breakdown/index.html", panelists=panelists)


@blueprint.route("/score-breakdown/<string:panelist>")
def score_breakdown_details(panelist: str):
    """View: Score Breakdown Details"""
    panelist_slug = slugify(panelist)
    if panelist and panelist != panelist_slug:
        return redirect_url(
            url_for("panelists.score_breakdown_details", panelist=panelist_slug)
        )

    database_connection = mysql.connector.connect(**current_app.config["database"])
    _panelist = Panelist(database_connection=database_connection)
    info = _panelist.retrieve_by_slug(panelist)

    if not info:
        return redirect_url(url_for("panelists.score_breakdown"))

    _panelist_scores = PanelistScores(database_connection=database_connection)
    scores = _panelist_scores.retrieve_scores_grouped_list_by_slug(panelist)
    agg_scores = agg.retrieve_score_spread()
    database_connection.close()

    return render_template(
        "panelists/score-breakdown/details.html",
        info=info,
        scores=scores,
        aggregate_scores=agg_scores,
    )


@blueprint.route("/scores-by-appearance")
def scores_by_appearance():
    """View: Scores by Appearances"""
    database_connection = mysql.connector.connect(**current_app.config["database"])
    _panelist = Panelist(database_connection=database_connection)
    panelists = _panelist.retrieve_all()
    database_connection.close()
    return render_template(
        "panelists/scores-by-appearance/index.html", panelists=panelists
    )


@blueprint.route("/scores-by-appearance/<string:panelist>")
def scores_by_appearance_details(panelist: str):
    """View: Scores by Appearances"""
    panelist_slug = slugify(panelist)
    if panelist and panelist != panelist_slug:
        return redirect_url(
            url_for("panelists.scores_by_appearance_details", panelist=panelist_slug)
        )

    database_connection = mysql.connector.connect(**current_app.config["database"])
    _panelist = Panelist(database_connection=database_connection)
    _panelist_scores = PanelistScores(database_connection=database_connection)
    info = _panelist.retrieve_by_slug(panelist)
    scores = _panelist_scores.retrieve_scores_list_by_slug(panelist)
    database_connection.close()

    if not info:
        return redirect_url(url_for("panelists.scores_by_appearance"))

    if scores:
        shows_json = json.dumps(scores["shows"])
        scores_json = json.dumps(scores["scores"])

        return render_template(
            "panelists/scores-by-appearance/details.html",
            info=info,
            shows=shows_json,
            scores=scores_json,
        )

    return render_template(
        "panelists/scores-by-appearance/details.html",
        info=info,
        shows=None,
        scores=None,
    )
