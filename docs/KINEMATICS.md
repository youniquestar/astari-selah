# Kinematic Modeling & Denavit-Hartenberg (D-H) Formulation

## 1. Kinematic Coordinate Frame Definitions

The arm is configured as an articulated 5-axis open kinematic chain:
1. **Frame 0 (Base)**: Origin at ground center of base enclosure.
2. **Frame 1 (Base Yaw)**: Rotates about $Z_0$ by angle $\theta_1$. Elevated by $d_1 = 85.0\text{ mm}$.
3. **Frame 2 (Shoulder Pitch)**: Rotates about $Y_1$ by angle $\theta_2$. Offset along $Z_1$ by $63.0\text{ mm}$ (effective height $148.0\text{ mm}$).
4. **Frame 3 (Elbow Pitch)**: Rotates about $Y_2$ by angle $\theta_3$. Offset along Link 1 axis by $a_2 = 220.0\text{ mm}$.
5. **Frame 4 (Wrist Pitch)**: Rotates about $Y_3$ by angle $\theta_4$. Offset along Link 2 axis by $a_3 = 180.0\text{ mm}$.
6. **Frame 5 (End-Effector / TCP)**: Offset by $d_5 = 60\text{ mm (wrist)} + 90\text{ mm (gripper)} = 150.0\text{ mm}$.

## 2. Standard Denavit-Hartenberg (D-H) Parameters

| Link $i$ | $\theta_i$ (Joint Angle) | $d_i$ (Link Offset) | $a_i$ (Link Length) | $\alpha_i$ (Link Twist) | Home ($\theta_i$) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | $\theta_1$ (Base Yaw) | $85.0\text{ mm}$ | $0.0\text{ mm}$ | $+90^\circ$ | $90.0^\circ$ |
| **2** | $\theta_2$ (Shoulder Pitch) | $63.0\text{ mm}$ | $220.0\text{ mm}$ | $0^\circ$ | $90.0^\circ$ |
| **3** | $\theta_3$ (Elbow Pitch) | $0.0\text{ mm}$ | $180.0\text{ mm}$ | $0^\circ$ | $90.0^\circ$ |
| **4** | $\theta_4$ (Wrist Pitch) | $0.0\text{ mm}$ | $60.0\text{ mm}$ | $0^\circ$ | $90.0^\circ$ |
| **5** | $0^\circ$ (Gripper TCP) | $0.0\text{ mm}$ | $90.0\text{ mm}$ | $0^\circ$ | — |

## 3. Forward Kinematics (FK)
Given joint angles $[\theta_1, \theta_2, \theta_3, \theta_4]$:

1. **Azimuthal angle**:
   $$\phi = \theta_1 - 90^\circ$$

2. **Elevation angles along the vertical plane**:
   $$\gamma_1 = \theta_2$$
   $$\gamma_2 = \gamma_1 + (\theta_3 - 90^\circ)$$
   $$\gamma_3 = \gamma_2 + (\theta_4 - 90^\circ)$$

3. **Planar radial distance $r$ and height $z$**:
   $$r = a_2 \cos(\gamma_1) + a_3 \cos(\gamma_2) + d_5 \cos(\gamma_3)$$
   $$z = d_1 + d_2 + a_2 \sin(\gamma_1) + a_3 \sin(\gamma_2) + d_5 \sin(\gamma_3)$$

4. **3D Cartesian coordinates**:
   $$X = r \cos(\phi)$$
   $$Y = r \sin(\phi)$$
   $$Z = z$$
   $$\text{Pitch} = \gamma_3$$

## 4. Analytical Inverse Kinematics (IK)
Given target $(X, Y, Z, \text{Pitch})$:

1. **Solve Joint 1 (Base Yaw)**:
   $$\theta_1 = \text{atan2}(Y, X) + 90^\circ$$

2. **Wrist Center Coordinates**:
   $$r = \sqrt{X^2 + Y^2}$$
   $$r_w = r - d_5 \cos(\text{Pitch})$$
   $$z_w = Z - d_5 \sin(\text{Pitch})$$

3. **Distance from Shoulder Pivot to Wrist**:
   $$\Delta r = r_w$$
   $$\Delta z = z_w - 148.0\text{ mm}$$
   $$D = \sqrt{\Delta r^2 + \Delta z^2}$$

4. **Law of Cosines for Elbow Pitch ($\theta_3$)**:
   $$\cos(\beta) = \frac{D^2 - a_2^2 - a_3^2}{2 a_2 a_3}$$
   $$\theta_3 = 180^\circ - \arccos(\beta)$$

5. **Shoulder Pitch ($\theta_2$)**:
   $$\alpha = \text{atan2}(\Delta z, \Delta r)$$
   $$\psi = \arccos\left(\frac{a_2^2 + D^2 - a_3^2}{2 a_2 D}\right)$$
   $$\theta_2 = \alpha + \psi$$

6. **Wrist Pitch ($\theta_4$)**:
   $$\theta_4 = \text{Pitch} - (\theta_2 + \theta_3 - 180^\circ) + 90^\circ$$
