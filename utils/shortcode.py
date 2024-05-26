import random
import re
import string


# used to generate shortcode
SHORTCODE_ALLOWED_CHARACTERS = string.ascii_letters + string.digits + "_"


def generate_shortcode() -> str:
    return ''.join(random.choices(SHORTCODE_ALLOWED_CHARACTERS, k=6))


def is_shortcode_valid(code: str) -> bool:
    if not isinstance(code, str):
        return False

    return bool(re.match(r"^[a-zA-Z0-9_]{6}$", code))
