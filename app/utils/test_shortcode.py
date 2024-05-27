from collections import namedtuple

from app.utils.shortcode import generate_shortcode, is_shortcode_valid

IsShortcodeValidExample = namedtuple(
    'IsShortcodeValidExample', ['code', 'expected'])


def test_is_shortcode_valid():
    examples = [
        IsShortcodeValidExample("invalid_code", False),
        IsShortcodeValidExample("w_R3d)", False),
        IsShortcodeValidExample("", False),
        IsShortcodeValidExample(None, False),

        IsShortcodeValidExample("w_R3dK", True),
    ]

    for ex in examples:
        assert is_shortcode_valid(ex.code) == ex.expected


def test_generate_shortcode():
    code = generate_shortcode()

    assert is_shortcode_valid(code)
