
from collections import defaultdict
from pathlib import Path



class SearchPath:

    indexed_extensions: list[str] = ['m', 'p', 'mlapp', 'mex', 'mexa64', 'mexmaci64', 'mexw32', 'mexw64']
    
    def __init__(self, matlab_path: list[str | Path]) -> None:

        for path in matlab_path:
            if not isinstance(path, (str, Path)):
                raise TypeError(f"Expected str or Path, got {type(path)}")
            
        self._search_path: list[Path] = []
        self._path_items: dict[Path, list[Path]] = defaultdict(list)
        self._namespace: dict[str, list[Path]] = defaultdict(list)
        self._database: dict[Path, object] = {}

        for path in matlab_path:
            self.addpath(Path(path), to_end=True)
    
    def addpath(self, path: str | Path, to_end: bool = False) -> list[Path]:

        old_path = [p for p in self._search_path]

        for item in path.iterdir():
            if item.is_file():
                self._path_items[path].append(item.name)
            else:
                self._path_items[path].extend(self._resolve_dir(item))

        return old_path
