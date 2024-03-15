function output = privatefunction(input)
    % This is a private function.
    % It takes an input and returns an output.
    
    % Your code here
    arguments (Input)
        input (1,1) double = 1
    end
    arguments (Output)
        output (1,1) string
    end
    
    output = string(input) % Your output value here
end