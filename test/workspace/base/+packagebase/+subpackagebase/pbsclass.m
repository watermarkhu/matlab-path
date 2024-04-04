classdef pbsclass
    properties
        brand
        model
        color
        price
    end
    
    methods
        function obj = pbsclass(brand, model, color, price)
            obj.brand = brand;
            obj.model = model;
            obj.color = color;
            obj.price = price;
        end
        
        function displayInfo(obj)
            fprintf('Brand: %s\n', obj.brand);
            fprintf('Model: %s\n', obj.model);
            fprintf('Color: %s\n', obj.color);
            fprintf('Price: $%.2f\n', obj.price);
        end
    end
end