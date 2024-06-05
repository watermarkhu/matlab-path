

#%%
from pathlib import Path

from matlab_path import SearchPath

current_path = Path(__file__).parent
path = current_path / "test" / "PlatEMO" / "PlatEMO"

search_path = SearchPath([], dependency_analysis=True, show_progressbar=True)
search_path.addpath(path, recursive=True)
search_path.resolve_dependencies()
#%%
