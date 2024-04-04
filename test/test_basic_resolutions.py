import pytest
from matlab_path import SearchPath
from matlab_path.matlab import nodes as n

workspace_mapping = {
    "myfunction"     : n.Function,
    "myscript"       : n.Script, 
    "myclass"        : n.Classdef,
    "classfoldercore": n.Classdef,
    "packagecore"       : n.Package
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
        "packagecore.subpackagecore.subsubpackagecore.sspcclass",
        "packagecore.pclassfoldercore",
    ]

    for item_name in workspace_mapping:
        print(f"Checking hierarchy with item \'{item_name}\' ..")
        assert workspace.resolve(item_name)
