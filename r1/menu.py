"""
Menu provider.
"""

import itertools as it
import re
from datetime import timedelta

import bs4
import requests

from .helpers import first_day_of_this_week, grouper
from .settings import PARAMS, URL
from .types import MenuItem, Restaurant


def get_url(restaurant):
    """
    Construct the URL to call.
    """

    params = PARAMS[restaurant]
    return URL.format(**params)


def extract_name(bsitem):
    """
    Extract the menu item.
    """

    return bsitem.find("span").text


def extract_price(bsitem):
    """
    Extract the price of the price of the menu item.
    """

    reg = re.compile(r"(\d+\.?\d*)")
    mat = reg.findall(bsitem.text)
    if mat:
        return float(mat[0])
    return 0.0


def extract_table(response):
    """
    Interpret the table from the upstream table.
    """
    soup = bs4.BeautifulSoup(response.text, "lxml")
    the_main_table = soup.find("table", class_="menuRestaurant")
    menus_content = the_main_table.findAll("table", class_="HauteurMenu")

    return [(extract_name(i), extract_price(i)) for i in menus_content[1::2]]


def fetch_menu(restaurant):
    """
    Fetch all menus of the given restaurant.
    """

    url = get_url(restaurant)
    req_session = requests.Session()
    return [extract_table(req_session.get(url))]


def split_days(items, structure):
    xs = [grouper(i, n) for i, n in zip(items, structure)]
    return [list(it.chain(*i)) for i in zip(*xs)]


def get_menu(restaurant):
    """
    Provide the complete menu of the given restaurant (for the current week=.
    """

    params = PARAMS[restaurant]
    items = split_days(fetch_menu(restaurant), params["page_structure"])
    day_structure = params["dishes"]
    first_day = first_day_of_this_week()
    menu = []

    for d, ms in enumerate(items):
        day = first_day + timedelta(days=d)
        while None in ms:
            ms.remove(None)

        for (name, price), t in zip(ms, day_structure):
            menu.append(MenuItem(restaurant, day, t, name, price, params["currency"]))
    return menu


def get_full_menu():
    """
    Return the menu of all restaurants.
    """

    return get_menu(Restaurant.r1) + get_menu(Restaurant.r2) + get_menu(Restaurant.r3)
