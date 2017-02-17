"""Models representing Standard File based objects."""


import json
from uuid import uuid4
from datetime import datetime


ALLOWED_TYPES = ('tag', 'note')


def link(standard1, standard2):
    """Create bi-directional references linking the two Standard-based objects.

    :param standard1: the first `Standard` object to be linked
    :param standard2: another `Standard` object to be linked
    :returns: `None`

    """
    standard1.references.append(standard2.reference)
    standard2.references.append(standard1.reference)
    return


class WrongTypeException(Exception):
    """An exception to throw if the Standard object isn't an allowed type."""
    pass


class Standard(object):
    """The base object from which the others shall derive."""
    def __init__(self, title, content_type, guid=None):
        self.content_type = content_type.lower()
        self._validate_type()
        self.title = title
        self.guid = guid if guid else str(uuid4())
        self.created_at = self.updated_at = datetime.utcnow().isoformat() + 'Z'
        self.references = []
        self.model = {
            "uuid": self.guid,
            "content_type": self.content_type,
            "content": {
                "title": self.title,
                "references": self.references
            },
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def __repr__(self):
        return '<{}: {}>'.format(self.content_type, self.guid)

    @property
    def reference(self):
        """Get a reference object for use in linking objects together.

        :returns: a dict with the guid and content type

        """
        return {
            'uuid': self.guid,
            'content_type': 'Tag'
        }

    def _validate_type(self, allowed=ALLOWED_TYPES):
        """Ensure that the type specified is valid.

        :param allowed: an iterable of the allowed types
        :raises: `onestandard.models.OneTypeException` if not a valid type

        """
        if self.content_type not in allowed:
            allowed = ', '.join(allowed)
            error_message = "Type '{}' not one of {}".format(self.content_type, allowed)
            raise WrongTypeException(error_message)

    def json(self, *args, **kwargs):
        """Dump the Standard model into JSON format.

        :param *args: positional arguments to pass to `json.dumps`
        :param **kwargs: keyword arguments to pass to `json.dumps`
        :returns: a JSON-ified string of the object model

        """
        return json.dumps(self.model, indent=4, *args, **kwargs)


class Tag(Standard):
    """A Standard Notes Tag object, used to sort notes."""
    def __init__(self, title, guid=None):
        super().__init__(title=title, content_type='Tag')


class Note(Standard):
    """A Standard Notes Note object, used to define notes."""
    def __init__(self, title, text, guid=None):
        super().__init__(title=title, content_type='Note')
        self.text = text
        self.model['content']['text'] = self.text


class Package(object):
    """A Standard Notes file containing tags and notes."""
    def __init__(self):
        self.items = []
        self.model = {
            'items': self.items
        }

    def add(self, item):
        """Add a `Standard` based object to the package.

        :param item: a `Standard`-based object to add
        :returns: `None`

        """
        self.items.append(item.model)

    def json(self, *args, **kwargs):
        """Dump a JSON string of the package data model.

        :param *args: the positional arguments to pass to `json.dumps`
        :param **kwargs: the keyword arguments to pass to `json.dumps`
        :returns: the JSON string version of the object model

        """
        return json.dumps(self.model, *args, **kwargs)

    def write(self, filepath):
        """Dump the JSON version of the object to disk.

        :param *args: the positional arguments to pass to `json.dumps`
        :param **kwargs: the keyword arguments to pass to `json.dumps`
        :returns: None

        """
        with open(filepath, 'w') as outfile:
            json.dump(self.model, outfile, indent=4)
        return
