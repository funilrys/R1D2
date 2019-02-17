"""
This is the flask application starting point.
"""

from os import getenv

import flask_shelve as shelve
from flask import Flask, g, jsonify, request
from flask_cors import cross_origin

from bot import RestaurantBot
from r1 import get_full_menu, serialize_menu
from r1.filter import filter_menu, make_filter
from r1.helpers import first_day_of_this_week

TELEGRAM_BOT_TOKEN = getenv("TELEGRAM_BOT_TOKEN")


def load_menu():
    """
    Get and return the full menu from the database.
    """

    database = shelve.get_shelve()
    first_day_of_the_week = first_day_of_this_week()
    current_day = database.get("day", None)

    if current_day is None or current_day != first_day_of_the_week:
        database["menu"] = get_full_menu()
        database["day"] = first_day_of_the_week

    return database["menu"]


def get_menu():
    """
    Get/set and return the full menu from the global data.
    """

    current_day = g.get("day", None)
    first_day_of_the_week = first_day_of_this_week()

    if current_day is None or current_day != first_day_of_the_week:
        g.menu = load_menu()
        g.day = current_day

    return g.menu


BOT = RestaurantBot(get_menu)
BOT.add_menu_action("r1", ["r1", "today"])
BOT.add_menu_action("r2", ["r2", "today"])
BOT.add_menu_action("r3", ["r3", "today"])
BOT.add_menu_action("today", ["today"])
BOT.add_menu_action("tomorrow", ["tomorrow"])
BOT.add_menu_action("vegetarian", ["vegetarian", "today"])

APP = Flask(__name__)
APP.debug = True
APP.config["SHELVE_FILENAME"] = "shelve.db"
shelve.init_app(APP)


@APP.route("/telegram/{}/".format(TELEGRAM_BOT_TOKEN), methods=["POST"])
def handle_telegram():
    resp = BOT.respond(request.json)
    if resp is None:
        return "OK"
    return jsonify(resp)


@APP.route("/<path:path>")
@cross_origin()
def json_menu(path):
    """
    Read the query string, get the menu and
    filter on top of the given query string

    :param path: The query string.
    :type path: str

    :return: The menu.
    :rtype: str|json
    """

    filter_ = make_filter(path.split("/"))
    menu = filter_menu(get_menu(), filter_)
    return jsonify(menu=serialize_menu(menu))


@APP.route("/")
def index():
    """
    Return the menu of the current day.
    """

    return json_menu("today")


if __name__ == "__main__":
    APP.run(debug=True)
