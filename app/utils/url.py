import re

# I am well aware that this is not matching every or only valid urls
# but I hope it'll do for this exercise
URL_PATTERN = r"^(https?://)?[a-zA-Z0-9-_]+\.[a-zA-Z]{2,}"


def maybe_add_https(url: str) -> str:
    if url.startswith("http"):
        return url

    return "https://" + url


def is_url_valid(url: str) -> bool:
    return bool(re.match(URL_PATTERN, url))
