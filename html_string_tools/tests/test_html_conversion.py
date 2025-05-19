#!/usr/bin/env python3

import html_string_tools.html_conversion as convert

def test_text_to_paragraphs():
    """
    Tests the text_to_paragraphs function.
    """
    # Test separating a single sentence into a single paragraph
    text = "  Just   one sentence!  "
    assert convert.text_to_paragraphs(text) == "<p>Just one sentence!</p>"
    # Test that multiple lines are treated as a single paragraph if appropriate
    text = "This paragraph\n exists on \n multiple \n lines... "
    assert convert.text_to_paragraphs(text) == "<p>This paragraph exists on multiple lines...</p>"
    text = "This\n\rhas\r\ncarriage\n\rreturns!"
    assert convert.text_to_paragraphs(text) == "<p>This has carriage returns!</p>"
    # Test splitting text into paragraphs based on new line with an indent, either tabbed or spaced.
    text = " First\n line.  \n    Second\n line!!  "
    assert convert.text_to_paragraphs(text) == "<p>First line.</p><p>Second line!!</p>"
    text = "Tabbed \r\n  text. \n\r\tNew paragraph."
    assert convert.text_to_paragraphs(text) == "<p>Tabbed text.</p><p>New paragraph.</p>"
    text = "All\n\tNew\n\tLines\t.\t"
    assert convert.text_to_paragraphs(text) == "<p>All</p><p>New</p><p>Lines .</p>"
    # Test splitting text into paragraphs based on having multiple newlines.
    text = "These. \n\n Are\n\n\n\nParagraphs!"
    assert convert.text_to_paragraphs(text) == "<p>These.</p><p>Are</p><p>Paragraphs!</p>"
    text = "First\r\nparagraph.\r\n\r\nSecond\r\nparagraph."
    assert convert.text_to_paragraphs(text) == "<p>First paragraph.</p><p>Second paragraph.</p>"
    # Test splitting text into paragraphs based on having quotes on the new line.
    text = "\"Same\" \"line.\"\n\"New\""
    assert convert.text_to_paragraphs(text) == "<p>&#34;Same&#34; &#34;line.&#34;</p><p>&#34;New&#34;</p>"
    text = "Start\n“Quote”\nEnd\nString."
    assert convert.text_to_paragraphs(text) == "<p>Start</p><p>“Quote”</p><p>End String.</p>"
    # Test converting special characters into HTML escape characters
    text = "This & that.\n\n>.>"
    assert convert.text_to_paragraphs(text) == "<p>This &#38; that.</p><p>&#62;.&#62;</p>"
    # Test that special characters are treated differently if the string contains HTML already
    text = "This & <i>that.</i>\n\n<span class=\"blah\">AAA</span>"
    converted = convert.text_to_paragraphs(text, True)
    assert converted == "<p>This &#38; <i>that.</i></p><p><span class=\"blah\">AAA</span></p>"

def test_html_to_text():
    """
    Tests the html_to_text function.
    """
    # Test replacing html breaks with new lines
    html = "These are<br><br />some<br/>words!"
    converted = convert.html_to_text(html, True)
    assert converted == "These are\n\nsome\nwords!"
    # Test retaining existing formatting if possible.
    html = "<pre>\nThis should remain\n\tindented.</pre>"
    converted = convert.html_to_text(html, True)
    assert converted == "This should remain\n\tindented."
    # Test replacing html paragraphs and divs with double new lines
    html = "<p>Paragraph 1</p>Outside<div>Paragraph 2</div>"
    converted = convert.html_to_text(html, True)
    assert converted == "Paragraph 1\n\nOutside\n\nParagraph 2"
    html = "First<div class='a'>Second</div>Third<p id='b'>Fourth</p>Fifth"
    converted = convert.html_to_text(html, True)
    assert converted == "First\n\nSecond\n\nThird\n\nFourth\n\nFifth"
    # Test replacing <strong> and <em> with <b> and <i> tags
    html = "<strong>AAA</strong> <em>BBB</em>"
    converted = convert.html_to_text(html, True)
    assert converted == "<b>AAA</b> <i>BBB</i>"
    html = "Thing <em id='a'>slanted</em> other <strong class='b'> Bold </strong>! "
    converted = convert.html_to_text(html, True)
    assert converted == "Thing <i>slanted</i> other <b> Bold </b>!"
    # Test removing attributes from bold and italic tags
    html = "<i id='thing'>Oblique</i> Nothing <b class='aa'>Other</b>"
    converted = convert.html_to_text(html, True)
    assert converted == "<i>Oblique</i> Nothing <b>Other</b>"
    # Test removing script and comment elements entirely
    html = "Two\n\n<!-- Comment --> Lines <script>this;is;ignored</script> Final"
    converted = convert.html_to_text(html, True)
    assert converted == "Two\n\nLines\n\nFinal"
    html = "<!-- Inside -->AAA<script id='a'> Inside </script>"
    converted = convert.html_to_text(html, True)
    assert converted == "AAA"
    # Test removing all attributes that aren't emphasis, image, or link tags
    html = "<span id='aaa'>Word.</span> <a href='thing'><i>Link</i></a><svg thing='aaa'/>"
    converted = convert.html_to_text(html, True)
    assert converted == "Word. <a href='thing'><i>Link</i></a>"
    html = "<img src='link' /><b>Bold</b> Thing <span>Other.</span>"
    converted = convert.html_to_text(html, True)
    assert converted == "<img src='link' /><b>Bold</b> Thing Other."
    # Test removing all html tags when specified
    html = "<span id='aaa'>Word.</span> <a href='thing'><i>Link</i></a><svg thing='aaa'/>"
    converted = convert.html_to_text(html, False)
    assert converted == "Word. Link"
    html = "<img src='link' /><b>Bold</b> Thing <span>Other.</span>"
    converted = convert.html_to_text(html, False)
    assert converted == "Bold Thing Other."
    # Test removing HTML escape characters
    html = "<span>This &amp; That!</span>"
    converted = convert.html_to_text(html, True)
    assert converted == "This &#38; That!"
    # Test that there are no escape characters when using total plain text
    html = "<span>&lt;3 &amp; Thing.</span>"
    converted = convert.html_to_text(html, False)
    assert converted == "<3 & Thing."
