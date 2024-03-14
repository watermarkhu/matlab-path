from __future__ import annotations

from collections import OrderedDict, TypedDict
from pathlib import Path


from .attributes import *

class Node(TypedDict, total=False):
    name: str
    path: Path
    parent: 'Node | None'

class Script(Node):
    docstring: dict[int, str]

class Property(Script):
    type: str
    default: str
    size: list[str]
    validators: list[str]
    attributes: PropertyAttributes

class Argument(Property):
    attributes: ArgumentAttributes

class Function(Script):
    input: OrderedDict[str, Property]
    output: dict[str, Property]
    options: OrderedDict[str, Property]

class Method(Function):
    attributes: MethodAttributes

class Classdef(Script):
    isclassfolder: bool
    ancestors: list[str]
    enumeration: dict[str, (str, str)]
    methods: dict[str, Method]
    properties: dict[str, Property]
    Attributes: ClassdefAttributes


class Package(Script):
    classes: dict[str, Classdef]
    functions: dict[str, Function]

class LiveScript(Script):
    pass

class App(Script):
    pass

class Mex(Node):
    pass




