#!/usr/bin/env

import html_string_tools as html_st

def test_get_extension():
    """
    Tests the get_extension function.
    """
    # Test getting extensions from filenames
    assert html_st.get_extension("test.png") == ".png"
    assert html_st.get_extension(".long") == ".long"
    assert html_st.get_extension("test2.thing") == ".thing"
    assert html_st.get_extension("blah.test.png") == ".png"
    # Test getting extensions from URLs with tokens
    assert html_st.get_extension("test.mp4?extra_.thing") == ".mp4"
    assert html_st.get_extension("thing.test.thing?") == ".thing"
    assert html_st.get_extension("another.txt? test.png?extra.thing") == ".png"
    # Test getting invalid extensions
    assert html_st.get_extension("test.tolong") == ""
    assert html_st.get_extension("test.notextension") == ""
    assert html_st.get_extension("asdfasdfasdfasdf") == ""
    assert html_st.get_extension("test.tolong?extra") == ""
    assert html_st.get_extension("none?") == ""
    # Test getting extension if given string is None
    assert html_st.get_extension(None) == ""

def test_entity_to_char():
    """
    Tests the entity_to_char function.
    """
    # Test replacing HTML character entities
    assert html_st.entity_to_character("&quot;") == "\""
    assert html_st.entity_to_character("&apos;") == "'"
    assert html_st.entity_to_character("&amp;") == "&"
    assert html_st.entity_to_character("&lt;") == "<"
    assert html_st.entity_to_character("&gt;") == ">"
    assert html_st.entity_to_character("&nbsp;") == " "
    assert html_st.entity_to_character("&#60;") == "<"
    assert html_st.entity_to_character("&#38;") == "&"
    # Test non-latin HTML entities
    assert html_st.entity_to_character("&Agrave;") == "À"
    assert html_st.entity_to_character("&Aacute;") == "Á"
    assert html_st.entity_to_character("&Auml;") == "Ä"
    assert html_st.entity_to_character("&Atilde;") == "Ã"
    assert html_st.entity_to_character("&Aring;") == "Å"
    # Test replacing invalid escape characters
    assert html_st.entity_to_character(None) is None
    assert html_st.entity_to_character("") == ""
    assert html_st.entity_to_character(" ") == " "
    assert html_st.entity_to_character("&;") == "&;"
    assert html_st.entity_to_character("&nope;") == "&nope;"
    assert html_st.entity_to_character("&#nope;") == "&#nope;"
    assert html_st.entity_to_character("&#;") == "&#;"

def test_replace_entities():
    """
    Tests the replace_entities function.
    """
    # Test replacing HTML enities in string
    in_str = "&lt;i&gt;T&euml;st HTML&#60;&#47;i&#62;"
    assert html_st.replace_entities(in_str) == "<i>Tëst HTML</i>"
    in_str = "this&that"
    assert html_st.replace_entities(in_str) == "this&that"
    in_str = "remove&this;"
    assert html_st.replace_entities(in_str) == "remove&this;"
    # Test replacing HTML entities in ivalid test
    assert html_st.replace_entities(None) == None

def test_char_to_entity():
    """
    Tests the char_to_entity function.
    """
    # Test converting characters into html escape characters
    assert html_st.character_to_entity("&") == "&#38;"
    assert html_st.character_to_entity("/") == "&#47;"
    assert html_st.character_to_entity("<") == "&#60;"
    # Test converting strings that are too long
    assert html_st.character_to_entity("string") == ""
    assert html_st.character_to_entity("<>") == ""
    # Test converting invalid characters
    assert html_st.character_to_entity(None) == ""
    assert html_st.character_to_entity("") == ""

def test_replace_reserved_characters():
    """
    Tests the replace_reserved_characters function.
    """
    # Test replacing reserved characters
    assert html_st.replace_reserved_characters("<bláh~!>") == "&#60;bláh~!&#62;"
    assert html_st.replace_reserved_characters("<a href=\"thíng...\">") == "&#60;a href&#61;&#34;thíng...&#34;&#62;"
    assert html_st.replace_reserved_characters("<ímg src='Heh?'>") == "&#60;ímg src&#61;&#39;Heh?&#39;&#62;"
    assert html_st.replace_reserved_characters("&Éh;") == "&#38;Éh&#59;"
    # Test replacing reserved characters and non-ASCII characters
    assert html_st.replace_reserved_characters("<bláh~!>", True) == "&#60;bl&#225;h~!&#62;"
    assert html_st.replace_reserved_characters("<a href=\"thíng...\">", True) == "&#60;a href&#61;&#34;th&#237;ng...&#34;&#62;"
    assert html_st.replace_reserved_characters("<ímg src='Heh?'>", True) == "&#60;&#237;mg src&#61;&#39;Heh?&#39;&#62;"
    assert html_st.replace_reserved_characters("&Éh;", True) == "&#38;&#201;h&#59;"
    # Test replacting reserved characters in invalid string
    assert html_st.replace_reserved_characters(None) is None
    assert html_st.replace_reserved_characters("") == ""

def test_replace_reserved_in_html():
    """
    Tests the replace_reserved_in_html function.
    """
    # Test that HTML tags are kept intact while the rest of text are preserved.
    assert html_st.replace_reserved_in_html("<ímg>Bláh!</ímg>", True) == "<ímg>Bl&#225;h!</ímg>"
    assert html_st.replace_reserved_in_html("<a href=\"bleh\">&thing;<\a>") == "<a href=\"bleh\">&#38;thing&#59;<\a>"
    # Test replacing text with no elements
    assert html_st.replace_reserved_in_html(">It's a thing!!<") == "&#62;It&#39;s a thing!!&#60;"
    # Test replacing text before and after element
    assert html_st.replace_reserved_in_html(";; <&thing!> &!") == "&#59;&#59; <&thing!> &#38;!"
    # Tests that already existing escape characters remain intact
    assert html_st.replace_reserved_in_html("<a>Th&#237;ng!!</a>", True) == "<a>Th&#237;ng!!</a>"
    assert html_st.replace_reserved_in_html("<a>Th&#237;ng!!</a>") == "<a>Thíng!!</a>"
    assert html_st.replace_reserved_in_html("&#59; <&!> &#59;") == "&#59; <&!> &#59;"
    # Test replacing characters with invalid text
    assert html_st.replace_reserved_in_html(None) == None
    assert html_st.replace_reserved_in_html("") == ""

def test_make_human_readable():
    """
    Tests the make_human_readable function
    """
    # Test making html human readable
    base = "<html><thing>Thing</thing><body>Other</body></html>"
    formatted = html_st.make_human_readable(base)
    compare = ""
    compare = f"{compare}<html>\n"
    compare = f"{compare}    <thing>Thing</thing>\n"
    compare = f"{compare}    <body>Other</body>\n"
    compare = f"{compare}</html>"

    print(formatted)

    assert formatted == compare
    base = "<html><head>Thing</head><body><div>Something</div><item blah=''/></body></html>"
    formatted = html_st.make_human_readable(base)
    compare = ""
    compare = f"{compare}<html>\n"
    compare = f"{compare}    <head>Thing</head>\n"
    compare = f"{compare}    <body>\n"
    compare = f"{compare}        <div>Something</div>\n"
    compare = f"{compare}        <item blah=''/>\n"
    compare = f"{compare}    </body>\n"
    compare = f"{compare}</html>"
    assert formatted == compare
    # Test with paragraph tags
    base = "<html url='/blah/'><head>Thing</head><body>"
    base = f"{base}<p>Something <b>BIG</b></p>"
    base = f"{base}<p class='thing'><a href=''>Link</a> Thing.</p>"
    base = f"{base}<p><i>internal</i><b>Thing</b></p>"
    base = f"{base}</body></html>"
    formatted = html_st.make_human_readable(base, "   ")
    compare = ""
    compare = f"{compare}<html url='/blah/'>\n"
    compare = f"{compare}   <head>Thing</head>\n"
    compare = f"{compare}   <body>\n"
    compare = f"{compare}      <p>Something <b>BIG</b></p>\n"
    compare = f"{compare}      <p class='thing'><a href=''>Link</a> Thing.</p>\n"
    compare = f"{compare}      <p><i>internal</i><b>Thing</b></p>\n"
    compare = f"{compare}   </body>\n"
    compare = f"{compare}</html>"
    assert formatted == compare
    # Test with existing spaces & newline characters
    base = "<html>\n\n  <head> AAA </head>\n \n<div>Thing  </div> </html>"
    formatted = html_st.make_human_readable(base, " ")
    compare = ""
    compare = f"{compare}<html>\n"
    compare = f"{compare} <head> AAA </head>\n"
    compare = f"{compare} <div>Thing  </div>\n"
    compare = f"{compare}</html>"
    assert formatted == compare
    # Test with improperly formatted html
    base = "</all></back></ports>"
    formatted = html_st.make_human_readable(base, "    ")
    assert formatted == "</all>\n</back>\n</ports>"
    base = "<html><head>Thing</head><p>Unfinished</html>"
    formatted = html_st.make_human_readable(base)
    compare = ""
    compare = f"{compare}<html>\n"
    compare = f"{compare}    <head>Thing</head>\n"
    compare = f"{compare}    <p>Unfinished</html>"
    assert formatted == compare
