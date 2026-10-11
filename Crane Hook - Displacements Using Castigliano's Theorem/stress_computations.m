% Analytical Stress
r = linspace(ri,ro,100);
y = rc - r; 
sigma_M = M * (y-e) ./ (A*e*(rc-y)); % sigma value due to the bending load [MPa]
sigma_N = N / A; %sigma value due to the normal load [MPa]
sigma = sigma_N + sigma_M; % superimposition on bending and normal effects

% Adimensionalization of analytical quantities
adi_r = r ./ rc;
adi_sigma = sigma ./ sigma_yield;

% Process Numerical FEA Stress Data
T = readtable('cross_section_stresses.csv', 'VariableNamingRule', 'preserve');
X_all = T.X;
Z_all = T.Z;
S22_all = T.S22;

tolerance = 0.5; 
midplane_idx = abs(X_all) <= tolerance;
Z_center = Z_all(midplane_idx);
S22_center = S22_all(midplane_idx);

[Z_sorted, sort_idx] = sort(Z_center);
S22_sorted = S22_center(sort_idx);

% Adimensionalization of numerical quantities
adi_Z_1 = Z_sorted ./ rc;
adi_S22_1 = S22_sorted ./ sigma_yield;

% Process Numerical FEA Stress Data
T = readtable('cross_section_stresses2.csv', 'VariableNamingRule', 'preserve');
X_all = T.X;
Z_all = T.Z;
S22_all = T.S22;

tolerance = 0.5; 
midplane_idx = abs(X_all) <= tolerance;
Z_center = Z_all(midplane_idx);
S22_center = S22_all(midplane_idx);

[Z_sorted, sort_idx] = sort(Z_center);
S22_sorted = S22_center(sort_idx);

% Adimensionalization of numerical quantities
adi_Z_2 = Z_sorted ./ rc;
adi_S22_2 = S22_sorted ./ sigma_yield;