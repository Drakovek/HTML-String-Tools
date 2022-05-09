#!/usr/bin/env

from html_string_tools.main.html_string_tools import character_to_entity
from html_string_tools.main.html_string_tools import get_extension
from html_string_tools.main.html_string_tools import entity_to_character
from html_string_tools.main.html_string_tools import regex_replace
from html_string_tools.main.html_string_tools import remove_whitespace
from html_string_tools.main.html_string_tools import replace_entities
from html_string_tools.main.html_string_tools import replace_reserved_characters as rrc
from html_string_tools.main.html_string_tools import replace_reserved_in_html as rrih

def test_remove_whitespace():
    """
    Tests the remove_whitespace function.
    """
    # Test removing whitespace from the beginning and end of strings
    assert remove_whitespace("") == ""
    assert remove_whitespace(" ") == ""
    assert remove_whitespace(" \t  ") == ""
    assert remove_whitespace("  blah") == "blah"
    assert remove_whitespace("blah   ") == "blah"
    assert remove_whitespace(" \t blah  \t") == "blah"
    assert remove_whitespace(" Other Text \n") == "Other Text"
    assert remove_whitespace("   Yet \n more Text \n \r") == "Yet \n more Text"    
    assert remove_whitespace("blah") == "blah"
    # Test using invalid string
    assert remove_whitespace(None) is None
    assert remove_whitespace(4) == 4

def test_get_extension():
    """
    Tests the get_extension function.
    """
    # Test getting extensions from filenames
    assert get_extension("test.png") == ".png"
    assert get_extension(".long") == ".long"
    assert get_extension("test2.thing") == ".thing"
    assert get_extension("blah.test.png") == ".png"
    # Test getting extensions from URLs with tokens
    assert get_extension("test.mp4?extra_.thing") == ".mp4"
    assert get_extension("thing.test.thing?") == ".thing"
    assert get_extension("another.txt? test.png?extra.thing") == ".png"
    # Test getting invalid extensions
    assert get_extension("test.tolong") == ""
    assert get_extension("test.notextension") == ""
    assert get_extension("asdfasdfasdfasdf") == ""
    assert get_extension("test.tolong?extra") == ""
    assert get_extension("none?") == ""
    # Test getting extension if given string is None
    assert get_extension(None) == ""

def test_regex_replace():
    """
    Tests the regex replace function.
    """
    # Test replacing regex matches
    replaced = regex_replace(get_extension, "[a-z]+\\.[a-z]+", "eh, bl.ah th.ing not")
    assert replaced == "eh, .ah .ing not"
    replaced = regex_replace(remove_whitespace, "\\s*[0-9]+\\s*", "   Some random  2   text!  1234!  and rest ")
    assert replaced == "   Some random2text!1234!  and rest "
    # Test replacing strings with no regex match
    replaced = regex_replace(get_extension, "nope", "got nothing")
    assert replaced == "got nothing"
    # Test replacing strings with invalid parameters
    assert regex_replace(None, "pattern", "string") == "string"
    assert regex_replace(get_extension, None, "string") == "string"
    assert regex_replace(get_extension, "pattern", None) is None

def test_entity_to_char():
    """
    Tests the entity_to_char function.
    """
    # Test replacing HTML character entities
    assert entity_to_character("&quot;") == "\""
    assert entity_to_character("&apos;") == "'"
    assert entity_to_character("&amp;") == "&"
    assert entity_to_character("&lt;") == "<"
    assert entity_to_character("&gt;") == ">"
    assert entity_to_character("&nbsp;") == " "
    assert entity_to_character("&#60;") == "<"
    assert entity_to_character("&#38;") == "&"
    # Test non-latin HTML entities
    assert entity_to_character("&Agrave;") == "À"
    assert entity_to_character("&Aacute;") == "Á"
    assert entity_to_character("&Auml;") == "Ä"
    assert entity_to_character("&Atilde;") == "Ã"
    assert entity_to_character("&Aring;") == "Å"
    # Test replacing invalid escape characters
    assert entity_to_character(None) is None
    assert entity_to_character("") == ""
    assert entity_to_character(" ") == " "
    assert entity_to_character("&;") == "&;"
    assert entity_to_character("&nope;") == "&nope;"
    assert entity_to_character("&#nope;") == "&#nope;"
    assert entity_to_character("&#;") == "&#;"

def test_replace_entities():
    """
    Tests the replace_entities function.
    """
    # Test replacing HTML enities in string
    in_str = "&lt;i&gt;T&euml;st HTML&#60;&#47;i&#62;"
    assert replace_entities(in_str) == "<i>Tëst HTML</i>"
    in_str = "this&that"
    assert replace_entities(in_str) == "this&that"
    in_str = "remove&this;"
    assert replace_entities(in_str) == "remove&this;"
    # Test replacing HTML entities in ivalid test
    assert replace_entities(None) == None

def test_char_to_entity():
    """
    Tests the char_to_entity function.
    """
    # Test converting characters into html escape characters
    assert character_to_entity("&") == "&#38;"
    assert character_to_entity("/") == "&#47;"
    assert character_to_entity("<") == "&#60;"
    # Test converting strings that are too long
    assert character_to_entity("string") == ""
    assert character_to_entity("<>") == ""
    # Test converting invalid characters
    assert character_to_entity(None) == ""
    assert character_to_entity("") == ""

def test_replace_reserved_characters():
    """
    Tests the replace_reserved_characters function.
    """
    # Test replacing reserved characters
    assert rrc("<bláh~!>") == "&#60;bláh~!&#62;"
    assert rrc("<a href=\"thíng...\">") == "&#60;a href&#61;&#34;thíng...&#34;&#62;"
    assert rrc("<ímg src='Heh?'>") == "&#60;ímg src&#61;&#39;Heh?&#39;&#62;"
    assert rrc("&Éh;") == "&#38;Éh&#59;"
    # Test replacing reserved characters and non-ASCII characters
    assert rrc("<bláh~!>", True) == "&#60;bl&#225;h~!&#62;"
    assert rrc("<a href=\"thíng...\">", True) == "&#60;a href&#61;&#34;th&#237;ng...&#34;&#62;"
    assert rrc("<ímg src='Heh?'>", True) == "&#60;&#237;mg src&#61;&#39;Heh?&#39;&#62;"
    assert rrc("&Éh;", True) == "&#38;&#201;h&#59;"
    # Test replacting reserved characters in invalid string
    assert rrc(None) is None
    assert rrc("") == ""

def test_replace_reserved_in_html():
    """
    Tests the replace_reserved_in_html function.
    """
    # Test that HTML tags are kept intact while the rest of text are preserved.
    assert rrih("<ímg>Bláh!</ímg>", True) == "<ímg>Bl&#225;h!</ímg>"
    assert rrih("<a href=\"bleh\">&thing;<\a>") == "<a href=\"bleh\">&#38;thing&#59;<\a>"
    # Test replacing text with no elements
    assert rrih(">It's a thing!!<") == "&#62;It&#39;s a thing!!&#60;"
    # Test replacing text before and after element
    assert rrih(";; <&thing!> &!") == "&#59;&#59; <&thing!> &#38;!"
    # Tests that already existing escape characters remain intact
    assert rrih("<a>Th&#237;ng!!</a>", True) == "<a>Th&#237;ng!!</a>"
    assert rrih("<a>Th&#237;ng!!</a>") == "<a>Thíng!!</a>"
    assert rrih("&#59; <&!> &#59;") == "&#59; <&!> &#59;"
    # Test replacing characters with invalid text
    assert rrih(None) == None
    assert rrih("") == ""
