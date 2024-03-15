function output = function4(input)
    % This function takes an input and returns a random output.
    
    % Generate a random number between 1 and 10
    random_num = randi([1, 10]);
    
    % Multiply the input by the random number
    output = input * random_num;
end