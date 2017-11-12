from textwrap import fill


def definitions(footnotes):
    """Convert JSON footnotes into a format suitable for Jinja2.

    In JSON a footnote is a list.
    The first element is the id.
    Other elements are either string or list, concatenated to make the text.
    A list is a grade (e.g. poor) followed by a string that will be rendered in
    a span with class="{{ grade }}".

    The definitions returned have numbers, ids and plain and rich text.

    The index returned is a map from id to index into definitions.
    """
    defs = []
    index = {}
    for i, footnote in enumerate(footnotes):
        id, *text = footnote
        defs.append({
            'number': i + 1,
            'id': id,
            'richtext': text,
            'tooltip': tooltip(text)})
        index[id] = i
    return defs, index


def tooltip(richtext, width=40):
    """Strip out rich formattting and fill to fixed width."""
    text = [item[1] if isinstance(item, list) else item
            for item in richtext]
    return fill(' '.join(text), width=width)
