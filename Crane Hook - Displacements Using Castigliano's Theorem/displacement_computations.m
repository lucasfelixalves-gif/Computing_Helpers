% =========================================================================
% Crane Hook Centerline Displacement (Full System Castigliano)
% =========================================================================

% Deformation Scale Factor
scale_factor = 50; 

% PLOT domain up to Section A-A (90 degrees)
Theta_plot_max = 90; 
theta_array = linspace(0, deg2rad(Theta_plot_max), 50);

% 1. Compute Undeformed Analytical Geometry
X_und = -rc * sin(theta_array);
Y_und = -rc * cos(theta_array);

% 2. Compute Analytical Deformed Geometry
delta_X = zeros(size(theta_array));
delta_Y = zeros(size(theta_array));

% Properties of the upper neck
ra = 70.24; 
r_ai = ra - (rc - ri); 
r_ao = r_ai + h;
b_ai = bo; % Narrow base is on the INSIDE of local curvature
b_ao = bi; % Wide base is on the OUTSIDE
r_na = A / (b_ao - b_ai + ((b_ai*r_ao - b_ao*r_ai)/h)*log(r_ao/r_ai)); 
ea = abs(ra - r_na);

for i = 1:length(theta_array)
    alpha = theta_array(i);
    X_alpha = -rc * sin(alpha);
    Y_alpha = -rc * cos(alpha);

    % --- PART A: Strain Energy of the Lower Hook ---
    % Integrate from alpha to the transition (150 deg)
    theta_int = linspace(alpha, deg2rad(150), 100);

    X_theta = -rc * sin(theta_int);
    Y_theta = -rc * cos(theta_int);

    % Explicit Shigley Load Formulations
    M_theta = F * rc * sin(theta_int);
    N_theta = F * sin(theta_int);

    % Virtual load arms
    mx_theta = Y_theta - Y_alpha; 
    nx_theta = -cos(theta_int); 

    my_theta = X_alpha - X_theta; 
    ny_theta = sin(theta_int); 

    dU_dX_theta = (M_theta .* mx_theta) / (E * A * e) + (N_theta .* nx_theta * rc) / (E * A);
    dU_dY_theta = (M_theta .* my_theta) / (E * A * e) + (N_theta .* ny_theta * rc) / (E * A);

    dX_lower = trapz(theta_int, dU_dX_theta);
    dY_lower = trapz(theta_int, dU_dY_theta);

    % --- PART B: Strain Energy of the Upper Neck ---
    % Integrate from beta = 0 to 60 deg 
    beta_int = linspace(0, deg2rad(60), 100);

    % Neck global coordinates 
    X_neck = -0.5*(rc+ra) + ra*cos(deg2rad(-60) + beta_int);
    Y_neck = (sqrt(3)/2)*(rc+ra) + ra*sin(deg2rad(-60) + beta_int);

    % Load Formulations (Moment = Force * distance to F axis)
    M_beta = -F * X_neck; 
    tangent_angle = deg2rad(30) + beta_int;
    N_beta = F * sin(tangent_angle);

    % Virtual load arms mapped from alpha to the neck cut
    mx_beta = Y_neck - Y_alpha;
    nx_beta = -cos(tangent_angle);

    my_beta = X_alpha - X_neck;
    ny_beta = sin(tangent_angle);

    dU_dX_beta = (M_beta .* mx_beta) / (E * A * ea) + (N_beta .* nx_beta * ra) / (E * A);
    dU_dY_beta = (M_beta .* my_beta) / (E * A * ea) + (N_beta .* ny_beta * ra) / (E * A);

    dX_upper = trapz(beta_int, dU_dX_beta);
    dY_upper = trapz(beta_int, dU_dY_beta);

    % --- TOTAL VIRTUAL DISPLACEMENT ---
    % By definition, Castigliano with horizontal pointing LEFT and vertical DOWN
    % gives positive values for those directions. True displacements must be inverted.
    true_dX = -(dX_lower + dX_upper);
    true_dY = -(dY_lower + dY_upper);

    delta_X(i) = true_dX;
    delta_Y(i) = true_dY;
end

% Apply true vector displacements to the undeformed coordinates
X_ana_def = X_und + (delta_X * scale_factor);
Y_ana_def = Y_und + (delta_Y * scale_factor);

% 3. Load and Process Numerical Displacement Data
try
    num_data = readtable('curvature_displacements.csv', 'VariableNamingRule', 'preserve');

    % A. Advanced Spatial Filtering
    % 1. Mid-plane (CAD X ~ 0)
    % 2. Left side of the hook only (CAD Z >= 0) to match the 0 to 150 deg analytical sweep
    % 3. Cut off the upper straight shank (CAD Y <= 115)
    tolerance = 0.5;
    valid_idx = (abs(num_data.X) <= tolerance) & (num_data.Z >= 0) & (num_data.Y <= 110);

    % B. Extract Raw CAD Coordinates
    Z_CAD = num_data.Z(valid_idx);
    Y_CAD = num_data.Y(valid_idx);

    % C. Shift to the Center of Curvature
    CAD_Center_Z = 0;   
    CAD_Center_Y = 110; 

    Z_centered = Z_CAD - CAD_Center_Z;
    Y_centered = Y_CAD - CAD_Center_Y;

    % D. Map to Analytical Axes (Flip Z to X to match the left-curving math)
    X_num_und = -Z_centered; 
    Y_num_und = Y_centered;

    % E. Map Displacements (Flip U3 to match X orientation)
    U_X_num = -num_data.U3(valid_idx); 
    U_Y_num = num_data.U2(valid_idx); 

    % F. Apply SCALED numerical displacements
    X_num_def = X_num_und + (U_X_num * scale_factor);
    Y_num_def = Y_num_und + (U_Y_num * scale_factor);

    % G. Sort by Y-coordinate (Safest method for a monotonic curve)
    [~, sort_idx] = sort(Y_num_und);

    X_num_def_1 = X_num_def(sort_idx);
    Y_num_def_1 = Y_num_def(sort_idx);

    data_loaded_1 = true;
catch ME
    warning('Error loading FEA data: %s', ME.message);
    data_loaded_1 = false;
end

try
    num_data = readtable('curvature_displacements2.csv', 'VariableNamingRule', 'preserve');

    % A. Advanced Spatial Filtering
    % 1. Mid-plane (CAD X ~ 0)
    % 2. Left side of the hook only (CAD Z >= 0) to match the 0 to 150 deg analytical sweep
    % 3. Cut off the upper straight shank (CAD Y <= 115)
    tolerance = 0.5;
    valid_idx = (abs(num_data.X) <= tolerance) & (num_data.Z >= 0) & (num_data.Y <= 110);

    % B. Extract Raw CAD Coordinates
    Z_CAD = num_data.Z(valid_idx);
    Y_CAD = num_data.Y(valid_idx);

    % C. Shift to the Center of Curvature
    CAD_Center_Z = 0;   
    CAD_Center_Y = 110; 

    Z_centered = Z_CAD - CAD_Center_Z;
    Y_centered = Y_CAD - CAD_Center_Y;

    % D. Map to Analytical Axes (Flip Z to X to match the left-curving math)
    X_num_und = -Z_centered; 
    Y_num_und = Y_centered;

    % E. Map Displacements (Flip U3 to match X orientation)
    U_X_num = -num_data.U3(valid_idx); 
    U_Y_num = num_data.U2(valid_idx); 

    % F. Apply SCALED numerical displacements
    X_num_def = X_num_und + (U_X_num * scale_factor);
    Y_num_def = Y_num_und + (U_Y_num * scale_factor);

    % G. Sort by Y-coordinate (Safest method for a monotonic curve)
    [~, sort_idx] = sort(Y_num_und);

    X_num_def_2 = X_num_def(sort_idx);
    Y_num_def_2 = Y_num_def(sort_idx);

    data_loaded_2 = true;
catch ME
    warning('Error loading FEA data: %s', ME.message);
    data_loaded_2 = false;
end