function BezierFitDemo_debug
% BezierFitDemo_debug.m - Versão com prints de debug
% Baseado no código original BezierFitDemo.m

clear;
demo = 1;

switch demo
    case 1
        C =[0     0;
            1     2;
            3     3;
            4     2];
        
        Q = cubicBezierToPolyline(C, 65);
        n = 3;  % Starting number of knot points
end

fprintf('=== MATLAB DEBUG ===\n');
fprintf('Demo: %d, n: %d\n', demo, n);
fprintf('Q shape: %dx%d\n', size(Q,1), size(Q,2));
fprintf('Q first 5 points:\n');
disp(Q(1:5,:));

% Now try to do a piecewise cubic Bézier fit to Q starting with n knot points
Qt = Q';
fprintf('Qt shape: %dx%d\n', size(Qt,1), size(Qt,2));

[IG, k] = iguess0_debug(Qt, n);

fprintf('=== AFTER IGUESS0 ===\n');
fprintf('IG length: %d\n', length(IG));
fprintf('k: ');
disp(k);
fprintf('IG: ');
disp(IG);

% Improve the fit: Segmentally Optimum Only Curve (SOO)
SOC = segop_debug(k, Qt, IG);

fprintf('=== AFTER SEGOP ===\n');
fprintf('SOC length: %d\n', length(SOC));
fprintf('SOC: ');
disp(SOC);

% Improve it again: Segmentally then Globally Optimized Curve (SGO)
GOC = globop_debug(SOC, Qt, 0, k);

fprintf('=== AFTER GLOBOP ===\n');
fprintf('GOC length: %d\n', length(GOC));
fprintf('GOC: ');
disp(GOC);

fprintf('=== MATLAB DEBUG END ===\n');
end
