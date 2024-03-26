from pathlib import Path
from matlab_path import SearchPath
import pytest

@pytest.fixture
def workspace():
    current_path = Path(__file__).parent.parent
    path = current_path / "test" / "workspace"
    search_path = SearchPath([], dependency_analysis=True)
    search_path.addpath(path, recursive=True)
    search_path.resolve_dependencies()
    return search_path


def test_wrong_class_folders(workspace: SearchPath):
    # Class folders expect: 
    #   - @my_class class folder expects a my_class.m
    #

    badclass = workspace.resolve("badclass")
    
    assert badclass is not None
    assert list(badclass.methods.keys()) == ['method1'] # type: ignore
