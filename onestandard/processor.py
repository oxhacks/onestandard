"""Utility to convert OneNote notebooks into Markdown."""

import logging
from collections import OrderedDict, namedtuple
from html import unescape

from bs4 import BeautifulSoup
import html2text


NOTE_STYLE = "3D'direction:ltr;border-width:100%'"
REPLACEMENTS = OrderedDict([
    ("\n", " "),
    ("= ", ""),
    ("-", '')
])
RawNote = namedtuple('RawNote', ['title', 'markdown', 'markup', 'headers'])


def get_soup(filepath):
    """Turn the given filepath into Beautiful Soup.

    :param filepath: the path to the HTML file to parse
    :returns: a `BeautifulSoup` object representing the parsed markup

    """
    with open(filepath, encoding='latin1') as infile:
        soup = BeautifulSoup(infile.read(), 'lxml')
    return soup


def extract_parts(note):
    """Search a given chunk of markup for specific references.

    :param note: the `BeautifulSoup` version of the markup to parse
    :returns: a tuple of the title, headers, and content

    """
    parts = note.find_all('div')
    if len(parts) == 3:
        title, headers, content = parts
    elif len(parts) == 2:
        title, headers = parts
        content = ''
    else:
        title, headers = parts[:2]
        content = parts[2]
    return title, headers, content


def get_notes(soup, note_style=NOTE_STYLE):
    """A generator to search through the notes and yield parsed content.

    :param soup: the `BeautifulSoup` version of the document markup
    :param note_style: the style tag used to signify notes
    :returns: (yields) a tuple of the title, headers, and content

    """
    notes = soup.find_all('div')
    for note in notes:
        style = str(note.get('style'))
        if style == note_style:
            note = note.find('div')
            try:
                title, headers, content = extract_parts(note)
            except ValueError:
                logging.warning('Could not parse note: %s', note.get_text())
                continue
            yield title, headers, content


def fix_line(line, replacements=None):
    """Fix the line by replacing the newline characters OneNote inserts.

    :param line: the line string to fix
    :param replacements: a dict of the replacements to use
    :returns: an enescaped version of the HTML line

    """
    if not replacements:
        replacements = REPLACEMENTS
    line = line.strip()
    for value, replacement in replacements.items():
        line = line.replace(value, replacement)
    return unescape(line)


def strip_linebreaks(text):
    """Turn double linebreaks into a single.

    :param text: the text to perform the replacement within
    :returns: the text stripped of extra linebreaks

    """
    return text.replace("\n\n", "\n")


def process_note(title, headers, content):
    """Helper to turn the note parts into a `namedtuple` that holds the parts.

    :param title: the `Tag` object to use for the title
    :param headers: the headers that contain the date and time
    :param content: the raw markup to turn into Markdown format
    :returns: a `namedtuple` object holding the fixed fields

    """
    title = fix_line(title.text)
    content = fix_line(str(content))
    markdown = html2text.html2text(content)
    markdown = strip_linebreaks(markdown)
    return RawNote(title, markdown, content, headers)
