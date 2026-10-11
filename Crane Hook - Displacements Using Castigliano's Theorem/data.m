% Material properties
E = 210E3; % Hooke's modulus [MPa]
sigma_yield = 650; % yield strength [MPa]

% Geometric properties
ri = 50; % internal radius in mm
ro = 110; % outer radius in mm
h = ro - ri; % trapezoid's height
bi = 60; % larger base of the trapezoid
bo = 34.23; % smaller base of the trapezoid
A = (bi + bo) * h * 0.5; % area of the cross_section
rc = ri + (h/3) * ((bi + 2* bo)/(bi + bo)) ; % radius of the centroid section
rn = A / (bo - bi + ( (bi*ro - bo*ri)/h)*log(ro/ri)); % neutral axis
e = rc - rn; % eccentricity

% --- Geometric Properties of the Upper Neck ---
ra = 70.24; % Centroidal radius of the upper neck (mm)

% Because the neck curves backwards, the cross-section is flipped relative 
% to the new center of curvature. The narrow base is now on the inside.
b_ai = bo; % Inner base of the neck is the narrow base
b_ao = bi; % Outer base of the neck is the wide base

% The inner and outer radii of the neck curve
r_ai = ra - (rc - ri); 
r_ao = r_ai + h;

% Compute the new neutral axis and eccentricity for the neck
r_na = A / (b_ao - b_ai + ((b_ai*r_ao - b_ao*r_ai)/h)*log(r_ao/r_ai));
ea = abs(ra - r_na); % Eccentricity of the upper neck

% Loads 
F = 50000;  % applied load [N]
M = F * rc; % bending equivalent load [N*mm]
N = F; % normal equivalent load [N]