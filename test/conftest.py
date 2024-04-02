from pathlib import Path

import pytest
from matlab_path import SearchPath


@pytest.fixture
def workspace():
    current_path = Path(__file__).parent
    path = current_path / "workspace"
    search_path = SearchPath([], dependency_analysis=True)
    search_path.addpath(path, recursive=True)
    search_path.resolve_dependencies()
    return search_path