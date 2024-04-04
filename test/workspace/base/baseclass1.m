classdef baseclass1
    properties
        radius
    end
    
    methods
        function obj = baseclass1(radius)
            obj.radius = radius;
        end
        
        function area = calculateArea(obj)
            area = pi * obj.radius^2;
        end
        
        function circumference = calculateCircumference(obj)
            circumference = 2 * pi * obj.radius;
        end
    end
end