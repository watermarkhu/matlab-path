import pytest
from matlab_path import SearchPath
from matlab_path.matlab import nodes as n

workspace_mapping = {
    "function0"     : n.Function,
    "script0"       : n.Script, 
    "class0"        : n.Classdef,
    "class1"        : n.Classdef,
    "package1"      : n.Package
}


@pytest.mark.parametrize("name,nodetype", workspace_mapping.items())
def test_basic_resolve(workspace: SearchPath, name: str, nodetype: n.Node):
    # Check name and nodetype
    item = workspace.resolve(name)
    assert item is not None
    assert item.name == name
    assert isinstance(item, nodetype)



def test_hierarchy(workspace: SearchPath):
    # Verify hierarchy of packages/classes 
    workspace_mapping = [
        "package1.package3.package4.class7",
        "package1.class6",
    ]

    for item_name in workspace_mapping:
        print(f"Checking hierarchy with item \'{item_name}\' ..")
        assert workspace.resolve(item_name)
