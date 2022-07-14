import sys

from cocktailapp import constants
from cocktailapp.interface import cli
from cocktailapp.lookup import query, ingredient_match


def execute(**app_args):
    available_ingredients = tuple(app_args[constants.ARG_INGREDIENTS])
    print(f"Matching ingredients: {available_ingredients}...")
    cocktails = set()

    for ingredient in available_ingredients:
        ingr_matching_cocktails: dict = query.cocktails_for_ingredient(ingredient=ingredient)

        for (cocktail_name, cocktail_ingrs) in ingr_matching_cocktails.values():
            if ingredient_match.check_ingredient_match(available_ingredients, tuple(cocktail_ingrs)):
                cocktails.add(cocktail_name)

    for cocktail in cocktails:
        print(cocktail)

    cocktails_as_list = list(cocktails)
    return cocktails_as_list


def start():
    app_args: dict = cli.parse_args()
    result = execute(**app_args)
    sys.exit(result)


if __name__ == '__main__':
    start()
