#!/usr/bin/env python3

import os
import re
import argparse
import html_string_tools
from os.path import abspath, exists, join

def text_to_paragraphs(text:str, contains_html:bool=False) -> str:
    """
    Converts plain text to HTML, with suspected paragraphs separated into different paragraph elements.
    Paragraphs are detected by having multiple newlines, tabbed paragraph, or starting with quotes.
    If the given text contains HTML, special characters are escaped with that in mind.

    :param text: Text to separate into different paragraph elements.
    :type text: str, required
    :param contains_html: Whether the given text contains HTML elements, defaults to False
    :param contains_html: bool, optional
    """
    # Replace tabs and carriage returns
    formatted_text = text.replace("\r", "")
    formatted_text = text.replace("\t", "    ")
    # Separate sections of text into paragraphs
    # Paragraphs are detected as being multiple newlines, a newline with a quote, or a newline with a tab
    regex = r"\n\s{3,}|(?:\n\s*){2,}|\n\s*(?=[\"ʺ“”＂])|(?<=[\"ʺ“”＂])\s*\n"
    formatted_text = re.sub(regex, "{{{PPP}}}", formatted_text)
    paragraphs = formatted_text.split("{{{PPP}}}")
    # Format the text for each individual paragraph
    formatted_text = ""
    for paragraph in paragraphs:
        # Replace all newlines with simple space
        formatted_paragraph = re.sub(r"\s*\n\s*", " ", paragraph)
        # Remove unnecessary whitespace
        formatted_paragraph = re.sub(r"\s+", " ", formatted_paragraph)
        formatted_paragraph = formatted_paragraph.strip()
        # Replace characters with html escape characters, if specified
        if contains_html:
            formatted_paragraph = html_string_tools.replace_reserved_in_html(formatted_paragraph, False)
        else:
            formatted_paragraph = html_string_tools.replace_reserved_characters(formatted_paragraph, False)
        # Add the paragraph to the final text within paragraph HTML elements
        formatted_text = f"{formatted_text}<p>{formatted_paragraph}</p>"
    return formatted_text

def html_to_text(html:str, keep_tags:bool=False) -> str:
    """
    Converts HTML formatted text into simple plain text, or vastly simplified HTML
    <p> and <div> elements are turned into double new lines.
    Besides links, images, and bold/italic tags, all HTML tags are removed.
    If specified even these tags will also be removed

    :param html: HTML to convert into plain text
    :type html: str, required
    :param keep_tags: Whether to keep some basic HTML tags like <i> and <b>, defaults to False
    :type keep_tags: bool, optional
    :return: Plain text
    :rtype: str
    """
    # Replace broken ending tags
    text = html.replace("\r", "")
    text = re.sub(r"<\s+(?=[^<>]*>)", "<", text)
    text = re.sub(r"<\/\s+(?=[A-Za-z][^<>]*>)", "</", text)
    # Replace breaking space elements with new lines
    text = re.sub(r"<br\s*\/?>", "\n", text)
    # Remove html comments and script tags along with their contents
    text = re.sub(r"<!-- .* -->", "\n\n", text)
    text = re.sub(r"<script>[^<>]*<\/script>|<script\s[^<>]*>[^<>]*<\/script>", "\n\n", text)
    # Replace strong and em tags with bold and italic tags
    text = re.sub(r"<strong>|<strong\s+[^<>]*>|<b\s+[^<>]*>", "<b>", text)
    text = re.sub(r"</strong>", "</b>", text)
    text = re.sub(r"<em>|<em\s+[^<>]*>|<i\s+[^<>]*>", "<i>", text)
    text = re.sub(r"</em>", "</i>", text)
    # Replace paragraph and div elements with new lines
    text = re.sub(r"\s*<p>\s*|\s*<p\s+[^<>]*>\s*|\s*<\/p>\s*", "\n\n", text)
    text = re.sub(r"\s*<div>\s*|\s*<div\s+[^<>]*>\s*|\s*<\/div>\s*", "\n\n", text)
    # Remove unnecessary tags
    if keep_tags:
        # Remove all except <i>, <b>, <a>, <hr>, and <img> tags
        text = re.sub(r"<(?!\/|img[\/\s>]|a[\/\s>]|i[\/\s>]|b[\/\s>]|hr[\/\s>])[^<>]*>", "", text)
        text = re.sub(r"<\/(?!a>|b>|i>|img>|hr>)[^<>]*>", "", text)
    else:
        # Remove every remaining html tag
        text = re.sub(r"<[^<>]*>", "", text)
    # Replace blocks of more than 2 newlines
    text = re.sub(r"\s*\n\s*\n\s*", "\n\n", text).strip()
    # Replace reserved characters in the text
    if keep_tags:
        text = html_string_tools.replace_reserved_in_html(text, False)
    else:
        text = html_string_tools.replace_entities(text)
    # Return the modified text
    return text

def user_txt_to_html():
    """
    Converts text from a file to an HTML file based on user inputs.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
            "-i",
            "--input",
            help="Input text file to convert into HTML",
            type=str,
            default=None)
    parser.add_argument(
            "-o",
            "--output",
            help="Output HTML file",
            type=str,
            default=None)
    parser.add_argument(
            "-c",
            "--contains-html",
            help="Whether the text file contains some HTML formatting tags.",
            action="store_true")
    args = parser.parse_args()
    # Check if the user added an input or output file
    if args.input is None:
        print("\033[31mInclude an input file.\033[0m")
    elif args.output is None:
        print("\033[31mInclude an output file.\033[0m")
    else:
        # Get the absolute paths for the input and output files.
        input_file = abspath(args.input)
        output_file = abspath(args.output)
        output_parent = abspath(join(output_file, os.pardir))
        # Check if the output directory is valid
        if not exists(output_parent):
            print("\033[31mInvalid Output File.\033[0m")
        else:
            # Read the HTML text file
            file_text = None
            encodings = ["utf-8", "ascii", "latin_1", "cp437", "cp500"]
            for encoding in encodings:
                try:
                    with open(abspath(input_file), "rb") as in_file:
                        data = in_file.read()
                        text = data.decode(encoding)
                        file_text = text.strip()
                        break
                except: pass
            # Check if the HTML file contents are valid
            if file_text is None:
                print("\033[31mInvalid Input File.\033[0m")
            else:
                # Write converted text to text file
                html_text = text_to_paragraphs(file_text, args.contains_html)
                html_text = f"<!DOCTYPE html><html><body>{html_text}</body></html>"
                with open(output_file, "w", encoding="UTF-8") as out:
                    out.write(html_text)

def user_html_to_txt():
    """
    Converts HTML from a file to a text file based on user inputs.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
            "-i",
            "--input",
            help="Input HTML file to convert into text",
            type=str,
            default=None)
    parser.add_argument(
            "-o",
            "--output",
            help="Output text file",
            type=str,
            default=None)
    parser.add_argument(
            "-k",
            "--keep-tags",
            help="Whether to keep basic HTML tags in the exported text",
            action="store_true")
    args = parser.parse_args()
    # Check if the user added an input or output file
    if args.input is None:
        print("\033[31mInclude an input file.\033[0m")
    elif args.output is None:
        print("\033[31mInclude an output file.\033[0m")
    else:
        # Get the absolute paths for the input and output files.
        input_file = abspath(args.input)
        output_file = abspath(args.output)
        output_parent = abspath(join(output_file, os.pardir))
        # Check if the output directory is valid
        if not exists(output_parent):
            print("\033[31mInvalid Output File.\033[0m")
        else:
            # Read the HTML text file
            html_text = None
            encodings = ["utf-8", "ascii", "latin_1", "cp437", "cp500"]
            for encoding in encodings:
                try:
                    with open(abspath(input_file), "rb") as in_file:
                        data = in_file.read()
                        text = data.decode(encoding)
                        html_text = text.strip()
                        break
                except: pass
            # Check if the HTML file contents are valid
            if html_text is None:
                print("\033[31mInvalid Input File.\033[0m")
            else:
                # Write converted text to text file
                text = html_to_text(html_text, args.keep_tags)
                with open(output_file, "w", encoding="UTF-8") as out:
                    out.write(text)
