import re
from typing import Dict, List, Union
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from falcano.expressions.operands import Path


PATH_SEGMENT_REGEX = re.compile(r'([^\[\]]+)((?:\[\d+\])*)$')


def get_path_segments(document_path: Union[str, 'Path', List[str]]) -> Union[List[str], List['Path']]:
    return document_path.split('.') if isinstance(document_path, str) else list(document_path)


def substitute_names(document_path: Union[str, 'Path'], placeholders: Dict[str, str]) -> str:
    """
    Replaces all attribute names in the given document path with placeholders.
    Stores the placeholders in the given dictionary.

    :param document_path: list of path segments (an attribute name and optional list dereference)
    :param placeholders:  a dictionary to store mappings from attribute names to expression attribute name placeholders

    For example: given the document_path for some attribute "baz", that is the first element of a list attribute "bar",
    that itself is a map element of "foo" (i.e. ['foo', 'bar[0], 'baz']) and an empty placeholders dictionary,
    `substitute_names` will return "#0.#1[0].#2" and placeholders will contain {"foo": "#0", "bar": "#1", "baz": "#2"}
    """
    path_segments = get_path_segments(document_path)
    for idx, segment in enumerate(path_segments):
        match = PATH_SEGMENT_REGEX.match(segment)
        if not match:
            raise ValueError('{} is not a valid document path'.format('.'.join(document_path)))
        name, indexes = match.groups()
        if name in placeholders:
            placeholder = placeholders[name]
        else:
            placeholder = '#' + str(len(placeholders))
            placeholders[name] = placeholder
        path_segments[idx] = placeholder + indexes
    return '.'.join(path_segments)


def get_value_placeholder(value: 'Path', expression_attribute_values: Dict[str, str]) -> str:
    placeholder = ':' + str(len(expression_attribute_values))
    expression_attribute_values[placeholder] = value
    return placeholder
