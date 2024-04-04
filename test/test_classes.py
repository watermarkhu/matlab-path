from matlab_path import SearchPath


def test_class_resolve(workspace: SearchPath):
    target_class_names = [ 
        "myclass",
        "packagebase.pbclass",
        "packagebase.subpackagebase.pbsclass"
    ]

    for class_name in target_class_names:
        target_class = workspace.resolve(class_name)
        assert target_class is not None
        assert target_class.fqdm == class_name
        assert target_class.nodetype == "Classdef"


def test_class_folder_resolve(workspace: SearchPath):
    target_class_names = [ 
        "classfoldercore",
        "packagecore.pclassfoldercore",
        "packagecore.subpackagecore.spcclass"
    ]

    for class_name in target_class_names:
        target_class = workspace.resolve(class_name)
        assert target_class is not None
        assert target_class.fqdm == class_name
        assert target_class.nodetype == "Classdef"

def test_class_methods(workspace: SearchPath):
    target_class_names = [ 
        "myclass", 
        "packagecore.pclassfoldercore"
    ]


    target_methods = {
        "myclass" : [
            "myclass",
            "my_method_0",
            "my_method_2"
        ],

        "packagecore.pclassfoldercore" : [
            "pclassfoldercore",
            "another_method",
            "another_method_1"            
        ]
    }

    # check that each class has methods in target_methods
    for class_name in target_class_names:
        target_class = workspace.resolve(class_name)
        assert target_methods[class_name] == list(target_class.methods.keys())  # type: ignore




#     for class_name in target_class_names:
#         target_class = 


# def test_class_properties(workspace: SearchPath):
#     pass 


# def test_class_hierarchy(workspace: SearchPath):
#     pass