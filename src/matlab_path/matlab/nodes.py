from __future__ import annotations

from collections import OrderedDict
from dataclasses import dataclass, field
from pathlib import Path

from .attributes import ArgumentAttributes, ClassdefAttributes, MethodAttributes, PropertyAttributes


@dataclass
class Node:
    name: str
    path: Path
    parent: Node | None = None


@dataclass
class PathItem(Node):
    fqdm: str = ""


@dataclass
class Script(Node):
    docstring: dict[int, str] = field(default_factory=dict)


@dataclass
class Property(Script):
    type: str = ""
    default: str = ""
    size: list[str] = field(default_factory=list)
    validators: list[str] = field(default_factory=list)
    attributes: PropertyAttributes = field(default_factory=PropertyAttributes)


@dataclass
class Argument(Script):
    type: str = ""
    default: str = ""
    size: list[str] = field(default_factory=list)
    validators: list[str] = field(default_factory=list)
    attributes: ArgumentAttributes = field(default_factory=ArgumentAttributes)


@dataclass
class Enum(Script):
    value: str = ""


@dataclass
class Function(Script, PathItem):
    input: OrderedDict[str, Argument] = field(default_factory=OrderedDict)
    output: OrderedDict[str, Argument] = field(default_factory=OrderedDict)
    options: dict[str, Argument] = field(default_factory=dict)


@dataclass
class Method(Function, PathItem):
    attributes: MethodAttributes = field(default_factory=MethodAttributes)


@dataclass
class Classdef(Script, PathItem):
    isclassfolder: bool = False
    ancestors: list[str] = field(default_factory=list)
    enumeration: list[Enum] = field(default_factory=list)
    methods: dict[str, Method] = field(default_factory=dict)
    properties: dict[str, Property] = field(default_factory=dict)
    attributes: ClassdefAttributes = field(default_factory=ClassdefAttributes)


@dataclass
class Package(Script, PathItem):
    classes: list[Classdef] = field(default_factory=list)
    functions: list[Function] = field(default_factory=list)
    packages: list[Package] = field(default_factory=list)


@dataclass
class LiveScript(Script, PathItem): ...


@dataclass
class App(Script, PathItem): ...


@dataclass
class Mex(PathItem): ...
