

#%%
from pathlib import Path

from matlab_path import SearchPath

current_path = Path(__file__).parent
path = current_path / "workspace"

search_path = SearchPath()
search_path.addpath(path, recursive=True)

#%%