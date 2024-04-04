classdef pbclass
    properties
        a
        b
    end
    methods
        function obj = pbclass(a,b)
            obj.a = a;
            obj.b = b;
        end
        function c = add(obj)
            c = obj.a + obj.b;
        end
    end
end