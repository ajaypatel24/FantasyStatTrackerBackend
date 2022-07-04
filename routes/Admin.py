from Model.variable import MatchupHistory, db
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import json
from Variables.TokenRefresh import lg, apiKey
from .FullData import test
from .WinningMatchup import winning, get_wins
from .RelevantData import get_last_week_roster
from HelperMethods.helper import getMatchups
from .Prediction import predict

Admin_Blueprint = Blueprint("Admin", __name__)


@Admin_Blueprint.route("/update-previous-week", methods=["GET"])  # winning
@cross_origin()
def update_roster_stats():
    headers = request.headers
    auth = headers.get("X-Api-Key")

    if auth == apiKey:

        previous_week = 23

        previous_week_data = test(previous_week).get_data()

        previous_winning_matchups = (
            winning(previous_week_data).get_data().decode("utf-8")
        )
        previous_leaders = get_wins(previous_week_data).get_data().decode("utf-8")
        previous_week_data = previous_week_data.decode("utf-8")
        previous_week_data = json.loads(previous_week_data)["TeamData"]

        matchup_record = MatchupHistory(
            matchup_week=previous_week,
            all_data=json.dumps(previous_week_data),
            winning_matchup=previous_winning_matchups,
            leader=previous_leaders,
        )
        db.session.add(matchup_record)
        db.session.commit()

        getMatchups()
        get_last_week_roster()

        predict()

    else:
        return jsonify({"message": "ERROR: unauthorized"}), 401

    return "Update Complete"
