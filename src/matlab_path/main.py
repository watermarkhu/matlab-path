from collections import defaultdict, deque
from pathlib import Path

from .matlab.nodes import Node
from .matlab.parser import get_node


class SearchPath:
    """
    Represents a search path for MATLAB paths.

    Attributes:
        _search_path (deque[Path]): A deque of Path objects representing the search path.
        _path_members (dict[Path, list[tuple[str, Path]]]): A dictionary mapping each path to a list of tuples containing the name and member Path objects.
        _namespace (dict[str, deque[Path]]): A dictionary mapping each name to a deque of member Path objects.
        _database (dict[Path, Node]): A dictionary mapping each member Path object to its corresponding Node object.

    """

    def __init__(self, matlab_path: list[str | Path]) -> None:
        """
        Initialize an instance of MyClass.

        Args:
            matlab_path (list[str | Path]): A list of strings or Path objects representing the MATLAB paths.

        Raises:
            TypeError: If any element in matlab_path is not a string or Path object.

        """
        for path in matlab_path:
            if not isinstance(path, (str, Path)):
                raise TypeError(f"Expected str or Path, got {type(path)}")

        self._search_path: deque[Path] = deque()
        self._path_members: dict[Path, list[tuple[str, Path]]] = defaultdict(list)
        self._namespace: dict[str, deque[Path]] = defaultdict(deque)
        self._database: dict[Path, Node] = {}

        for path in matlab_path:
            self.addpath(Path(path), to_end=True)

    def resolve(self, name: str) -> Node | None:
        """
        Resolves the given name to a Node object.

        Args:
            name (str): The name to resolve.

        Returns:
            Node | None: The resolved Node object, or None if the name is not found.
        """
        if name in self._namespace:
            return self._database[self._namespace[name][0]]
        return None

    def addpath(
        self, path: str | Path, to_end: bool = False, recursive: bool = False
    ) -> list[Path]:
        """
        Add a path to the search path.

        Args:
            path (str | Path): The path to be added.
            to_end (bool, optional): Whether to add the path to the end of the search path. Defaults to False.

        Returns:
            list[Path]: The previous search path before adding the new path.
        """
        if isinstance(path, str):
            path = Path(path)

        old_path = [p for p in self._search_path]

        if path in self._search_path:
            self._search_path.remove(path)

        if to_end:
            self._search_path.append(path)
        else:
            self._search_path.appendleft(path)

        for member in path.iterdir():
            if recursive and member.is_dir() and member.stem[0] not in ["+", "@"]:
                self.addpath(member, to_end=to_end, recursive=True)
                continue

            node = get_node(member)
            if node is None:
                continue
            self._path_members[path].append((node.fqdm, member))
            self._database[member] = node
            if to_end:
                self._namespace[node.fqdm].append(member)
            else:
                self._namespace[node.fqdm].appendleft(member)

        return old_path

    def rm_path(self, path: str | Path, recursive: bool = False) -> list[Path]:
        """
        Removes a path from the search path and updates the namespace and database accordingly.

        Args:
            path (str | Path): The path to be removed from the search path.
            recursive (bool, optional): If True, recursively removes all subdirectories of the given path from the search path. Defaults to False.

        Returns:
            list[Path]: The previous search path before the removal.

        """
        if isinstance(path, str):
            path = Path(path)

        if path not in self._search_path:
            return list(self._search_path)

        old_path = [p for p in self._search_path]

        self._search_path.remove(path)

        for name, member in self._path_members.pop(path):
            self._namespace[name].remove(member)
            self._database.pop(member)

        if recursive:
            for subdir in [item for item in self._search_path if _is_subdirectory(path, item)]:
                self.rm_path(subdir, recursive=False)

        return old_path


def _is_subdirectory(parent_path: Path, child_path: Path) -> bool:
    try:
        child_path.relative_to(parent_path)
    except ValueError:
        return False
    else:
        return True
