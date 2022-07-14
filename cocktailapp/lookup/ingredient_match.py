import functools


@functools.lru_cache(maxsize=1000)
def check_ingredient_match(available_ingredients, candidate_ingredients):
    _available = set(available_ingredients)
    _candidate = set(candidate_ingredients)
    return _candidate.issubset(_available)
