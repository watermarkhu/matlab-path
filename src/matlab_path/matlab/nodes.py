from __future__ import annotations

from collections import OrderedDict
from dataclasses import dataclass, field
from pathlib import Path

from .attributes import ArgumentAttributes, ClassdefAttributes, MethodAttributes, PropertyAttributes


@dataclass(repr=False)
class Node:
    name: str
    path: Path
    parent: Node | None = None

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name}: path={self.path})"


@dataclass(repr=False)
class Script(Node):
    fqdm: str = ""
    docstring: dict[int, str] = field(default_factory=dict)


@dataclass(repr=False)
class Property(Node):
    type: str = ""
    default: str = ""
    size: list[str] = field(default_factory=list)
    validators: list[str] = field(default_factory=list)
    attributes: PropertyAttributes = field(default_factory=PropertyAttributes)
    docstring: dict[int, str] = field(default_factory=dict)


@dataclass(repr=False)
class Argument(Node):
    type: str = ""
    default: str = ""
    size: list[str] = field(default_factory=list)
    validators: list[str] = field(default_factory=list)
    attributes: ArgumentAttributes = field(default_factory=ArgumentAttributes)
    docstring: dict[int, str] = field(default_factory=dict)


@dataclass(repr=False)
class Enum(Node):
    value: str = ""
    docstring: dict[int, str] = field(default_factory=dict)


@dataclass(repr=False)
class Function(Script):
    input: OrderedDict[str, Argument] = field(default_factory=OrderedDict)
    output: OrderedDict[str, Argument] = field(default_factory=OrderedDict)
    options: dict[str, Argument] = field(default_factory=dict)


@dataclass(repr=False)
class Method(Function):
    attributes: MethodAttributes = field(default_factory=MethodAttributes)


@dataclass(repr=False)
class Classdef(Script):
    isclassfolder: bool = False
    ancestors: list[str] = field(default_factory=list)
    enumeration: list[Enum] = field(default_factory=list)
    methods: dict[str, Method] = field(default_factory=dict)
    properties: dict[str, Property] = field(default_factory=dict)
    attributes: ClassdefAttributes = field(default_factory=ClassdefAttributes)


@dataclass(repr=False)
class Package(Script):
    classes: list[Classdef] = field(default_factory=list)
    functions: list[Function] = field(default_factory=list)
    packages: list[Package] = field(default_factory=list)


@dataclass(repr=False)
class LiveScript(Script): ...


@dataclass(repr=False)
class App(Script): ...


@dataclass(repr=False)
class Mex(Script): ...
