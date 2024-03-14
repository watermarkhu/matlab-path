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
class Script(Node):
    fqdm: str = ""
    docstring: dict[int, str] = field(default_factory=dict)


@dataclass
class Property(Node):
    type: str = ""
    default: str = ""
    size: list[str] = field(default_factory=list)
    validators: list[str] = field(default_factory=list)
    attributes: PropertyAttributes = field(default_factory=PropertyAttributes)
    docstring: dict[int, str] = field(default_factory=dict)


@dataclass
class Argument(Node):
    type: str = ""
    default: str = ""
    size: list[str] = field(default_factory=list)
    validators: list[str] = field(default_factory=list)
    attributes: ArgumentAttributes = field(default_factory=ArgumentAttributes)
    docstring: dict[int, str] = field(default_factory=dict)


@dataclass
class Enum(Node):
    value: str = ""
    docstring: dict[int, str] = field(default_factory=dict)


@dataclass
class Function(Script):
    input: OrderedDict[str, Argument] = field(default_factory=OrderedDict)
    output: OrderedDict[str, Argument] = field(default_factory=OrderedDict)
    options: dict[str, Argument] = field(default_factory=dict)


@dataclass
class Method(Function):
    attributes: MethodAttributes = field(default_factory=MethodAttributes)


@dataclass
class Classdef(Script):
    isclassfolder: bool = False
    ancestors: list[str] = field(default_factory=list)
    enumeration: list[Enum] = field(default_factory=list)
    methods: dict[str, Method] = field(default_factory=dict)
    properties: dict[str, Property] = field(default_factory=dict)
    attributes: ClassdefAttributes = field(default_factory=ClassdefAttributes)


@dataclass
class Package(Script):
    classes: list[Classdef] = field(default_factory=list)
    functions: list[Function] = field(default_factory=list)
    packages: list[Package] = field(default_factory=list)


@dataclass
class LiveScript(Script): ...


@dataclass
class App(Script): ...


@dataclass
class Mex(Script): ...
