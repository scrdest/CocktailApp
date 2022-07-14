import json
import os
import functools
import httpx

from cocktailapp import constants


def get_api_key() -> str:
    api_key = (
        os.environ.get(constants.ENV_API_KEY)
        or constants.VAL_DEFAULT_API_KEY
    )
    return api_key


@functools.lru_cache(maxsize=2)
def get_root_query_url(api_key: str = None) -> str:
    _true_api_key = api_key or get_api_key()

    full_base_url = "/".join((
        constants.VAL_COCKTAILAPI_BASE_URL,
        constants.VAL_COCKTAILAPI_URL_API_SUFFIX,
        _true_api_key
    ))

    return full_base_url


@functools.lru_cache(maxsize=2)
def get_base_ingredient_search_query_url(api_key: str = None) -> str:
    _true_api_key = api_key or get_api_key()

    full_base_url = get_root_query_url(_true_api_key)

    base_search_url = "/".join((
        full_base_url,
        "filter.php",
    ))

    return base_search_url


@functools.lru_cache(maxsize=2)
def get_base_cocktail_search_query_url(api_key: str = None) -> str:
    _true_api_key = api_key or get_api_key()

    full_base_url = get_root_query_url(_true_api_key)

    base_search_url = "/".join((
        full_base_url,
        "lookup.php",
    ))

    return base_search_url


def build_query_for_ingredient(ingredient: str):
    base_search_url = get_base_ingredient_search_query_url()
    full_search_url = f"{base_search_url}?i={ingredient}"
    return full_search_url


def build_query_for_cocktail(cocktail_id: str):
    base_search_url = get_base_cocktail_search_query_url()
    full_search_url = f"{base_search_url}?i={cocktail_id}"
    return full_search_url


@functools.lru_cache(maxsize=1000)
def lookup_cocktail_ingredients(cocktail_id: str):
    query_endpoint = build_query_for_cocktail(cocktail_id=cocktail_id)
    raw_response = httpx.get(query_endpoint)
    raw_response.raise_for_status()

    cocktail_json = raw_response.json()
    cocktails_as_list = cocktail_json.get(constants.KEY_APIRESPONSE_DRINKS) or []

    ingredients = set()

    for drink_data in cocktails_as_list:

        for (detail_key, detail_value) in drink_data.items():

            if not detail_key.startswith("strIngredient"):
                continue

            if not detail_value:
                continue

            ingredients.add(detail_value.lower())

    return ingredients


def cocktails_for_ingredient(ingredient):
    query_endpoint = build_query_for_ingredient(ingredient=ingredient)
    raw_response = httpx.get(query_endpoint)
    raw_response.raise_for_status()
    drinks_json = {}

    try:
        drinks_json = raw_response.json()
    except json.JSONDecodeError as json_err:
        print(json_err, raw_response.text)

    drinks_as_list = drinks_json.get(constants.KEY_APIRESPONSE_DRINKS) or []
    drinks_map = {}

    for drink in drinks_as_list:
        drink_id = drink.get(constants.KEY_APIRESPONSE_DRINK_ID)
        drink_name = drink.get(constants.KEY_APIRESPONSE_DRINK_NAME)

        if not drink_id:
            continue

        drink_details = lookup_cocktail_ingredients(drink_id)
        drinks_map[drink_id] = (drink_name, drink_details)

    return drinks_map


if __name__ == '__main__':
    cocktails_for_ingredient("vodka")
