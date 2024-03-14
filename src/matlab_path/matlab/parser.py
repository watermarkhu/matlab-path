from __future__ import annotations

from collections import OrderedDict
from typing import Protocol
from pathlib import Path

import texmate_grammar as tm
from textmate_grammar.elements import ContentBlockElement, ContentElement

from .nodes import *
from .utils import append_block_comment, append_comment, append_section_comment, fix_indentation

tm.utils.cache.init_cache("shelve")
TM_PARSER = tm.language.LanguageParser(tm.grammars.matlab)


def get_node(item: Path, parent: Node | None = None) -> Node:

    if item.is_file():
        name = _resolve_name(item.stem, parent)
        if item.suffix == ".m":
            element = TM_PARSER.parse_file(item)

            try:
                next(element.find("meta.class.matlab", depth=1))[0]
                parser = _parse_m_classdef
            except StopIteration:
                generator = element.find(
                    [
                        "comment.line.percentage.matlab",
                        "comment.block.percentage.matlab",
                        "comment.line.double-percentage.matlab",
                        "meta.function.matlab",
                    ],
                    stop_tokens="*",
                    depth=1,
                )
                for item, _ in generator:
                    if item.token == "meta.function.matlab":
                        parser = _parse_m_function
                        break
                else:
                    parser = _parse_m_script

            return parser(item, element)
            
        elif item.suffix == ".p":
            # TODO get docstring from .m helper file
            return Node(name=name, path=item, parent=parent)
        elif item.suffix == ".mlx":
            # TODO get docstring
            return LiveScript(name=name, path=item, parent=None)
        elif item.suffix == ".mlapp":
            # TODO get docstring
            return App(name=name, path=item, parent=None)
        elif item.suffix in [".mex", ".mexa64", ".mexmaci64", ".mexw32", ".mexw64"]:
            return Mex(name=name, path=item, parent=None)
        
    elif item.is_dir():
        name = _resolve_name(item.stem[1:], parent)
        if item.stem[0] == "+":
            # TODO get items of package
            # TODO get docstring from contents.m
            return Package(name=item.stem, path=item, parent=parent)
        elif item.stem[0] == "@":
            # TODO get items of class folder
            # TODO get docstring from contents.m
            return Classdef(name=item.stem, path=item, parent=parent, isclassfolder=True)


_COMMENT_TOKENS = [
    "comment.line.percentage.matlab",
    "comment.block.percentage.matlab",
    "comment.line.double-percentage.matlab",
]

def _resolve_name(name: str, parent: Node | None) -> str:
    while parent:
        name = f"{parent.name}.{name}"
        parent = parent.parent
    return name

def _get_offset(element: ContentElement) -> int:
    first_charater_position = next(iter(element.characters))
    return first_charater_position[0]


def _validate_token(element: ContentElement, token: str) -> None:
    if element.token != token:
        raise ValueError


def _parse_m_script(file: Path, element: ContentBlockElement) -> Script:

    docstring: dict[int, str] = {}
    for function_item, _ in element.find(_COMMENT_TOKENS, stop_tokens="*", depth=1):
        if function_item.token == "comment.line.percentage.matlab":
            append_comment(function_item, docstring)
        elif function_item.token == "comment.line.double-percentage.matlab":
            append_section_comment(function_item, docstring)
        else:
            # Block comments will take precedence over single % comments
            append_block_comment(function_item, docstring)
            break
    fix_indentation(docstring)
    return Script(name=file.stem, path=file, parent=None, docstring=docstring)


def _parse_m_function(file: Path, element: ContentBlockElement, parent: Node | None = None) -> Function:

    _validate_token(element, "meta.function.matlab")
    name = _resolve_name(file.stem, parent)
    node = Function(name=name, path=file, parent=parent)
    _common_function_method(node, element, parent)


def _parse_method(
    parent: Classdef, 
    element: ContentBlockElement, 
    attributes: MethodAttributes) -> Method:

    _validate_token(element, "meta.function.matlab")
    declaration = next(element.find("meta.function.declaration.matlab", depth=1))[0]
    local_name = next(declaration.find("entity.name.function.matlab"))[0].content
    name = _resolve_name(local_name, parent)
    node = Method(name=name, element=element, attributes=attributes, parent=parent)
    _common_function_method(node, element, parent)


def _common_function_method(node: Function | Method, element: ContentBlockElement, parent: Node | None = None) -> Function:

    def _add_argument(
        arg_item: ContentBlockElement,
        attributes: ArgumentAttributes,
        docstring_lines: list[str],
    ):
        arg = Property(arg_item, attributes=attributes, docstring_lines=docstring_lines)

        if attributes.Output:
            node.output[arg.name] = arg
        else:
            if "." in arg.name:
                node.input.pop(arg.name.split(".")[0], None)
                arg.name = arg.name.split(".")[1]
                node.options[arg.name] = arg
            else:
                node.input[arg.name] = arg

    for function_item, _ in element.find(
        ["meta.function.declaration.matlab", "meta.arguments.matlab"] + _COMMENT_TOKENS,
        depth=1,
    ):
        if function_item.token == "meta.function.declaration.matlab":
            # Get input and output arguments from function declaration

            for variable, _ in function_item.find(
                ["variable.parameter.output.matlab","variable.parameter.input.matlab"]
            ):
                if variable.token == "variable.parameter.input.matlab":
                    node["input"][variable.content] = Argument(variable.content, parent=node)
                else:
                    node["output"][variable.content] = Argument(variable.content, parent=node)

        elif function_item.token == "comment.block.percentage.matlab":
            docstring_lines = append_block_comment(function_item)

        elif function_item.token == "comment.line.percentage.matlab":
            append_comment(function_item, docstring_lines)

        elif function_item.token == "comment.line.double-percentage.matlab":
            append_section_comment(function_item, docstring_lines)

        else:  # meta.arguments.matlab
            modifiers = {
                m.content: True
                for m, _ in function_item.findall(
                    "storage.modifier.arguments.matlab", attribute="begin"
                )
            }
            attributes = ArgumentAttributes(**modifiers)

            arg = None
            arg_doc_parts: list[str] = []

            for arg_item, _ in function_item.find(
                [
                    "meta.assignment.definition.property.matlab",
                    "comment.line.percentage.matlab",
                ],
                depth=1,
            ):
                if arg_item.token == "meta.assignment.definition.property.matlab":
                    if arg:
                        _add_argument(arg, attributes, arg_doc_parts)

                    arg_doc_parts = []
                    arg = arg_item
                else:
                    arg_doc_parts.append(arg_item.content[arg_item.content.index("%") + 1 :])
            else:
                if arg:
                    _add_argument(arg, attributes, arg_doc_parts)
                    arg_doc_parts = []

    self._doc = parse_comment_docstring(docstring_lines)

def _parse_m_classdef(file: Path, element: ContentBlockElement) -> Classdef:
    pass


def _common_property_argument(
    node: Property | Argument,
    element: ContentBlockElement, 
    docstring: dict[int, str] = {}):

    if element.end:
        default_elements = element.findall(
            "*",
            stop_tokens=_COMMENT_TOKENS,
            attribute="end",
            depth=1,
        )
        if (
            default_elements
            and default_elements[0][0].token == "keyword.operator.assignment.matlab"
        ):
            node["default"] = "".join([el.content for el, _ in default_elements[1:]])

        doc_elements = element.findall("comment.line.percentage.matlab", attribute="end")

        for el, _ in doc_elements:
            index = next(el.charaters.keys())[0]
            docstring[index] = el.content[1:]

    node["docstring"] = fix_indentation(docstring)

    for expression, _ in element.find(
        [
            "storage.type.matlab",
            "meta.parens.size.matlab",
            "meta.block.validation.matlab",
        ],
        depth=1,
    ):
        if expression.token == "storage.type.matlab":
            node["type"] = expression.content
        elif expression.token == "meta.parens.size.matlab":
            node["size"] = expression.content.split(",")
        else:
            node["validators"] = [validator.content for validator in expression.children]

    return node


def _parse_argument(
    node: Argument, 
    element: ContentBlockElement, 
    attributes: ArgumentAttributes = ArgumentAttributes(), 
    docstring: dict[int, str] = {}) -> Argument:

    _validate_token(element, "meta.assignment.definition.property.matlab")
    name = _resolve_name(element.begin[0].content, parent)
    node = Argument(name=name, parent=parent)
    node["attributes"] = attributes
    _common_property_argument(node, element, docstring)
    return node


def _parse_property(
    parent: Classdef, 
    element: ContentBlockElement, 
    attributes: PropertyAttributes, 
    docstring: dict[int, str] = {}) -> Property:

    _validate_token(element, "meta.assignment.definition.property.matlab")
    name = _resolve_name(element.begin[0].content, parent)
    node = Property(name=name, parent=parent)
    node["attributes"] = attributes
    _common_property_argument(node, element, docstring)
    return node







class Method(Function):
    def __init__(
        self, element: ContentBlockElement, attributes: MethodAttributes, classdef: "Classdef"
    ):
        self.validate_token(element)
        self.element = element
        self.attributes = attributes
        self.classdef = classdef
        self._process_elements(element)

        if self.local_name != classdef.local_name or not attributes.Static:
            self.input.popitem(last=False)


class Classdef(MatObject):
    _textmate_token = "meta.class.matlab"

    def __init__(self, node: NamespaceNode) -> None:
        self.validate_token(node._element)
        self.node = node
        self.offset = 0

        self.local_name: str = ""
        self.ancestors: list[str] = []
        self.enumeration: dict[str, (str, str)] = dict()
        self.methods: dict[str, Method] = dict()
        self.properties: dict[str, Property] = dict()

        docstring_lines: list[str] = []

        for class_item, _ in node._element.find(
            [
                "meta.class.declaration.matlab",
                "meta.properties.matlab",
                "meta.enum.matlab",
                "meta.methods.matlab",
            ]
            + _COMMENT_TOKENS,
            depth=1,
        ):
            if class_item.token == "meta.class.declaration.matlab":
                modifiers = {}
                current_modifier, current_value = "", True

                for attribute_item, _ in class_item.find(
                    "*",
                    start_tokens="punctuation.section.parens.begin.matlab",
                    stop_tokens="punctuation.section.parens.end.matlab",
                    depth=1,
                ):
                    if attribute_item.token == "punctuation.section.parens.begin.matlab":
                        continue
                    elif attribute_item.token == "storage.modifier.class.matlab":
                        current_modifier = attribute_item.content
                    elif attribute_item.token == "keyword.operator.assignment.matlab":
                        current_value = ""
                    elif attribute_item.token == "punctuation.separator.modifier.comma.matlab":
                        modifiers[current_modifier], current_value = current_value, True
                    elif attribute_item.token not in _COMMENT_TOKENS:
                        current_value += attribute_item.content
                else:
                    if current_modifier:
                        modifiers[current_modifier] = current_value

                self._attributes = ClassdefAttributes.from_dict(modifiers)

                declation_tokens = [
                    "entity.name.type.class.matlab",
                    "meta.inherited-class.matlab",
                    "punctuation.definition.comment.matlab",
                ]

                for declation_item, _ in class_item.find(
                    declation_tokens, start_tokens=declation_tokens, depth=1
                ):
                    if declation_item.token == "entity.name.type.class.matlab":
                        self.local_name = declation_item.content
                    elif declation_item.token == "meta.inherited-class.matlab":
                        self.ancestors.append(declation_item.content)
                    elif declation_item.token == "punctuation.definition.comment.matlab":
                        docstring_lines.append(
                            class_item.content[class_item.content.index("%") + 1 :]
                        )
            elif class_item.token == "comment.block.percentage.matlab":
                docstring_lines = append_block_comment(class_item)

            elif class_item.token == "comment.line.percentage.matlab":
                append_comment(class_item, docstring_lines)

            elif class_item.token == "comment.line.double-percentage.matlab":
                append_section_comment(class_item, docstring_lines)

            elif class_item.token == "meta.properties.matlab":
                modifiers = {}
                current_modifier, current_value = "", True
                for modifier_item, _ in class_item.findall(
                    "*", start_tokens="storage.modifier.properties.matlab", attribute="begin"
                ):
                    if modifier_item.token == "storage.modifier.properties.matlab":
                        if current_modifier:
                            modifiers[current_modifier], current_value = current_value, True
                        current_modifier = modifier_item.content
                    elif modifier_item.token == "keyword.operator.assignment.matlab":
                        current_value = ""
                    elif modifier_item.token not in _COMMENT_TOKENS:
                        current_value += modifier_item.content
                else:
                    if current_modifier:
                        modifiers[current_modifier] = current_value

                attributes = PropertyAttributes.from_dict(modifiers)

                prop = None
                prop_doc_parts: list[str] = []
                for prop_item, _ in class_item.find(
                    [
                        "meta.assignment.definition.property.matlab",
                        "comment.line.percentage.matlab",
                    ],
                    depth=1,
                ):
                    if prop_item.token == "meta.assignment.definition.property.matlab":
                        if prop:
                            self._add_prop(prop, attributes, prop_doc_parts)

                        prop_doc_parts = []
                        prop = prop_item
                    else:
                        prop_doc_parts.append(prop_item.content[prop_item.content.index("%") + 1 :])
                else:
                    if prop:
                        self._add_prop(prop, attributes, prop_doc_parts)
                        prop_doc_parts = []

            elif class_item.token == "meta.enum.matlab":
                enum_doc_parts: list[str] = []
                enum_name: str = ""
                enum_value: str = ""
                for enum_item, _ in class_item.find(
                    [
                        "meta.assignment.definition.enummember.matlab",
                        "meta.parens.matlab",
                        "comment.line.percentage.matlab",
                    ],
                    attribute="children",
                ):
                    if enum_item.token == "meta.assignment.definition.enummember.matlab":
                        if enum_name:
                            enum_doc = parse_comment_docstring(enum_doc_parts)
                            self.enumeration[enum_name] = (enum_value, enum_doc)
                            enum_doc_parts, enum_value = [], ""
                        enum_name = next(enum_item.find("variable.other.enummember.matlab"))[
                            0
                        ].content

                    elif enum_item.token == "meta.parens.matlab":
                        enum_value = enum_item.content
                    else:
                        append_comment(enum_item, enum_doc_parts)
                else:
                    if enum_name:
                        enum_doc = parse_comment_docstring(enum_doc_parts)
                        self.enumeration[enum_name] = (enum_value, enum_doc)
                        enum_doc_parts, enum_value = [], ""

            else:
                modifiers = {}
                current_modifier, current_value = "", True
                for modifier_item, _ in class_item.findall(
                    ["storage.modifier.methods.matlab", "storage.modifier.access.matlab"],
                    attribute="begin",
                ):
                    if modifier_item.token == "storage.modifier.methods.matlab":
                        if current_modifier:
                            modifiers[current_modifier], current_value = current_value, True
                        current_modifier = modifier_item.content
                    else:
                        current_value = modifier_item.content
                else:
                    if current_modifier:
                        modifiers[current_modifier] = current_value

                attributes = MethodAttributes.from_dict(modifiers)

                for method_item, _ in class_item.find("meta.function.matlab", depth=1):
                    method = Method(method_item, attributes, self)
                    self.methods[method.local_name] = method

        self._doc = parse_comment_docstring(docstring_lines)

    def _add_prop(
        self,
        prop_item: ContentBlockElement,
        attributes: ArgumentAttributes | PropertyAttributes,
        docstring_lines: list[str],
    ):
        prop = Property(prop_item, attributes=attributes, docstring_lines=docstring_lines)
        self.properties[prop.name] = prop

    def doc(self, config: Config) -> str:
        docstring = self._doc
        if config.class_docstring == "merge" and self.local_name in self.methods:
            constructor_docstring = self.methods[self.local_name].doc(config)
            if docstring and constructor_docstring:
                docstring += "\n\n"
            docstring += constructor_docstring

        if self.enumeration:
            docstring = append_enum_table(
                self.enumeration, docstring, renderer=config.render_plugin
            )

        if config.class_properties_table:
            public_properties = {
                name: prop
                for (name, prop) in self.properties.items()
                if prop._attributes.Access == "public" or prop._attributes.GetAccess == "public"
            }
            if public_properties:
                docstring = append_validation_table(
                    public_properties, docstring, renderer=config.render_plugin, title="Properties"
                )

        return docstring