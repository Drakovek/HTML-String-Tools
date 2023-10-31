#!/usr/bin/env python3

import re

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
        matches = re.findall(pattern, string)
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