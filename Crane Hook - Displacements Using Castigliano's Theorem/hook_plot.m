clear; clc; close all;

% Initialize the data script - contains geometric and material data
data;

% Initialize the stress computations script
stress_computations;

% Initialize the displacement computations script
displacement_computations;

% --- Plot 1: Cross-Sectional Stress ---
figure('Name', 'Cross-Sectional Stress Comparison', 'Color', 'w');
hold on; grid on;

% 2. Plot the analytical and FEM curves
plot(adi_r, adi_sigma, "b-", 'LineWidth', 1.5, 'DisplayName', 'Analytical Results');
plot(adi_Z_1, adi_S22_1, "r-.*", 'LineWidth', 1.5, 'DisplayName', 'FEM Results - Coarse Mesh');
plot(adi_Z_2, adi_S22_2, "g^-", 'LineWidth', 1.5, 'DisplayName', 'FEM Results - Fine Mesh');

% 3. Add the arrows (quiver plot)
% arrow_spacing = 5; % Plots an arrow every 5th data point (adjust for density)
% r_arrows = adi_r(1:arrow_spacing:end);
% sigma_arrows = adi_sigma(1:arrow_spacing:end);
% 
% % quiver(X_start, Y_start, U_vector, V_vector)
% % AutoScale must be 'off' so the arrows reach exactly to the curve
% quiver(r_arrows, zeros(size(r_arrows)), zeros(size(r_arrows)), sigma_arrows, ...
%     'AutoScale', 'off', ...
%     'Color', 'k', ...
%     'LineWidth', 1, ...
%     'MaxHeadSize', 0.1, ...
%     'DisplayName', 'Stress Vectors');

% 4. Add vertical lines for Neutral and Centroidal axes (from your previous setup)
% Note: Make sure 'rc' and 'rn' are accessible in this workspace, or use their adimensionalized versions
xline(rn/rc, 'LineStyle', '--', 'Color', [0.5 0.5 0.5], 'Label', 'Neutral Axis Radius');
xline(1, 'LineStyle', '--', 'Color', [0.5 0.5 0.5], 'Label', 'Centroid Radius');
yline(0, 'k-', 'LineWidth', 1);
% Formatting
xlabel('$\frac{r}{r_c} \ [-]$', 'Interpreter', 'latex');
ylabel('$\frac{\sigma}{\sigma_y} \ [-]$', 'Interpreter', 'latex');
legend('Anality Results','Numerical Results - Coarse Mesh', 'Numerical Results - Fine Mesh','Location', 'best');
title('Stress Distribution along the Critical Cross-Section');
set(gca, 'FontSize', 11);
hold off;


% --- Adimensionalize Coordinates ---
adi_X_und = X_und / rc;
adi_Y_und = Y_und / rc;

adi_X_ana_def = X_ana_def / rc;
adi_Y_ana_def = Y_ana_def / rc;

if data_loaded_1
    adi_X_num_def_1 = X_num_def_1 / rc;
    adi_Y_num_def_1 = Y_num_def_1 / rc;
end
if data_loaded_2
    adi_X_num_def_2 = X_num_def_2 / rc;
    adi_Y_num_def_2 = Y_num_def_2 / rc;
end


% --- Plot 2: Hook Deflection (Dimensionless) ---
figure('Name', 'Crane Hook Deflection Comparison', 'Color', 'w');
hold on; grid on; axis equal;

% Plot the dimensionless data
plot(adi_X_und, adi_Y_und, 'k--', 'LineWidth', 1.5, 'DisplayName', 'Undeformed Geometry');
plot(adi_X_ana_def, adi_Y_ana_def, 'b-', 'LineWidth', 2, 'DisplayName', sprintf('Analytical Deformed (%dx)', scale_factor));

% if data_loaded_1
%     plot(adi_X_num_def_1, adi_Y_num_def_1, 'r-.*', 'MarkerSize', 7.5, 'LineWidth', 1.2, ...
%         'DisplayName', sprintf('Numerical Deformed - Coarse Mesh (%dx)', scale_factor));
% end
% if data_loaded_2
%     plot(adi_X_num_def_2, adi_Y_num_def_2, 'g^-', 'MarkerSize', 7.5, 'LineWidth', 1.2, ...
%         'DisplayName', sprintf('Numerical Deformed - Fine Mesh (%dx)', scale_factor));
% end
% Formatting
title('Crane Hook Centerline: Analytical vs. Numerical Deformation');
xlabel('$\frac{X}{r_c} \ [-]$', 'Interpreter', 'latex');
ylabel('$\frac{Y}{r_c} \ [-]$', 'Interpreter', 'latex');
legend('Location', 'best');
set(gca, 'FontSize', 11);
hold off;