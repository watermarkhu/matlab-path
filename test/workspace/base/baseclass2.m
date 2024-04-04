classdef baseclass2 < baseclass1
    properties
        width
        height
    end
    
    methods
        function obj = baseclass2(width, height)
            obj.width = width;
            obj.height = height;
        end
        
        function area = calculateArea(obj)
            area = obj.width * obj.height;
        end
        
        function perimeter = calculatePerimeter(obj)
            perimeter = 2 * (obj.width + obj.height);
        end
    end
end