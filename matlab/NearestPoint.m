function np = NearestPoint(C, P)

% Quick and dirty find nearest point on cubic B�zier curve specfied by
% control points C to point P sing Geom2D toolkit

% Compute complete Bezier
% disp("C");
% disp(C);
% disp("P");
% disp(P);
% asdasdas
% disp("C");
% disp(C);
Q = cubicBezierToPolyline(C, 128);
% disp("Q");
% disp(Q);
% Find nearest point on Bezier
ind = findClosestPoint(P, Q);
% disp("ind");
% disp(ind);
np  = Q(ind,:);
% disp("np");
% disp(np);

% % Test
% figure;plot(Q(:,1), Q(:,2), 'b.--', C(:,1), C(:,2), 'ks:');
% hold on;
% plot(P(1), P(2), 'rx', np(1), np(2), 'ro');
% axis equal; axis tight;
