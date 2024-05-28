from dataclasses import dataclass

from app.utils.shortcode import generate_shortcode, is_shortcode_valid


@dataclass
class Example:
    data: str
    expected: bool


def test_is_shortcode_valid():
    examples = [
        Example(data="invalid_code", expected=False),
        Example(data="w_R3d)", expected=False),
        Example(data="", expected=False),
        Example(data=None, expected=False),

        Example(data="w_R3dK", expected=True),
    ]

    for ex in examples:
        assert is_shortcode_valid(ex.data) == ex.expected


def test_generate_shortcode():
    for i in range(10):
        code = generate_shortcode()

        assert is_shortcode_valid(code)
