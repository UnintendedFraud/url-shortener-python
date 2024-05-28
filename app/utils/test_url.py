from app.utils.url import maybe_add_https, is_url_valid

from dataclasses import dataclass


@dataclass
class Example:
    data: str
    expected: str | bool


def test_maybe_add_https():
    examples = [
        Example(data="example.com", expected="https://example.com"),
        Example(data="21-dw_2fdeD.fr", expected="https://21-dw_2fdeD.fr"),

        Example(data="http://example.com", expected="http://example.com"),
        Example(data="https://example.com", expected="https://example.com"),
    ]

    for ex in examples:
        assert maybe_add_https(ex.data) == ex.expected


def test_validate_url():
    examples = [
        Example(data="example.com", expected=True),
        Example(data="http://example.com", expected=True),
        Example(data="https://example.com", expected=True),
        Example(data="21-dw_2fdeD.fr", expected=True),

        Example(data="htt:example.com", expected=False),
        Example(data="http:/example.com", expected=False),
        Example(data="//example.com", expected=False),
        Example(data="://example.com", expected=False),
        Example(data="example", expected=False),
        Example(data="https://example", expected=False),
        Example(data="https://example.f", expected=False),
    ]

    for ex in examples:
        assert is_url_valid(ex.data) == ex.expected
