

#%%
from pathlib import Path

from matlab_path import SearchPath

current_path = Path(__file__).parent
path = current_path / "workspace"

search_path = SearchPath([], dependency_analysis=True)
search_path.addpath(path, recursive=True)
search_path.resolve_dependencies()
#%%

f0 = search_path.resolve('function0')
f4 = search_path.resolve('function4')
c0 = search_path.resolve('class0')
c3 = search_path.resolve('class3')
p2 = search_path.resolve('package2')
p3 = search_path.resolve('package2.package3')
lf = search_path.resolve('privatefunction', local_namespaces=[p2.path.parent])
# %%


