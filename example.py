
import logging
from pathlib import Path

from matlab_path import SearchPath

current_path = Path(__file__).resolve().parent
path = current_path.parent.parent / "foclev-matlab" / "leveling" / "IMO3" / "strokes_simulation" / "data" / "tests"
print(path, path.exists())

# from textmate_grammar.parsers.matlab import MatlabParser


# Enable debug logging
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger("textmate_grammar").setLevel(logging.ERROR)

# # Initialize language parser
# # parser = MatlabParser(remove_line_continuations=True)
# # element = parser.parse_file(path / "S3-CMA-ES"/ "GenerateBigPopulation.m")
# # print(element)

search_path = SearchPath([], dependency_analysis=True, show_progressbar=True)
search_path.addpath(path, recursive=True)
search_path.resolve_dependencies()
#%%
