"""Utility script to process notes from the command line."""

import sys
import os

from onestandard import processor, models


def create_tag(filename):
    basename = os.path.basename(filename)
    noext = basename.split('.')[0]
    return models.Tag(noext)


if __name__ == '__main__':
    soup = processor.get_soup(sys.argv[1])
    package = models.Package()
    tag = create_tag(sys.argv[1])
    package.add(tag)
    notes = processor.get_notes(soup)
    for title, headers, content in notes:
        print("===========")
        raw_note = processor.process_note(title, headers, content)
        #print(raw_note.markdown)
        note = models.Note(raw_note.title, raw_note.markdown)
        models.link(note, tag)
        package.add(note)
    
    package.write('package.json')