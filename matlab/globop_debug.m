function GOC = globop_debug(xi,Q,t,k)
% Versão com debug do globop.m

fprintf('=== GLOBOP DEBUG ===\n');
fprintf('xi length: %d\n', length(xi));
fprintf('xi: ');
disp(xi);
fprintf('Q shape: %dx%d\n', size(Q,1), size(Q,2));
fprintf('t: %d\n', t);
fprintf('k: ');
disp(k);

options.Display = 'off';  % ECR, to match obselete fmins params above
options.TolX    = 0.01;
options.TolFun  = 0.01;

% Teste da função objetivo antes da otimização
fprintf('Testing objf2 before optimization:\n');
obj_value = objf2(xi, Q, t, k);
fprintf('Initial objective value: %f\n', obj_value);

GOC = fminsearch(@objf2, xi, options, Q, t, k);

fprintf('After fminsearch:\n');
fprintf('GOC length: %d\n', length(GOC));
fprintf('GOC: ');
disp(GOC);

% Teste da função objetivo após a otimização
obj_value_final = objf2(GOC, Q, t, k);
fprintf('Final objective value: %f\n', obj_value_final);

fprintf('=== GLOBOP DEBUG END ===\n');
end
