function output = functioncore(input)
    % This function calculates the sum of the squares of the elements in the input array.
    % It then returns the square root of the sum.
    
    % Calculate the sum of squares
    sumOfSquares = sum(input.^2);
    
    % Calculate the square root of the sum
    output = sqrt(sumOfSquares);
end