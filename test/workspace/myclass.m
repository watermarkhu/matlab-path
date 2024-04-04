classdef myclass < matlab.unittest.TestCase & char
    properties
        Property1 (1,1) class4
        Property2 (1,1) double {mustBeNumeric, mustBePositive} = functioncore(0, 1)
    end

    methods
        function obj = myclass(inputArg1)
            obj = myfunction(inputArg1);
        end

        function obj = my_method_0(obj, arg1)

        end

        function obj = my_method_2(obj, arg1)

        end        
    end
end