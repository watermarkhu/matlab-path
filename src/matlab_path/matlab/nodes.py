from __future__ import annotations

from collections import OrderedDict
from pathlib import Path
from typing import TypedDict

from .attributes import ArgumentAttributes, ClassdefAttributes, MethodAttributes, PropertyAttributes


class Node(TypedDict, total=False):
    name: str
    path: Path
    parent: Node | None


class Script(Node, total=False):
    docstring: dict[int, str]


class Property(Script, total=False):
    type: str
    default: str
    size: list[str]
    validators: list[str]
    attributes: PropertyAttributes


class Argument(Script, total=False):
    type: str
    default: str
    size: list[str]
    validators: list[str]
    attributes: ArgumentAttributes


class Enum(Script, total=False):
    value: str


class Function(Script, total=False):
    input: OrderedDict[str, Argument]
    output: dict[str, Argument]
    options: OrderedDict[str, Argument]


class Method(Function, total=False):
    attributes: MethodAttributes


class Classdef(Script, total=False):
    isclassfolder: bool
    classname: str
    ancestors: list[str]
    enumeration: list[Enum]
    methods: dict[str, Method]
    properties: dict[str, Property]
    attributes: ClassdefAttributes


class Package(Script, total=False):
    classes: dict[str, Classdef]
    functions: dict[str, Function]


class LiveScript(Script, total=False): ...


class App(Script, total=False): ...


class Mex(Node, total=False): ...
