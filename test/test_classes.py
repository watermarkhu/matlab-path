from matlab_path import SearchPath


def test_class_resolve(workspace: SearchPath):
    target_class_names = [ 
        "class0",
        "package2.class00",
        "package2.package3.class00"
    ]

    for class_name in target_class_names:
        target_class = workspace.resolve(class_name)
        assert target_class is not None
        assert target_class.fqdm == class_name
        assert target_class.nodetype == "Classdef"


def test_class_folder_resolve(workspace: SearchPath):
    target_class_names = [ 
        "class1",
        "package1.class6",
        "package1.package3.class8"
    ]

    for class_name in target_class_names:
        target_class = workspace.resolve(class_name)
        assert target_class is not None
        assert target_class.fqdm == class_name
        assert target_class.nodetype == "Classdef"

def test_class_methods(workspace: SearchPath):
    target_class_names = [ 
        "class0", 
        "package1.class6"
    ]


    target_methods = {
        "class0" : [
            "class0",
            "my_method_0",
            "my_method_2"
        ],

        "package1.class6" : [
            "class6",
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