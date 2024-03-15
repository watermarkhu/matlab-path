# MATLAB path

```matlab
from pathlib import Path
from matlab_path import SearchPath

path = Path("./test/workspace")

search_path = SearchPath([])
search_path.addpath(path, recursive=True)
```
