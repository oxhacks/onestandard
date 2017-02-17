# onestandard
Convert notebooks from OneNote into [Standard Notes](https://standardnotes.org) format.

### Usage
```bash
$ python process_notes.py <path to OneNote export>
```

### Getting Notes from OneNote
#### OneNote 2016
File > Export > Notebook > Single File Web Page (*.mht)

_Other versions coming soon_

### Why?
When Linux is your daily driver, OneNote is not an available option (yet!) without
virtualization or other less than ideal setups.

### Other Considerations
#### Dependencies
Built using the fabulous [pipenv](https://github.com/kennethreitz/pipenv) from Kenneith Reitz. 
However, a `requirements.txt` is also included.

#### Python Version Support
Supports Python 3 only.
