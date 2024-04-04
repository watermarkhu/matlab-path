from matlab_path import SearchPath


def test_wrong_class_folders(workspace: SearchPath):
    # Class folders expect: 
    #   - @my_class class folder expects a my_class.m
    #

    badclass = workspace.resolve("badclassfolder")
    
    assert badclass is not None
    assert list(badclass.methods.keys()) == ['method1'] # type: ignore
