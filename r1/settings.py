from .types import DishType, Restaurant

BASE = "https://www.novae-restauration.ch/menus/"
URL = BASE + "menu-week/cern/{restaurant_id}?display=columns"
PARAMS = {
    Restaurant.r1: {
        "restaurant_id": "13",
        "pages": 3,
        "page_structure": (8, 2),
        "dishes": (
            DishType.menu1,
            DishType.menu2,
            DishType.pasta_di_guiseppe,
            DishType.pasta,
            DishType.pizza,
            DishType.speciality,
            DishType.grill,
            DishType.vegetarian,
            DishType.hamburger,
        ),
        "currency": "CHF",
    },
    Restaurant.r2: {
        "restaurant_id": "21",
        "pages": 2,
        "page_structure": (11, 1),
        "dishes": (
            DishType.marche,
            DishType.season,
            DishType.vegetarian,
            DishType.pasta_of_the_day,
            DishType.pasta_of_the_day2,
            DishType.speciality,
            DishType.grill,
            DishType.grill1,
            DishType.grill2,
            DishType.pizza_of_the_day,
            DishType.pizza,
        ),
        "currency": "CHF",
    },
    Restaurant.r3: {
        "restaurant_id": "33",
        "pages": 2,
        "page_structure": (7, 1),
        "dishes": (
            DishType.vegetarian_marche,
            DishType.season,
            DishType.atelier,
            DishType.speciality,
            DishType.grill,
            DishType.pizza_of_the_day,
            DishType.pizza,
        ),
        "currency": "€",
    },
}
