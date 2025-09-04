function [IG, k] = iguess0_debug(Q, n, k)
% Versão com debug do iguess0.m

global dpkpc;
[r ,m] = size(Q);

fprintf('=== IGUESS0 DEBUG ===\n');
fprintf('Q shape: %dx%d\n', r, m);
fprintf('n: %d\n', n);

% Q  = datapoints (2xm)
% n  = The number of knotpoints
% k  = default know positions (indices 1...m)
if nargin < 3
    k = defk(m,n); % Calls for default knot position.
end

fprintf('k after defk: ');
disp(k);

dpkpc = k; 		    % Position of knot points passed globally.
P   = knots(Q,k); 	% call to compute the knotpoints.

fprintf('P shape: %dx%d\n', size(P,1), size(P,2));
fprintf('P: ');
disp(P);

dt  = distEJL(P); 	% Call to compute the distance between
                    % successive knot points.

fprintf('dt shape: %dx%d\n', size(dt,1), size(dt,2));
fprintf('dt: ');
disp(dt);

ang = tang(Q,k); 	% Call to compute the angles for
                    % the unit tangent vectors.

fprintf('ang length: %d\n', length(ang));
fprintf('ang: ');
disp(ang);

C   = ctpts(P,ang,dt);	% Call to compute the control points;
                        % for the curve.

fprintf('C shape: %dx%d\n', size(C,1), size(C,2));
fprintf('C first 5 points: ');
if size(C,1) >= 5
    disp(C(1:5,:));
else
    disp(C);
end

% Assemble the composite vector of the initial guess curve parameters
IG = [P(1,:) P(2,:) ang dt(1,:) dt(2,:)];

fprintf('IG length: %d\n', length(IG));
fprintf('IG: ');
disp(IG);
fprintf('=== IGUESS0 DEBUG END ===\n');
end
