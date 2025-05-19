# HTML-String-Tools

HTML-String-Tools is a simple set of python scripts for formatting and converting HTML text. It's mainly intended for use as a library, but there are a couple command line utilities for converting between HTML and plain text as well.

- [Installation](#installation)
- [Functions](#functions)
- [CLI](#cli)

# Installation

HTML-String-Tools can be downloaded from its PyPI package using pip:

    pip3 install HTML-String-Tools

HTML-String-Tools only uses standard libraries included with Python3, so there are no additional required packages if building from source.

# Functions

There are several functions in HTML-String-Tools you can use in your python projects.

## get_extension

Returns the extension of a given URI or file

    import html_string_tools

    extension = html_string_tools.get_extension("path/to/resourse/image.png?1234")
    # extension will be ".png"

## entity_to_character

Returns a single unicode character corresponding to a given HTML escape entity.

    import html_string_tools

    character = html_string_tools.entity_to_character("&#38;")
    # character will be "&"

    character = html_string_tools.entity_to_character("&gt;")
    # character will be ">"

## character_to_entity

Converts a single unicode character into an HTML escape entity

    import html_string_tools

    entity = html_string_tools.character_to_entity("&")
    # entity will be "&#38;"

## replace_entities

Replaces all HTML escape entities in a given string with their corresponding unicode characters

    import html_string_tools

    string = html_string_tools.replace_entities("This &amp; That &#60;3")
    # string will be "This & That <3"

## replace_reserved_characters

Replaces all reserved HTML characters in a string with HTML escape entities

    import html_string_tools

    string = html_string_tools.replace_reserved_characters("This & That <3")
    # string will be "This &#38; That &#60;3"

This function also has an optional `escape_non_ascii` bool parameter that when true, will replace ALL non-standard ASCII characters in the string with HTML escape entities, not just characters reserved for HTML.

    import html_string_tools

    string = html_string_tools.replace_reserved_characters("<Tést>", escape_non_ascii=True)
    # string will be "&#60;T&#233;st&#62;"

## replace_reserved_in_html

Attempts to replace reserved HTML characters with HTML escape entities in a string that already contains HTML syntax. This function will keep HTML tags and attributes intact, while replacing any characters within the user readable text that shouldn't contain reserved HTML characters.

    import html_string_tools

    string = html_string_tools.replace_reserved_in_html("<i>Text <3</i>")
    # string will be "<i>Text &#60;3</i>"

Like the `replace_reserved_characters` function, this function also has an optional `escape_non_ascii` bool parameter that when true, will replace ALL non-standard ASCII characters in the string with HTML escape entities. This will NOT affect text that is part of an HTML tag or attribute.

    import html_string_tools

    string = html_string_tools.replace_reserved_in_html("<span id='á'>á</span>", escape_non_ascii=True)
    # string will be "<span id='á'>&#225;</span>"

## text_to_paragraphs

Breaks up plain text into a series of HTML paragraphs enclosed in <p> tags. Determines whether text on different lines should be considered part of the same paragraph based on number of new lines, indentation, and lines starting with quotes.

This includes a `contains_html` bool parameter that determines how to escape characters that are reserved for HTML. If False, all reserved characters in the text are escaped. If True, HTML tags and attributes are left intact while readable text is escaped. Defaults to False.

    import html_string_tools

    string = html_string_tools.text_to_paragraphs("Line 1\n\nLine 2")
    # string will be "<p>Line 1</p><p>Line 2</p>"

## html_to_text

Converts string with HTML formatting into simple plain text. HTML tags are removed, and both the tags and unreadable text inside of comments and \<script\> tags are removed. The text is spaced out with new lines appropriately based on how they would have been separated in the original HTML.

    import html_string_tools

    string = html_string_tools.html_to_text("<p>Line 1</p><p>Line 2</p>")
    # string will be "Line 1\n\nLine 2"

There is also a `keep_tags` bool parameter that defaults to False. When True, most HTML elements are removed as normal, but images, links, and basic formatting like italic and bold tags remain intact. This is intended to drastically simplify HTML, and can be used in conjunction with `text_to_paragraphs` to create HTML suited for reader mode.

# CLI

There are two command line scripts for converting between text files and HTML files.

## Text to HTML

Use the `text-to-html` command to convert plain text to an HTML file. Runs off of the function described above: `text_to_paragraphs`.

    text-to-html -i input.txt -o output.html

## HTML to Text

Use the `html-to-text` command to convert an HTML file into plain text. Runs off of the function described above: `html_to_text`

    html-to-text -i input.htm -o output.txt
