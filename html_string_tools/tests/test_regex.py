#!/usr/bin/env

from html_string_tools import html, regex

def test_regex_replace():
    """
    Tests the regex replace function.
    """
    # Test replacing regex matches
    replaced = regex.regex_replace(html.get_extension, "[a-z]+\\.[a-z]+", "eh, bl.ah th.ing not")
    assert replaced == "eh, .ah .ing not"
    # Test replacing strings with no regex match
    replaced = regex.regex_replace(html.get_extension, "nope", "got nothing")
    assert replaced == "got nothing"
    # Test replacing strings with invalid parameters
    assert regex.regex_replace(None, "pattern", "string") == "string"
    assert regex.regex_replace(html.get_extension, None, "string") == "string"
    assert regex.regex_replace(html.get_extension, "pattern", None) is None