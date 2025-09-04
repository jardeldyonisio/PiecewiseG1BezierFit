% BezierFitDemo_final.m - Final version with plot saving
% 
% A demonstration of the piecewise, cubic Bézier curve fit.
%
% See also: globop, segop, iguess0, poplt, knots

function BezierFitDemo_final()

    % Demonstrate Bezier curve fit
    demo = 1;
    k = [];
    
    if demo == 1
        C = [0,0; 1,2; 3,3; 4,2];
        Q = cubicBezierToPolyline(C, 65);
        n = 3; % Starting number of knot points
    end
    
    fprintf('Demo: %d, n: %d\n', demo, n);
    fprintf('Q size: %dx%d\n', size(Q, 1), size(Q, 2));
    
    % Now try to do a piecewise cubic Bézier fit to Q starting with n knot points
    [IG, k, dpkpc] = iguess0(Q, n, k);
    fprintf('Initial guess completed, k: [%s]\n', num2str(k));
    
    % Improve the fit: Segmentally Optimum Only Curve (SOO)
    SOC = segop(k, Q, IG);
    fprintf('Segmental optimization completed\n');
    
    % Improve it again: Segmentally then Globally Optimized Curve (SGO)
    GOC = globop(SOC, Q, 0, k, dpkpc);
    fprintf('Global optimization completed\n');
    
    % plot SGO curve using internal routine
    figure;
    poplt(GOC, Q);
    title('MATLAB: Plot of SGO curve');
    print('-dpng', '-r300', '/home/jardeldyonisio/PiecewiseG1BezierFit/matlab_sgo_curve.png');
    fprintf('Saved MATLAB SGO curve plot\n');
    
    % Get the Bézier control points of the curve fit
    Cnew = cpoints(GOC);
    P = knots(Q, k);
    
    % Plot fitted, segment by segment
    figure;
    for i = 1:3:length(Cnew)-2
        if i+3 <= length(Cnew)
            drawBezierCurve(Cnew(i:i+3,:));  % Fitted cubic Bézier segment
        end
    end
    hold on;
    
    hc = plot(Cnew(:,1), Cnew(:,2), 'o-', 'LineWidth', 2, 'MarkerSize', 6);
    ho = plot(Q(:,1), Q(:,2), 'k.', 'MarkerSize', 3);
    hn = plot(P(:,1), P(:,2), 'kx', 'MarkerSize', 10, 'LineWidth', 3);
    
    legend('Original data', sprintf('Original guess n = %d knots', n), 'New control points');
    title('MATLAB: Detailed Bézier Curve Fit');
    grid on;
    axis equal;
    
    print('-dpng', '-r300', '/home/jardeldyonisio/PiecewiseG1BezierFit/matlab_detailed_fit.png');
    fprintf('Saved MATLAB detailed fit plot\n');
    
end
