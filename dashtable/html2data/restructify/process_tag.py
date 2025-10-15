from bs4 import NavigableString

from .converters import *

def truncate_empties(lines):
    while lines[0].rstrip() == '':
        lines.pop(0)
    while lines[len(lines) - 1].rstrip() == '':
        lines.pop(-1)
    return lines


def clean_text(text):
    """
    Remove problematic Unicode characters that cause alignment issues.
    
    Removes:
    - U+200B: Zero-Width Space
    - U+200C: Zero-Width Non-Joiner
    - U+200D: Zero-Width Joiner  
    - U+FEFF: Zero-Width No-Break Space (BOM)
    """
    # Remove zero-width spaces and similar characters
    text = text.replace('\u200b', '')  # Zero-Width Space
    text = text.replace('\u200c', '')  # Zero-Width Non-Joiner
    text = text.replace('\u200d', '')  # Zero-Width Joiner
    text = text.replace('\ufeff', '')  # Zero-Width No-Break Space
    return text


def process_tag(node):
    """
    Recursively go through a tag's children, converting them, then
    convert the tag itself.

    """
    text = ''

    exceptions = ['table']

    for element in node.children:
        if isinstance(element, NavigableString):
            text += clean_text(str(element))
        elif not node.name in exceptions:
            text += process_tag(element)

    try:
        convert_fn = globals()["convert_%s" % node.name.lower()]
        text = convert_fn(node, text)

    except KeyError:
        pass

    return text
