#!/usr/bin/env

from html import unescape
from re import findall as re_find
from re import sub as re_sub

def regex_replace(funct, pattern:str, string:str) -> str:
    """
    Replaces text matching regex pattern with said matching text run though a given function.

    :param funct: Function to run matching text through, required
    :type funct: function, required
    :param pattern: Regex pattern to search for in string
    :type pattern: str, required
    :param string: String to search for pattern within
    :type string: str, required
    :return: Given string with pattern matched text replaced
    :rtype: str
    """
    try:
        # Get all strings that match the regex pattern
        matches = re_find(pattern, string)
        # Run through all matches to replace text
        new_text = ""
        left_text = string
        for match in matches:
            # Keep all of the text begore the match
            index = left_text.find(match)
            new_text = new_text + left_text[:index]
            # Add replacement for the match
            new_text = new_text + funct(match)
            # Set the remaining text for after the match
            index += len(match)
            left_text = left_text[index:]
        # Keep all the text left in the initial string
        new_text = new_text + left_text
        # Return the string with matching patterns replaced
        return new_text
    except TypeError: return string

def remove_whitespace(string:str) -> str:
    """
    Removes whitespace from the beggining and end of a given string.

    :param string: Given string to remove whitespace from
    :type string: str, required
    :return: String with the whitespace removed
    :rtype: str
    """
    try:
        # Remove leading and ending whitespace
        return re_sub("^\\s+|\\s+$", "", string)
    except TypeError: return string

def get_extension(path:str) -> str:
    """
    Returns the extension for a given filename or direct file URL.
    If extension does not exist, returns empty.

    :param path: Given path with extension
    :type path: str, required
    :return: Extension for the path
    :rtype: str
    """
    try:
        # Find potential extensions
        match = re_find("\\.[a-zA-Z0-9]{1,5}\\?|\\.[a-zA-Z0-9]{1,5}$", path)
        # Remove "?" from end of extension, if necessary
        extension = match[0]
        for item in match:
            if item.endswith("?"):
                extension = item[:len(item)-1]
        # Return the extension
        return extension
    except (IndexError, TypeError): return ""

def entity_to_character(entity:str) -> str:
    """
    Returns single character for a given HTML entity escape character.
    Returned in string format. Returns the given string if not an HTML entity.

    :param escape: HTML escape character
    :type escape: str, required
    :return: Unicode character
    :rtype: str
    """
    try:
        # Check that the given string is an HTML entity
        return unescape(re_find("^&[^&;]+;$", entity)[0])
    except (IndexError, TypeError): return entity

def replace_entities(string:str=None) -> str:
    """
    Replaces all HTML entities in a string with Unicode characters.

    :param string: Given string
    :type string: str, required
    :return: String with HTML escape characters replaced
    :rtype: str
    """
    return regex_replace(entity_to_character, "&[^&;]+;", string)

def character_to_entity(character:str) -> str:
    """
    Converts a single character into an HTML entity.

    :param character: Single character to convert into an HTML escape
    :type character: str, required
    :return: HTML entity for the given character
    :rtype: str
    """
    try:
        # Convert character to HTML entity
        return "&#" + str(ord(character)) + ";"
    except TypeError: return ""

def replace_reserved_characters(string:str, escape_non_ascii:bool=False) -> str:
    """
    Replaces all reserved HTML characters with escape entities.
    Also replaces all non-ASCII characters, if specified.

    :param string: String to replace characters within
    :type string: str, required
    :param escape_non_ascii: Whether to replace non-ASCII characters, defaults to False
    :type escape_non_ascii: bool, optional
    :return: String with reserved characters replaced
    :rtype: str
    """
    regex = "[<>/='\"&;]"
    if escape_non_ascii: regex = "[<>/='\"&;]|[^ -~]"
    return regex_replace(character_to_entity, regex, string)

def replace_reserved_in_html(html_string:str, escape_non_ascii:bool=False) -> str:
    """
    Replaces reserved HTML characters in text which already contains HTML syntax.
    Preserves any text within HTML elements.

    :param html_string: HTML string to replace characters within
    :type html_string: str, required
    :param escape_non_ascii: Whether to replace non-ASCII characters, defaults to False
    :type escape_non_ascii: bool, optional
    :return: HTML string with characters replaced with character entities
    :rtype: str
    """
    try:
        # Find all HTML element blocks
        elements = re_find("<[^<>]+>", html_string)
        # Run through each HTML element
        left_text = html_string
        new_text = ""
        for element in elements:
            # Replace characters in text before the element
            index = left_text.find(element)
            replaced = replace_entities(left_text[:index])
            replaced = replace_reserved_characters(replaced, escape_non_ascii)
            left_text = left_text[index+len(element):]
            new_text = new_text + replaced + element
        # Replace characters in all remaining text
        replaced = replace_entities(left_text)
        new_text = new_text + replace_reserved_characters(replaced, escape_non_ascii)
        return new_text
    except TypeError: return html_string
