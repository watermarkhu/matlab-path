
% Comment

%{
    Comment block 
%}

function ret = myfunction(arg1, arg2):
    % This is a function

    arguments
        arg1 (1,1) double {mustBeNumeric, mustBePositive} = 1
        arg2 (1,1) double {mustBeNumeric, mustBePositive} = basefunction2(arg1)
    end
    import packagecore.pcfunction
    import packagebase.*
    import packagebase.subpackagebase.*
    %#function num2str linspace

    pbsfunction(arg1, arg2);
    arg3 = function2;
    function3
    [arg4, arg5] = pbfunction1(arg1);

    unknown_function(arg1, arg2, arg3);

    variable = arg1;
    value = function_direct_call;
    script_direct_call;

    packagecore.pcfunction(arg1, arg2, arg3);

    baseclass1.calculateArea(0, 1, 2);

    ret = arg1 + arg2 + arg3;
end