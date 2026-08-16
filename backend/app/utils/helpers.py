import json


def safe_json(val):
    """Safely parse a JSON value from DB. Handles cases where SQLite stores int/float instead of text."""
    if val is None or val == '':
        return None
    if isinstance(val, (list, dict)):
        return val
    if isinstance(val, str):
        try:
            return json.loads(val)
        except (json.JSONDecodeError, ValueError):
            return val
    return val
