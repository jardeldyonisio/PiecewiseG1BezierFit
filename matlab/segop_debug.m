function SOC = segop_debug(k,Q,x0)
% Versão com debug do segop.m

fprintf('=== SEGOP DEBUG ===\n');
fprintf('k: ');
disp(k);
fprintf('Q shape: %dx%d\n', size(Q,1), size(Q,2));
fprintf('x0 length: %d\n', length(x0));
fprintf('x0: ');
disp(x0);

[P,ang,dt] = ktangdt(x0);   % Separates the vector x0 into its subcomponents.

fprintf('After ktangdt:\n');
fprintf('P shape: %dx%d\n', size(P,1), size(P,2));
fprintf('P: ');
disp(P);
fprintf('ang length: %d\n', length(ang));
fprintf('ang: ');
disp(ang);
fprintf('dt shape: %dx%d\n', size(dt,1), size(dt,2));
fprintf('dt: ');
disp(dt);

bdt = bstdst(dt,Q,P,ang,k); % Call to the function which finds
                            % the optimum distances for a segment.

fprintf('After bstdst:\n');
fprintf('bdt shape: %dx%d\n', size(bdt,1), size(bdt,2));
fprintf('bdt: ');
disp(bdt);

bdt1 = [];                  % ECR

for i = 1 : 2 % Loop to assemble the "best" distances.
    bdt1 =  [bdt1 bdt(i,:)];
end

fprintf('bdt1 length: %d\n', length(bdt1));
fprintf('bdt1: ');
disp(bdt1);

% Assemble the vector of parameters for the curve.
SOC = [P(1,:) P(2,:) ang bdt1];

fprintf('SOC length: %d\n', length(SOC));
fprintf('SOC: ');
disp(SOC);
fprintf('=== SEGOP DEBUG END ===\n');
end
