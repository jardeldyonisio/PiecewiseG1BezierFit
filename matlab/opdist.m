function se2 = opdist(id,Q,P,ang)

% function se2 = opdist(id,Q,P,ang). This function is the obj
% ective function to be minimized during segment optimization.
% It receives subcomponents from a curve's composite vector, a
% segment at a time. It returns the sum error for a segment.
% It was written by E. J. Lane.

n = length(Q);

C = ctpts(P,ang,id); 	% Call to compute the segments
% control points.

se2 = 0;
cont = 0;

% disp("id");
% disp(id);
% disp("Q");
% disp(Q);
% disp("P");
% disp(P);
% disp("ang");
% disp(ang);
% disp("C");
% disp(C);

% Loop to find distance error in a segment.
for j = 1:n
    np = NearestPoint(C', Q(:,j)');
    % disp("np");
    % disp(np);
    if (j==1) && isequal(np, C(:,1)')
        %disp("Entrou 1");
        d = zeros(1,2);
    elseif (j==n) && isequal(np, C(:,4)')
        %disp("Entrou 2");
        d = zeros(1,2);
    else
        %disp("Entrou 3");
        d = (Q(:,j)' - np);
        % disp("Q(:,j)'");
        % disp(Q(:,j)');
        % disp('d');
        % disp(d);
        % disp("np");
        % disp(np);
    end
    % disp("d");
    % disp(d);
    se2 = se2 + d*d';  
    % disp("se2");
    % disp(se2);
end