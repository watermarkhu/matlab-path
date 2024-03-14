from __future__ import annotations

from collections import OrderedDict, TypedDict
from pathlib import Path

from .attributes import ArgumentAttributes, ClassdefAttributes, MethodAttributes, PropertyAttributes


class Node(TypedDict, total=False):
    name: str
    path: Path
    parent: Node | None = None


class Script(Node):
    docstring: dict[int, str] = {}


class Property(Script):
    type: str = ""
    default: str = ""
    size: list[str] = []
    validators: list[str] = []
    attributes: PropertyAttributes = PropertyAttributes()


class Argument(Property):
    attributes: ArgumentAttributes = ArgumentAttributes()


class Function(Script):
    input: OrderedDict[str, Property] = OrderedDict()
    output: dict[str, Property] = {}
    options: OrderedDict[str, Property] = OrderedDict


class Method(Function):
    attributes: MethodAttributes = MethodAttributes()


class Classdef(Script):
    isclassfolder: bool = False
    classname: str = ""
    ancestors: list[str] = []
    enumeration: dict[str, (str, str)] = {}
    methods: dict[str, Method] = {}
    properties: dict[str, Property] = {}
    Attributes: ClassdefAttributes = ClassdefAttributes()


class Package(Script):
    classes: dict[str, Classdef]
    functions: dict[str, Function]


class LiveScript(Script):
    pass


class App(Script):
    pass


class Mex(Node):
    pass
