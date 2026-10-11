# Appendix A: Derivation of Internal Bending Moments for Castigliano’s Theorem

## 1. Introduction

To compute the horizontal and vertical displacements at an arbitrary angle $\Theta$ on the lower hook, fictitious dummy loads are introduced at the point of interest $(X_\Theta, Y_\Theta)$. The horizontal dummy load $H$ acts in the $-X$ direction, and the vertical dummy load $V$ acts in the $-Y$ direction. These loads are used with Castigliano’s theorem to obtain the corresponding displacement components by differentiating the strain energy with respect to $H$ and $V$. The real working load $F$ is applied vertically downwards at the hook’s tip, taken as the origin of the applied-load coordinate description. The internal bending moment is obtained by isolating the portion of the hook on the load side of a moving cut and enforcing moment equilibrium about that cut.

![Crane Hook Coordinate System](centerline_2.png)

## 2. Coordinate System and Geometric Mapping

The global origin $(0,0)$ is defined at the center of curvature of the lower hook. The coordinates of each moving cut are expressed in this global Cartesian system. The angle $\Theta$ identifies the point at which the displacement is sought, whereas $\theta$ or $\beta$ identifies the location of the moving integration cut.

### 2.1 Lower Hook: $0^\circ \le \theta \le 150^\circ$

For the lower hook, the centroidal centerline is represented by a circular arc of radius $r_c$. The point of interest at angle $\Theta$ has coordinates

$$
X_\Theta = -r_c \sin\Theta,
\qquad
Y_\Theta = -r_c \cos\Theta.
$$

The moving cut at angle $\theta$ has coordinates

$$
X_\theta = -r_c \sin\theta,
\qquad
Y_\theta = -r_c \cos\theta.
$$

Here, $\Theta$ is held fixed while $\theta$ varies over the lower-hook integration interval. This distinction is important: the dummy loads remain applied at $(X_\Theta,Y_\Theta)$, while the internal section and its moment arm change with the integration variable $\theta$.

### 2.2 Upper Neck: $0^\circ \le \beta \le 60^\circ$

At $\theta=150^\circ$, the curvature inflects and the center of curvature shifts to a new point $C_a$. This change in centerline curvature is represented by the upper-neck centroidal radius $r_a$. The location of $C_a$ is selected to maintain geometric continuity with the lower-hook arc:

$$
X_{C_a} = -\frac{1}{2}(r_c+r_a),
\qquad
Y_{C_a} = \frac{\sqrt{3}}{2}(r_c+r_a).
$$

The upper-neck cut is parameterized by an angle that sweeps from $-60^\circ$ to $0^\circ$ relative to $C_a$. With $\beta$ varying from $0^\circ$ to $60^\circ$, the corresponding global Cartesian coordinates are

$$
X_\beta
= -\frac{1}{2}(r_c+r_a)
  + r_a\cos(\beta-60^\circ),
$$

$$
Y_\beta
= \frac{\sqrt{3}}{2}(r_c+r_a)
  + r_a\sin(\beta-60^\circ).
$$

These mappings express the upper-neck cut in the same global coordinate system used for the lower hook and for the dummy-load application point.

## 3. Internal Moment of the Lower Hook: $M_\theta$

For the lower-hook segment, the sign convention is chosen such that a positive bending moment places the inner, or right-hand, fibers in tension. Taking moments about the moving cut $(X_\theta,Y_\theta)$, the internal bending moment must balance the moments produced by the real load $F$ and the two dummy loads:

$$
M_\theta
= -F\cdot X_\theta
  + H\cdot(Y_\theta-Y_\Theta)
  + V\cdot(X_\Theta-X_\theta).
$$

The first term is the moment of the vertically downward real load about the cut. The horizontal dummy load has the vertical lever arm $Y_\theta-Y_\Theta$, while the vertical dummy load has the horizontal lever arm $X_\Theta-X_\theta$.

Substituting the lower-hook coordinates gives

$$
\begin{aligned}
M_\theta
&= -F(-r_c\sin\theta)
  + H\left[(-r_c\cos\theta)-(-r_c\cos\Theta)\right] \\
&\quad
  + V\left[(-r_c\sin\Theta)-(-r_c\sin\theta)\right].
\end{aligned}
$$

Simplifying each moment arm produces the explicit lower-hook expression

$$
\boxed{
M_\theta
= F r_c\sin\theta
  + H r_c(\cos\Theta-\cos\theta)
  + V r_c(\sin\theta-\sin\Theta)
}
$$

The first term is the bending moment caused by the real working load. The terms proportional to $H$ and $V$ are the virtual-load contributions required when differentiating the strain energy with respect to the corresponding displacement coordinates.

## 4. Internal Moment of the Upper Neck: $M_\beta$

Because the upper-neck curvature inflects relative to the lower hook, the inner fibers are now on the left side of the section. Accordingly, the positive-moment convention is reversed for this portion of the centerline: a positive $M_\beta$ places the left fibers in tension.

Taking moments about the upper-neck cut $(X_\beta,Y_\beta)$ gives

$$
M_\beta
= -F\cdot X_\beta
  + H\cdot(Y_\beta-Y_\Theta)
  + V\cdot(X_\Theta-X_\beta).
$$

Substitute the upper-neck coordinates and the lower-hook coordinates of the dummy-load point:

$$
\begin{aligned}
M_\beta
={}&
-F\left[
-\frac{1}{2}(r_c+r_a)
+r_a\cos(\beta-60^\circ)
\right] \\
&+H\left[
\frac{\sqrt{3}}{2}(r_c+r_a)
+r_a\sin(\beta-60^\circ)
+r_c\cos\Theta
\right] \\
&+V\left[
-r_c\sin\Theta
+\frac{1}{2}(r_c+r_a)
-r_a\cos(\beta-60^\circ)
\right].
\end{aligned}
$$

Rearranging the real-load term yields the fully expanded upper-neck moment equation:

$$
\boxed{
\begin{aligned}
M_\beta
={}&
F\left[
\frac{1}{2}(r_c+r_a)
-r_a\cos(\beta-60^\circ)
\right] \\
&+H\left[
\frac{\sqrt{3}}{2}(r_c+r_a)
+r_a\sin(\beta-60^\circ)
+r_c\cos\Theta
\right] \\
&+V\left[
-r_c\sin\Theta
+\frac{1}{2}(r_c+r_a)
-r_a\cos(\beta-60^\circ)
\right].
\end{aligned}
}
$$

The terms multiplying $H$ and $V$ are the corresponding virtual-work moment arms for a cut in the upper neck. In an application of Castigliano’s theorem, $M_\beta$ is used in the upper-neck strain-energy integral, with the upper-neck section properties and the sign convention defined above.
