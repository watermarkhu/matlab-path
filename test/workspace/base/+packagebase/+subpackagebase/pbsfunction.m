function output = pbsfunction(input)
    % This function performs a random operation on the input
    
    % Random operation
    output = input + randn(size(input));
end