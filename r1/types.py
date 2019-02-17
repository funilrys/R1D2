"""
Types provider.
"""

from collections import namedtuple
from enum import Enum
from functools import partial


def valid_string_for_enum(enum, s):
    return s in enum.__members__


def enum_from_string(enum, s):
    return enum.__members__[s]


Restaurant = Enum("Restaurant", ["r1", "r2", "r3"])
valid_string_for_restaurant = partial(valid_string_for_enum, Restaurant)
restaurant_from_string = partial(enum_from_string, Restaurant)


DishType = Enum(
    "DishType",
    [
        "atelier",
        "grill",
        "grill1",
        "grill2",
        "grill3",
        "hamburger",
        "marche",
        "menu1",
        "menu2",
        "menu3",
        "pasta_di_guiseppe",
        "pasta_of_the_day",
        "pasta_of_the_day2",
        "pasta",
        "pizza_of_the_day",
        "pizza",
        "pizza2",
        "saison",
        "season",
        "speciality",
        "vegetarian_marche",
        "vegetarian",
    ],
)
valid_string_for_dishtype = partial(valid_string_for_enum, DishType)
dishtype_from_string = partial(enum_from_string, DishType)


MenuItem = namedtuple(
    "MenuItem", ["restaurant", "date", "type", "name", "price", "currency"]
)
