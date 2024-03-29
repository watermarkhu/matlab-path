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

def test_basic_resolve(workspace: SearchPath):
    # Check name and nodetype
    workspace_mapping = {
        "function0"     : "Function",
        "script0"       : "Script", 
        "class0"        : "Classdef",
        "class1"        : "Classdef",
        "package1"      : "Package"
    }

    for k, v in workspace_mapping.items():
        print(f"Verifying \'{k}\' ..")
        item = workspace.resolve(k)
        assert item is not None
        assert item.name == k
        assert item.nodetype == v



def test_hierarchy(workspace: SearchPath):
    # Verify hierarchy of packages/classes 
    workspace_mapping = [
        "package1.package3.package4.class7",
        "package1.class6",
    ]

    for item_name in workspace_mapping:
        print(f"Checking hierarchy with item \'{item_name}\' ..")
        assert workspace.resolve(item_name)
