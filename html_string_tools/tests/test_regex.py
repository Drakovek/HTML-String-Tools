#!/usr/bin/env

from html_string_tools import html, regex

def test_remove_whitespace():
    """
    Tests the remove_whitespace function.
    """
    # Test removing whitespace from the beginning and end of strings
    assert regex.remove_whitespace("") == ""
    assert regex.remove_whitespace(" ") == ""
    assert regex.remove_whitespace(" \t  ") == ""
    assert regex.remove_whitespace("  blah") == "blah"
    assert regex.remove_whitespace("blah   ") == "blah"
    assert regex.remove_whitespace(" \t blah  \t") == "blah"
    assert regex.remove_whitespace(" Other Text \n") == "Other Text"
    assert regex.remove_whitespace("   Yet \n more Text \n \r") == "Yet \n more Text"    
    assert regex.remove_whitespace("blah") == "blah"
    # Test using invalid string
    assert regex.remove_whitespace(None) is None
    assert regex.remove_whitespace(4) == 4

def test_regex_replace():
    """
    Tests the regex replace function.
    """
    # Test replacing regex matches
    replaced = regex.regex_replace(html.get_extension, "[a-z]+\\.[a-z]+", "eh, bl.ah th.ing not")
    assert replaced == "eh, .ah .ing not"
    replaced = regex.regex_replace(regex.remove_whitespace, "\\s*[0-9]+\\s*", "   Some random  2   text!  1234!  and rest ")
    assert replaced == "   Some random2text!1234!  and rest "
    # Test replacing strings with no regex match
    replaced = regex.regex_replace(html.get_extension, "nope", "got nothing")
    assert replaced == "got nothing"
    # Test replacing strings with invalid parameters
    assert regex.regex_replace(None, "pattern", "string") == "string"
    assert regex.regex_replace(html.get_extension, None, "string") == "string"
    assert regex.regex_replace(html.get_extension, "pattern", None) is None