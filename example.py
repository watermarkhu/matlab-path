

#%%
from pathlib import Path

from matlab_path import SearchPath

current_path = Path(__file__).parent
path = current_path / "test" / "workspace"

search_path = SearchPath([], dependency_analysis=True)
search_path.addpath(path, recursive=True)
search_path.resolve_dependencies()
#%%

bf1 = search_path.resolve('basefunction1')
bc1 = search_path.resolve('baseclass1')
cc = search_path.resolve('classfoldercore')
fc = search_path.resolve('functioncore')
lf = search_path.resolve('baseprivatefunction', local_namespaces=[bc1.path.parent])
# %%


