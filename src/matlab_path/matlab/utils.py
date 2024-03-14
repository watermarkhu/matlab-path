from textmate_grammar.elements import ContentElement


def append_comment(elem: ContentElement, docstring: dict[int, str]) -> dict[int, str]:
    """
    Append a comment from the given element to the docstring.

    Parameters:
        elem (ContentElement): The element containing the comment.
        docstring (dict[int, str]): The existing docstring.

    Returns:
        dict[int, str]: The updated docstring with the appended comment.
    """
    content = elem.content[elem.content.index("%") + 1 :]
    pos = list(elem.characters.keys())[0]
    docstring[pos[0]] = content
    return docstring


def append_section_comment(elem: ContentElement, docstring: dict[int, str]) -> dict[int, str]:
    """
    Appends a section comment to the given docstring.

    Args:
        elem (ContentElement): The content element containing the section comment.
        docstring (dict[int, str]): The existing docstring to append the section comment to.

    Returns:
        dict[int, str]: The updated docstring with the section comment appended.
    """
    content = elem.content[elem.content.index("%%") + 2 :]
    pos = list(elem.characters.keys())[0]
    docstring[pos[0]] = content
    return docstring


def append_block_comment(elem: ContentElement, docstring: dict[int, str]) -> dict[int, str]:
    """
    Appends the block comment from the given element to the docstring dictionary.

    Args:
        elem (ContentElement): The element containing the block comment.
        docstring (dict[int, str]): The dictionary to append the block comment to.

    Returns:
        dict[int, str]: The updated docstring dictionary.
    """
    bracket = elem.content.index("%{") + 2
    begin = elem.content[bracket:].index("\n") + bracket + 1
    content = elem.content[begin : elem.content.index("%}")]
    pos = list(elem.characters.keys())[0]
    index = pos[0] + 1
    for i, line in enumerate(content.split("\n")):
        docstring[index + i] = line
    return docstring


def fix_indentation(docstring: dict[int, str]) -> dict[int, str]:
    """
    Fixes the indentation of a multi-line docstring.

    Args:
        docstring (dict[int, str]): A dictionary representing the lines of the docstring.

    Returns:
        str: The fixed docstring with correct indentation.

    """
    if not docstring:
        return {}
    padding = [len(line) - len(line.lstrip()) for line in docstring.values()]
    indent = min(
        [pad for pad, line in zip(padding, docstring.values()) if not (line.isspace() or not line)]
    )

    for (i, line), pad in zip(docstring.items(), padding):
        docstring[i] = line[indent:].rstrip() if len(line) >= pad else line.rstrip()
    return docstring
