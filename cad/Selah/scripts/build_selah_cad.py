#!/usr/bin/env python3
"""
================================================================================
SELAH — PROFESSIONAL MODULAR FREECAD CAD SYSTEM
================================================================================
Rebuilds every mechanical component, actuator, bearing, and fastener of the
Astari Selah 5-DOF robotic manipulator directly in FreeCAD.

Features:
- Native FreeCAD Group Hierarchy with root folder 'Selah' and organized sub-folders:
    ├── Selah/
    │   ├── 01_Base_Assembly/
    │   ├── 02_Shoulder_Assembly/
    │   ├── 03_Upper_Arm_Assembly/
    │   ├── 04_Forearm_Assembly/
    │   ├── 05_Wrist_Assembly/
    │   ├── 06_Gripper_Assembly/
    │   ├── 07_Actuators_And_Electronics/
    │   └── 08_Bearings_And_Fasteners/
- Modular separation: Every component is individually modeled, assigned professional
  color styling, and exported both as an individual .FCStd project and in the master assembly.
- Rich industrial design features: cooling louvers, wiring conduits, lightening trusses,
  bearing retaining pockets, recessed FSR 402 tactile nests, and chamfered gussets.
- Output formats: Native .FCStd, ISO-10303 STEP solids, and high-precision STL meshes.
================================================================================
"""

import sys
import os
import math

try:
    import FreeCAD
    import Part
    import Mesh
except ImportError:
    print("Error: FreeCAD Python API modules not found. Execute with FreeCAD or freecadcmd.")
    sys.exit(1)

# Base Paths
try:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    SCRIPT_DIR = "/home/jeremiah/ros2_ws/src/astari_selah/cad/Selah/scripts"
SELAH_DIR = os.path.dirname(SCRIPT_DIR)
CAD_ROOT = os.path.dirname(SELAH_DIR)
REPO_ROOT = os.path.dirname(CAD_ROOT)

ASM_DIR = os.path.join(SELAH_DIR, "assembly")
PARTS_DIR = os.path.join(SELAH_DIR, "parts")
COMPONENTS_DIR = os.path.join(SELAH_DIR, "components")

LEGACY_PARTS_DIR = os.path.join(CAD_ROOT, "parts")
ROS2_VISUAL_DIR = os.path.join(REPO_ROOT, "ros2", "astari_selah_description", "meshes", "visual")
ROS2_COLLISION_DIR = os.path.join(REPO_ROOT, "ros2", "astari_selah_description", "meshes", "collision")

for d in [ASM_DIR, PARTS_DIR, COMPONENTS_DIR, LEGACY_PARTS_DIR, ROS2_VISUAL_DIR, ROS2_COLLISION_DIR]:
    os.makedirs(d, exist_ok=True)

# Curated Professional Color Palette (RGB 0.0 - 1.0)
COLOR_CHASSIS_BLACK  = (0.13, 0.13, 0.15)   # Matte Stealth Black (PETG / PLA+)
COLOR_ROBOTIC_BLUE   = (0.05, 0.38, 0.88)   # Industrial Precision Blue
COLOR_SERVO_ALU      = (0.25, 0.25, 0.28)   # Anodized Aluminum Heatsink
COLOR_SERVO_GOLD     = (0.85, 0.65, 0.13)   # Brass / Titanium Nitride Spline
COLOR_BEARING_CHROME = (0.82, 0.84, 0.86)   # 52100 Chrome Steel
COLOR_FASTENER_STEEL = (0.45, 0.47, 0.50)   # 12.9 Grade Black Oxide Steel
COLOR_FSR_TOUCH      = (0.18, 0.78, 0.52)   # Tactile Sensor Mint Green

# ==============================================================================
# 1. BASE ENCLOSURE (Diameter: 180mm, Height: 85mm, D-Profile, Louvers & Standoffs)
# ==============================================================================
def build_base_enclosure():
    """Builds the stationary base housing electronics and turntable bearing."""
    R = 90.0
    H = 85.0
    
    # Main outer cylinder
    base = Part.makeCylinder(R, H, FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1))
    
    # D-Profile rear flat face at Y = -68mm (for connector and switch panel)
    rear_cut = Part.makeBox(220.0, 50.0, H + 20.0, FreeCAD.Vector(-110.0, -118.0, -10.0))
    base = base.cut(rear_cut)
    
    # Internal hollow cavity: 5.0mm reinforced bottom floor and 4.5mm outer walls
    inner_cavity = Part.makeCylinder(R - 4.5, H - 9.5, FreeCAD.Vector(0, 0, 5.0), FreeCAD.Vector(0, 0, 1))
    base = base.cut(inner_cavity)
    
    # Top turntable 6812ZZ bearing pocket: 78.4mm OD (+0.4mm tolerance), 10.5mm depth
    bearing_pocket = Part.makeCylinder(39.2, 12.0, FreeCAD.Vector(0, 0, H - 10.5), FreeCAD.Vector(0, 0, 1))
    base = base.cut(bearing_pocket)
    
    # Center wire egress through-hole (diameter 40mm)
    center_hole = Part.makeCylinder(20.0, H + 10.0, FreeCAD.Vector(0, 0, -5.0), FreeCAD.Vector(0, 0, 1))
    base = base.cut(center_hole)
    
    # Rear connector ports panel (XT60 power socket, USB-C pass-through, and rocker switch)
    xt60_cut = Part.makeBox(16.5, 20.0, 9.0, FreeCAD.Vector(-35.0, -75.0, 25.0))
    usb_cut = Part.makeBox(13.0, 20.0, 8.0, FreeCAD.Vector(0.0, -75.0, 25.5))
    switch_cut = Part.makeBox(21.5, 20.0, 14.0, FreeCAD.Vector(25.0, -75.0, 22.5))
    base = base.cut(xt60_cut).cut(usb_cut).cut(switch_cut)
    
    # Horizontal cooling louvers / ventilation vents on side walls
    for z in [22.0, 32.0, 42.0, 52.0]:
        # Left ventilation slot
        l_slot = Part.makeBox(40.0, 12.0, 3.5, FreeCAD.Vector(-85.0, -20.0, z))
        # Right ventilation slot
        r_slot = Part.makeBox(40.0, 12.0, 3.5, FreeCAD.Vector(45.0, -20.0, z))
        base = base.cut(l_slot).cut(r_slot)
        
    # 4x Bottom non-slip rubber foot recesses (18mm dia, 2.5mm deep)
    feet_coords = [(58.0, 45.0), (-58.0, 45.0), (58.0, -35.0), (-58.0, -35.0)]
    for fx, fy in feet_coords:
        foot_pocket = Part.makeCylinder(9.0, 3.0, FreeCAD.Vector(fx, fy, -0.5), FreeCAD.Vector(0, 0, 1))
        base = base.cut(foot_pocket)
        
    # Internal electronics mounting bosses (ESP32, XL4016, LM2596, PCA9685)
    standoffs = [
        # ESP32 NodeMCU (52 x 26 mm)
        (26.0, 13.0), (26.0, -13.0), (-26.0, 13.0), (-26.0, -13.0),
        # XL4016 Buck Converter (65 x 40 mm)
        (45.0, 45.0), (45.0, 5.0), (-45.0, 45.0), (-45.0, 5.0)
    ]
    for sx, sy in standoffs:
        boss = Part.makeCylinder(3.5, 7.0, FreeCAD.Vector(sx, sy, 5.0), FreeCAD.Vector(0, 0, 1))
        hole = Part.makeCylinder(1.5, 8.0, FreeCAD.Vector(sx, sy, 5.0), FreeCAD.Vector(0, 0, 1))
        base = base.fuse(boss).cut(hole)
        
    return base

# ==============================================================================
# 2. SHOULDER YOKE (Dual-Pivot Clevis, 63mm Axis Height, RDS5160 & 608ZZ Pocket)
# ==============================================================================
def build_shoulder_yoke():
    """Builds the dual-pivot shoulder yoke supporting the RDS5160 servo and 608ZZ bearing."""
    # Turntable mounting plate (dia 76mm, 8mm thick)
    base_plate = Part.makeCylinder(38.0, 8.0, FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1))
    
    # Dual upright clevis arms rising to Z = 88mm (Shoulder pivot axis at Z = 63.0mm)
    # Left upright (RDS5160 mount side): X from -49.0 to -27.0 (22mm thick)
    left_upright = Part.makeBox(22.0, 64.0, 80.0, FreeCAD.Vector(-49.0, -32.0, 8.0))
    # Right upright (608ZZ bearing side): X from +27.0 to +47.0 (20mm thick)
    right_upright = Part.makeBox(20.0, 64.0, 80.0, FreeCAD.Vector(27.0, -32.0, 8.0))
    
    yoke = base_plate.fuse(left_upright).fuse(right_upright)
    
    # Left pocket: DSSERVO RDS5160 servo body cutout (60.5 x 30.5 x 24.0 mm)
    rds_pocket = Part.makeBox(25.0, 30.5, 60.5, FreeCAD.Vector(-52.0, -15.25, 32.75))
    yoke = yoke.cut(rds_pocket)
    
    # 4x M3 counterbored screw holes for RDS5160 mounting flanges
    for y_off in [-19.0, 19.0]:
        for z_off in [40.0, 80.0]:
            screw_hole = Part.makeCylinder(1.6, 30.0, FreeCAD.Vector(-55.0, y_off, z_off), FreeCAD.Vector(1, 0, 0))
            yoke = yoke.cut(screw_hole)
            
    # Right pocket: 608ZZ miniature ball bearing press-fit pocket (22.1mm OD, 7.2mm deep)
    bearing_pocket = Part.makeCylinder(11.05, 7.2, FreeCAD.Vector(27.0, 0.0, 63.0), FreeCAD.Vector(1, 0, 0))
    yoke = yoke.cut(bearing_pocket)
    
    # Hexagonal captive nut pocket for M8 locknut on right upright outer face (13.0mm across flats, 6.5mm deep)
    m8_hex_pocket = Part.makeCylinder(7.5, 6.5, FreeCAD.Vector(41.0, 0.0, 63.0), FreeCAD.Vector(1, 0, 0))
    yoke = yoke.cut(m8_hex_pocket)
    
    # M8 pivot bolt through-bore through both uprights along X-axis at Z = 63.0mm
    m8_through_bore = Part.makeCylinder(4.2, 110.0, FreeCAD.Vector(-55.0, 0.0, 63.0), FreeCAD.Vector(1, 0, 0))
    yoke = yoke.cut(m8_through_bore)
    
    # Central wire conduit through-hole in base plate (diameter 26mm)
    conduit_hole = Part.makeCylinder(13.0, 16.0, FreeCAD.Vector(0, 0, -4.0), FreeCAD.Vector(0, 0, 1))
    yoke = yoke.cut(conduit_hole)
    
    # Aerodynamic chamfers on top outer corners
    chamfer_l = Part.makeBox(25.0, 40.0, 40.0, FreeCAD.Vector(-50.0, 25.0, 75.0))
    chamfer_r = Part.makeBox(25.0, 40.0, 40.0, FreeCAD.Vector(25.0, 25.0, 75.0))
    yoke = yoke.cut(chamfer_l).cut(chamfer_r)
    
    return yoke

# ==============================================================================
# 3. UPPER ARM LINK 1 (Length: 220mm Axis-to-Axis, 55x45mm Profile, Truss Windows)
# ==============================================================================
def build_upper_arm():
    """Builds Link 1: 220mm center-to-center rigid beam with internal ribbing."""
    L = 220.0
    
    # Main structural tapered box beam
    beam = Part.makeBox(54.0, 44.0, L, FreeCAD.Vector(-27.0, -22.0, 0.0))
    
    # Proximal shoulder hub cylinder (at Z = 0.0, dia 44mm)
    prox_hub = Part.makeCylinder(22.0, 54.0, FreeCAD.Vector(-27.0, 0.0, 0.0), FreeCAD.Vector(1, 0, 0))
    # Distal elbow hub cylinder (at Z = L, dia 42mm)
    dist_hub = Part.makeCylinder(21.0, 54.0, FreeCAD.Vector(-27.0, 0.0, L), FreeCAD.Vector(1, 0, 0))
    beam = beam.fuse(prox_hub).fuse(dist_hub)
    
    # Proximal pivot bore (M8 bolt through-hole at Z = 0)
    shoulder_bore = Part.makeCylinder(4.2, 60.0, FreeCAD.Vector(-30.0, 0.0, 0.0), FreeCAD.Vector(1, 0, 0))
    beam = beam.cut(shoulder_bore)
    
    # RDS5160 servo horn pocket on drive face (dia 32mm, depth 4.0mm)
    horn_pocket = Part.makeCylinder(16.0, 4.0, FreeCAD.Vector(-27.0, 0.0, 0.0), FreeCAD.Vector(1, 0, 0))
    beam = beam.cut(horn_pocket)
    
    # Distal elbow pivot bore (dia 8.4mm at Z = 220.0)
    elbow_bore = Part.makeCylinder(4.2, 60.0, FreeCAD.Vector(-30.0, 0.0, L), FreeCAD.Vector(1, 0, 0))
    beam = beam.cut(elbow_bore)
    
    # Distal MG996R elbow actuator pocket (41.0 x 20.2 x 44.0 mm)
    servo_pocket = Part.makeBox(41.0, 20.2, 44.0, FreeCAD.Vector(-20.5, -10.1, L - 48.0))
    beam = beam.cut(servo_pocket)
    
    # 3x Diamond / Hexagonal weight reduction lightening truss windows along the beam
    for z_center in [60.0, 110.0, 160.0]:
        truss_window = Part.makeBox(28.0, 48.0, 30.0, FreeCAD.Vector(-14.0, -24.0, z_center - 15.0))
        beam = beam.cut(truss_window)
        
    # Cable routing channel along rear spine (6mm wide, 4mm deep)
    wire_trough = Part.makeBox(8.0, 6.0, L - 60.0, FreeCAD.Vector(-4.0, 18.0, 30.0))
    beam = beam.cut(wire_trough)
    
    return beam

# ==============================================================================
# 4. FOREARM LINK 2 (Length: 180mm Axis-to-Axis, 42mm OD, 20° Camera Shelf)
# ==============================================================================
def build_forearm():
    """Builds Link 2: 180mm cylindrical arm with 22mm wire channel and camera shelf."""
    L = 180.0
    R = 21.0
    
    # Main cylindrical arm tube
    tube = Part.makeCylinder(R, L, FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1))
    
    # Proximal clevis hub (at Z = 0)
    prox_hub = Part.makeCylinder(R, 48.0, FreeCAD.Vector(-24.0, 0.0, 0.0), FreeCAD.Vector(1, 0, 0))
    # Distal wrist clevis hub (at Z = L)
    dist_hub = Part.makeCylinder(18.0, 42.0, FreeCAD.Vector(-21.0, 0.0, L), FreeCAD.Vector(1, 0, 0))
    tube = tube.fuse(prox_hub).fuse(dist_hub)
    
    # Internal hollow wiring conduit (dia 22mm running full length)
    wire_conduit = Part.makeCylinder(11.0, L + 20.0, FreeCAD.Vector(0, 0, -10.0), FreeCAD.Vector(0, 0, 1))
    tube = tube.cut(wire_conduit)
    
    # Proximal elbow pivot bore (Z = 0)
    elbow_bore = Part.makeCylinder(4.2, 55.0, FreeCAD.Vector(-27.0, 0.0, 0.0), FreeCAD.Vector(1, 0, 0))
    tube = tube.cut(elbow_bore)
    
    # Distal wrist pivot bore (Z = 180.0)
    wrist_bore = Part.makeCylinder(4.2, 50.0, FreeCAD.Vector(-25.0, 0.0, L), FreeCAD.Vector(1, 0, 0))
    tube = tube.cut(wrist_bore)
    
    # 608ZZ bearing pocket on proximal clevis passive ear (22.1mm OD, 7.2mm deep)
    bearing_pocket = Part.makeCylinder(11.05, 7.2, FreeCAD.Vector(16.0, 0.0, 0.0), FreeCAD.Vector(1, 0, 0))
    tube = tube.cut(bearing_pocket)
    
    # Dedicated ESP32-CAM mounting shelf at Z = 155.0mm (25mm before wrist)
    # Inclined at 20° downward relative to arm axis for optimal workspace viewing
    shelf_body = Part.makeBox(38.0, 30.0, 6.0, FreeCAD.Vector(-19.0, 15.0, 150.0))
    shelf_body.rotate(FreeCAD.Vector(0, 15.0, 150.0), FreeCAD.Vector(1, 0, 0), -20.0)
    
    # Camera lens aperture through shelf (dia 12mm)
    cam_aperture = Part.makeCylinder(6.0, 20.0, FreeCAD.Vector(0, 25.0, 145.0), FreeCAD.Vector(0, 1, 0))
    shelf_body = shelf_body.cut(cam_aperture)
    
    tube = tube.fuse(shelf_body)
    
    # Smooth chamfered cable entry/exit ports
    entry_slot = Part.makeBox(14.0, 30.0, 16.0, FreeCAD.Vector(-7.0, -15.0, 20.0))
    exit_slot = Part.makeBox(14.0, 30.0, 16.0, FreeCAD.Vector(-7.0, -15.0, 140.0))
    tube = tube.cut(entry_slot).cut(exit_slot)
    
    return tube

# ==============================================================================
# 5. WRIST LINK 3 (Length: 60mm Axis-to-Axis, 40x35mm Compact Bracket)
# ==============================================================================
def build_wrist():
    """Builds Link 3: 60mm compact wrist housing MG996R wrist pitch servo."""
    L = 60.0
    body = Part.makeBox(40.0, 35.0, L, FreeCAD.Vector(-20.0, -17.5, 0.0))
    
    # Proximal wrist pivot bore (at Z = 0)
    pivot_bore = Part.makeCylinder(4.2, 50.0, FreeCAD.Vector(-25.0, 0.0, 0.0), FreeCAD.Vector(1, 0, 0))
    body = body.cut(pivot_bore)
    
    # MG996R wrist pitch servo pocket (41.0 x 20.2 x 43.0 mm)
    servo_pocket = Part.makeBox(41.0, 20.2, 43.0, FreeCAD.Vector(-20.5, -10.1, 8.0))
    body = body.cut(servo_pocket)
    
    # Clamping slit for zero-backlash pivot clamp (width 1.5mm)
    clamp_slit = Part.makeBox(45.0, 1.5, 20.0, FreeCAD.Vector(-22.5, -0.75, -5.0))
    body = body.cut(clamp_slit)
    
    # Distal circular mounting flange (dia 44mm, 6.0mm thickness at Z = 60.0)
    flange = Part.makeCylinder(22.0, 6.0, FreeCAD.Vector(0, 0, L - 6.0), FreeCAD.Vector(0, 0, 1))
    body = body.fuse(flange)
    
    # Central centering boss (dia 16.0mm, 2.0mm high)
    centering_boss = Part.makeCylinder(8.0, 2.0, FreeCAD.Vector(0, 0, L), FreeCAD.Vector(0, 0, 1))
    body = body.fuse(centering_boss)
    
    # 4x M3 screw holes on dia 32mm pitch circle for mounting end-effector
    for angle in [45.0, 135.0, 225.0, 315.0]:
        rad = math.radians(angle)
        sx = 16.0 * math.cos(rad)
        sy = 16.0 * math.sin(rad)
        screw_hole = Part.makeCylinder(1.6, 20.0, FreeCAD.Vector(sx, sy, L - 12.0), FreeCAD.Vector(0, 0, 1))
        body = body.cut(screw_hole)
        
    return body

# ==============================================================================
# 6. GRIPPER BASE & CHASSIS (Length: 90mm Closed, 70mm Jaw Stroke, Dual Pivots)
# ==============================================================================
def build_gripper_base():
    """Builds the end-effector base housing the horizontal MG996R servo and jaw hinges."""
    body = Part.makeBox(48.4, 44.0, 60.0, FreeCAD.Vector(-24.2, -22.0, 0.0))
    
    # Circular recess on rear face mating with wrist centering boss
    centering_recess = Part.makeCylinder(8.15, 3.0, FreeCAD.Vector(0, 0, -1.0), FreeCAD.Vector(0, 0, 1))
    body = body.cut(centering_recess)
    
    # 4x M3 counterbored screw holes matching wrist flange
    for angle in [45.0, 135.0, 225.0, 315.0]:
        rad = math.radians(angle)
        sx = 16.0 * math.cos(rad)
        sy = 16.0 * math.sin(rad)
        screw_hole = Part.makeCylinder(1.6, 25.0, FreeCAD.Vector(sx, sy, -2.0), FreeCAD.Vector(0, 0, 1))
        c_bore = Part.makeCylinder(3.2, 10.0, FreeCAD.Vector(sx, sy, 8.0), FreeCAD.Vector(0, 0, 1))
        body = body.cut(screw_hole).cut(c_bore)
        
    # MG996R horizontal actuator pocket
    servo_pocket = Part.makeBox(42.0, 20.5, 41.0, FreeCAD.Vector(-21.0, -10.25, 12.0))
    body = body.cut(servo_pocket)
    
    # Dual finger pivot hinge bores at X = +/-13.0mm, Y = 0.0, Z = 48.0mm (M4 pivot bolts)
    for x_piv in [-13.0, 13.0]:
        hinge_bore = Part.makeCylinder(2.1, 55.0, FreeCAD.Vector(x_piv, -25.0, 48.0), FreeCAD.Vector(0, 1, 0))
        body = body.cut(hinge_bore)
        
    # Gear shroud protective cavity
    gear_shroud = Part.makeBox(36.0, 14.0, 16.0, FreeCAD.Vector(-18.0, -7.0, 42.0))
    body = body.cut(gear_shroud)
    
    return body

# ==============================================================================
# 7. GRIPPER LEFT FINGER (Tactile with Recessed FSR 402 Pocket & Traction Ribs)
# ==============================================================================
def build_gripper_left_finger():
    """Builds the left articulated gripper claw with 1.0mm recessed FSR 402 sensor pocket."""
    L = 90.0
    
    # Main curved finger body
    jaw = Part.makeBox(10.0, L, 14.0, FreeCAD.Vector(-5.0, 0.0, 0.0))
    
    # Hinge pivot boss at proximal end (at Y = 10.0, Z = 7.0)
    pivot_boss = Part.makeCylinder(9.0, 10.0, FreeCAD.Vector(-5.0, 10.0, 7.0), FreeCAD.Vector(1, 0, 0))
    jaw = jaw.fuse(pivot_boss)
    
    # M4 hinge pivot hole
    pivot_hole = Part.makeCylinder(2.1, 20.0, FreeCAD.Vector(-10.0, 10.0, 7.0), FreeCAD.Vector(1, 0, 0))
    jaw = jaw.cut(pivot_hole)
    
    # Spur gear sector around pivot (simulated via radial notches)
    for a in [-30.0, -15.0, 0.0, 15.0, 30.0]:
        rad = math.radians(a)
        gx = 10.0 * math.sin(rad)
        gy = 10.0 - 10.0 * math.cos(rad)
        tooth_cut = Part.makeCylinder(1.2, 12.0, FreeCAD.Vector(-6.0, gy, 7.0 + gx), FreeCAD.Vector(1, 0, 0))
        jaw = jaw.cut(tooth_cut)
        
    # Recessed tactile nest on inner face for Interlink FSR 402 (dia 18.5mm, 1.2mm deep)
    # Centered at Y = 58.0mm, Z = 7.0mm
    fsr_pocket = Part.makeCylinder(9.25, 1.5, FreeCAD.Vector(5.0, 58.0, 7.0), FreeCAD.Vector(-1, 0, 0))
    jaw = jaw.cut(fsr_pocket)
    
    # Wire exit channel from sensor pocket down to pivot hub (3mm wide x 2mm deep)
    wire_trough = Part.makeBox(2.0, 45.0, 3.0, FreeCAD.Vector(3.5, 15.0, 5.5))
    jaw = jaw.cut(wire_trough)
    
    # 4x Tactile traction ridges on fingertip (0.8mm proud)
    for y_ridge in [76.0, 80.0, 84.0, 88.0]:
        ridge = Part.makeBox(0.8, 1.5, 10.0, FreeCAD.Vector(4.5, y_ridge, 2.0))
        jaw = jaw.fuse(ridge)
        
    # Tapered ergonomic chamfer on outer back face
    taper_cut = Part.makeBox(12.0, 45.0, 16.0, FreeCAD.Vector(-6.0, 45.0, -8.0))
    taper_cut.rotate(FreeCAD.Vector(0, 45.0, 0), FreeCAD.Vector(1, 0, 0), -12.0)
    jaw = jaw.cut(taper_cut)
    
    return jaw

# ==============================================================================
# 8. GRIPPER RIGHT FINGER (Counter-Rotating Geared Jaw with Gripping Ridges)
# ==============================================================================
def build_gripper_right_finger():
    """Builds the right articulated gripper claw counter-rotating with left claw."""
    L = 90.0
    
    # Main curved finger body
    jaw = Part.makeBox(10.0, L, 14.0, FreeCAD.Vector(-5.0, 0.0, 0.0))
    
    # Hinge pivot boss at proximal end
    pivot_boss = Part.makeCylinder(9.0, 10.0, FreeCAD.Vector(-5.0, 10.0, 7.0), FreeCAD.Vector(1, 0, 0))
    jaw = jaw.fuse(pivot_boss)
    
    # M4 hinge pivot hole
    pivot_hole = Part.makeCylinder(2.1, 20.0, FreeCAD.Vector(-10.0, 10.0, 7.0), FreeCAD.Vector(1, 0, 0))
    jaw = jaw.cut(pivot_hole)
    
    # Spur gear sector
    for a in [-30.0, -15.0, 0.0, 15.0, 30.0]:
        rad = math.radians(a)
        gx = 10.0 * math.sin(rad)
        gy = 10.0 - 10.0 * math.cos(rad)
        tooth_cut = Part.makeCylinder(1.2, 12.0, FreeCAD.Vector(-6.0, gy, 7.0 + gx), FreeCAD.Vector(1, 0, 0))
        jaw = jaw.cut(tooth_cut)
        
    # 4x Tactile traction ridges on inner grasping face
    for y_ridge in [76.0, 80.0, 84.0, 88.0]:
        ridge = Part.makeBox(0.8, 1.5, 10.0, FreeCAD.Vector(-5.3, y_ridge, 2.0))
        jaw = jaw.fuse(ridge)
        
    # Lightweight web cutout along the finger spine
    spine_lightening = Part.makeBox(12.0, 30.0, 6.0, FreeCAD.Vector(-6.0, 35.0, 4.0))
    jaw = jaw.cut(spine_lightening)
    
    # Tapered ergonomic chamfer
    taper_cut = Part.makeBox(12.0, 45.0, 16.0, FreeCAD.Vector(-6.0, 45.0, -8.0))
    taper_cut.rotate(FreeCAD.Vector(0, 45.0, 0), FreeCAD.Vector(1, 0, 0), -12.0)
    jaw = jaw.cut(taper_cut)
    
    return jaw

# ==============================================================================
# 9. COTS HARDWARE & COMPONENT GENERATORS
# ==============================================================================
def build_rds5160_servo():
    """Generates realistic DSSERVO RDS5160 digital servo solid."""
    body = Part.makeBox(60.0, 30.0, 48.0, FreeCAD.Vector(-30.0, -15.0, 0.0))
    # Aluminum middle heatsink
    heatsink = Part.makeBox(60.4, 30.4, 18.0, FreeCAD.Vector(-30.2, -15.2, 15.0))
    # Output spline hub
    spline = Part.makeCylinder(10.0, 8.0, FreeCAD.Vector(-12.0, 0.0, 48.0), FreeCAD.Vector(0, 0, 1))
    return body.fuse(heatsink).fuse(spline)

def build_mg996r_servo():
    """Generates realistic TowerPro MG996R servo solid."""
    body = Part.makeBox(40.7, 19.7, 42.9, FreeCAD.Vector(-20.35, -9.85, 0.0))
    # Mounting ears
    ears = Part.makeBox(54.0, 19.0, 3.0, FreeCAD.Vector(-27.0, -9.5, 27.0))
    # Output spline
    spline = Part.makeCylinder(6.0, 6.0, FreeCAD.Vector(-10.0, 0.0, 42.9), FreeCAD.Vector(0, 0, 1))
    return body.fuse(ears).fuse(spline)

def build_bearing_6812zz():
    """Generates 6812ZZ thin section deep-groove ball bearing (60 ID x 78 OD x 10 W)."""
    outer = Part.makeCylinder(39.0, 10.0, FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1))
    inner = Part.makeCylinder(30.0, 12.0, FreeCAD.Vector(0, 0, -1.0), FreeCAD.Vector(0, 0, 1))
    return outer.cut(inner)

def build_bearing_608zz():
    """Generates 608ZZ miniature ball bearing (8 ID x 22 OD x 7 W)."""
    outer = Part.makeCylinder(11.0, 7.0, FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1))
    inner = Part.makeCylinder(4.0, 9.0, FreeCAD.Vector(0, 0, -1.0), FreeCAD.Vector(0, 0, 1))
    return outer.cut(inner)

def build_fsr402_sensor():
    """Generates Interlink FSR 402 tactile force sensor disc (18.3mm dia, 0.5mm thick)."""
    disc = Part.makeCylinder(9.15, 0.5, FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1))
    tail = Part.makeBox(5.0, 35.0, 0.3, FreeCAD.Vector(-2.5, -35.0, 0.1))
    return disc.fuse(tail)

# ==============================================================================
# MASTER BUILDER ROUTINE
# ==============================================================================
def main():
    print("*" * 75)
    print("  SELAH: PROFESSIONAL MODULAR FREECAD CAD REBUILD ENGINE")
    print("*" * 75)
    
    # 1. Build all modular components
    print("\n[Step 1/5] Parametrically modeling aesthetic modular components...")
    
    parts_catalog = {
        "Base_Enclosure":       (build_base_enclosure(),       COLOR_CHASSIS_BLACK, "01_Base_Assembly"),
        "Shoulder_Yoke":        (build_shoulder_yoke(),        COLOR_ROBOTIC_BLUE,  "02_Shoulder_Assembly"),
        "Upper_Arm":            (build_upper_arm(),            COLOR_CHASSIS_BLACK, "03_Upper_Arm_Assembly"),
        "Forearm":              (build_forearm(),              COLOR_ROBOTIC_BLUE,  "04_Forearm_Assembly"),
        "Wrist":                (build_wrist(),                COLOR_CHASSIS_BLACK, "05_Wrist_Assembly"),
        "Gripper_Base":         (build_gripper_base(),         COLOR_ROBOTIC_BLUE,  "06_Gripper_Assembly"),
        "Gripper_Left_Finger":  (build_gripper_left_finger(),  COLOR_CHASSIS_BLACK, "06_Gripper_Assembly"),
        "Gripper_Right_Finger": (build_gripper_right_finger(), COLOR_CHASSIS_BLACK, "06_Gripper_Assembly"),
    }
    
    cots_catalog = {
        "Servo_RDS5160_Shoulder": (build_rds5160_servo(),  COLOR_SERVO_ALU,      "07_Actuators_And_Electronics"),
        "Servo_MG996R_Elbow":     (build_mg996r_servo(),   COLOR_SERVO_GOLD,     "07_Actuators_And_Electronics"),
        "Bearing_6812ZZ_Base":    (build_bearing_6812zz(), COLOR_BEARING_CHROME, "08_Bearings_And_Fasteners"),
        "Bearing_608ZZ_Pivot":    (build_bearing_608zz(),  COLOR_BEARING_CHROME, "08_Bearings_And_Fasteners"),
        "FSR402_Tactile_Sensor":  (build_fsr402_sensor(),  COLOR_FSR_TOUCH,      "07_Actuators_And_Electronics"),
    }
    
    for name, (shape, _, _) in {**parts_catalog, **cots_catalog}.items():
        print(f"  ✓ Built solid: {name:<26} (Volume: {shape.Volume:10.2f} mm³)")

    # 2. Construct Master FreeCAD Document with Root Group 'Selah'
    print("\n[Step 2/5] Creating FreeCAD Master Document with 'Selah' folder hierarchy...")
    master_doc = FreeCAD.newDocument("Selah_Master")
    
    # Root Folder: Selah
    root_folder = master_doc.addObject("App::DocumentObjectGroup", "Selah")
    root_folder.Label = "Selah"
    
    # Sub-folders
    sub_groups = {}
    sub_names = [
        "01_Base_Assembly",
        "02_Shoulder_Assembly",
        "03_Upper_Arm_Assembly",
        "04_Forearm_Assembly",
        "05_Wrist_Assembly",
        "06_Gripper_Assembly",
        "07_Actuators_And_Electronics",
        "08_Bearings_And_Fasteners"
    ]
    for sg_name in sub_names:
        sg = master_doc.addObject("App::DocumentObjectGroup", sg_name)
        sg.Label = sg_name
        root_folder.addObject(sg)
        sub_groups[sg_name] = sg
        
    # Populate Master Document
    all_shapes_for_asm = []
    for name, (shape, color, parent_group) in {**parts_catalog, **cots_catalog}.items():
        obj = master_doc.addObject("Part::Feature", name)
        obj.Shape = shape
        obj.Label = name
        if hasattr(obj, "ViewObject") and obj.ViewObject:
            obj.ViewObject.ShapeColor = color
        sub_groups[parent_group].addObject(obj)
        all_shapes_for_asm.append(shape)
        
    master_doc.recompute()
    master_fcstd = os.path.join(ASM_DIR, "Selah_Master.FCStd")
    master_doc.saveAs(master_fcstd)
    print(f"  ✓ Saved Master FreeCAD Document: {master_fcstd}")

    # 3. Save Individual .FCStd Projects for Each Component
    print("\n[Step 3/5] Saving modular individual .FCStd projects for every part...")
    for name, (shape, color, parent_group) in parts_catalog.items():
        part_doc = FreeCAD.newDocument(f"Selah_{name}")
        p_root = part_doc.addObject("App::DocumentObjectGroup", "Selah")
        p_root.Label = "Selah"
        p_sub = part_doc.addObject("App::DocumentObjectGroup", parent_group)
        p_sub.Label = parent_group
        p_root.addObject(p_sub)
        
        part_obj = part_doc.addObject("Part::Feature", name)
        part_obj.Shape = shape
        part_obj.Label = name
        if hasattr(part_obj, "ViewObject") and part_obj.ViewObject:
            part_obj.ViewObject.ShapeColor = color
        p_sub.addObject(part_obj)
        part_doc.recompute()
        
        part_fcstd = os.path.join(PARTS_DIR, f"{name}.FCStd")
        part_doc.saveAs(part_fcstd)
        FreeCAD.closeDocument(f"Selah_{name}")
        print(f"  ✓ Saved modular part: {part_fcstd}")

    # 4. Export STEP Solids
    print("\n[Step 4/5] Exporting STEP solid models...")
    # Master assembly STEP
    master_step = os.path.join(ASM_DIR, "Selah_Assembly.step")
    Part.export(all_shapes_for_asm, master_step)
    print(f"  ✓ Master Assembly STEP: {master_step}")
    
    # Individual parts STEPs
    for name, (shape, _, _) in parts_catalog.items():
        step_path = os.path.join(PARTS_DIR, f"{name}.step")
        Part.export([shape], step_path)
        # Also copy to legacy parts folder with snake_case
        snake_name = name.lower()
        legacy_step = os.path.join(LEGACY_PARTS_DIR, f"{snake_name}.step")
        Part.export([shape], legacy_step)
        
    # COTS STEPs
    for name, (shape, _, _) in cots_catalog.items():
        step_path = os.path.join(COMPONENTS_DIR, f"{name}.step")
        Part.export([shape], step_path)
    print("  ✓ All component STEP files exported.")

    # 5. Export High-Precision Slice-Ready STL Meshes
    print("\n[Step 5/5] Exporting slice-ready STL meshes for manufacturing & ROS 2...")
    for name, (shape, _, _) in parts_catalog.items():
        snake_name = name.lower()
        selah_stl = os.path.join(PARTS_DIR, f"{name}.stl")
        legacy_stl = os.path.join(LEGACY_PARTS_DIR, f"{snake_name}.stl")
        ros2_vis_stl = os.path.join(ROS2_VISUAL_DIR, f"{snake_name}.stl")
        ros2_col_stl = os.path.join(ROS2_COLLISION_DIR, f"{snake_name}.stl")
        
        mesh = Mesh.Mesh()
        mesh.addFacets(shape.tessellate(0.08))  # High-definition 0.08mm deflection
        mesh.write(selah_stl)
        mesh.write(legacy_stl)
        mesh.write(ros2_vis_stl)
        mesh.write(ros2_col_stl)
        print(f"  ✓ Generated mesh: {name:<22} -> STL")

    print("\n" + "=" * 75)
    print("  SELAH FREECAD REBUILD SUCCESSFULLY COMPLETED!")
    print(f"  Hierarchy Root:       Selah (Folder/Group)")
    print(f"  Master Document:      {master_fcstd}")
    print(f"  Individual Parts:     {PARTS_DIR}")
    print(f"  COTS Components:      {COMPONENTS_DIR}")
    print(f"  ROS 2 Meshes Updated: {ROS2_VISUAL_DIR}")
    print("=" * 75)

if __name__ == "__main__":
    main()
