#!/usr/bin/env python3

"""
Setuptools setup file.
"""

import setuptools

console_scripts = [
    "html-to-text = html_string_tools.html_conversion:user_html_to_txt",
    "text-to-html = html_string_tools.html_conversion:user_txt_to_html"]

with open("README.md", "r") as fh:
    long_description = fh.read()

desc = "A simple set of scripts for handling, formatting, and converting HTML formatted text."

setuptools.setup(
    name="HTML-String-Tools",
    version="0.4.2",
    author="Drakovek",
    author_email="DrakovekMail@gmail.com",
    description=desc,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Drakovek/HTML-String-Tools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.0',
    entry_points={"console_scripts": console_scripts}
)
