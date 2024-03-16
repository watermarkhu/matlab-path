
% Comment

%{
    Comment block 
%}

function ret = function0(arg1, arg2):
    % This is a function

    arguments
        arg1 (1,1) double {mustBeNumeric, mustBePositive} = 1
        arg2 (1,1) double {mustBeNumeric, mustBePositive} = function2(arg1)
    end
    import package1.function22
    import package2.*
    import package2.package3.*
    %#function num2str linspace

    function1(arg1, arg2);
    arg3 = function2;
    function3
    [arg4, arg5] = function4(arg1);
    ret = arg1.class.list(0) + arg2 + arg3;
end