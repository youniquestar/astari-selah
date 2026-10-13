import cadquery as cq

# ==============================================================================
# PARAMETRIC BASE DIMENSIONS & CLEARANCES (All units in mm)
# ==============================================================================

# 1. Global Shell Enclosure (As requested in prompt)
BASE_RADIUS = 90.0             # 180mm total diameter across front arc
BAY_DEPTH = 130.0              # Extends along -Y from origin (Y=0 to Y=-130)
BAY_WIDTH = 180.0              # Matches semicircle width (X: -90 to +90)
TOTAL_HEIGHT = 85.0            # Adjusted to 85.0mm per .antigravity_rules
FLOOR_THICKNESS = 5.0          # Structural bottom plate
WALL_THICKNESS = 4.0           # Exterior perimeter wall thickness

# 2. 6812ZZ Bearing Interface (Top Roof Center: X=0, Y=0)
BEARING_POCKET_DIA = 78.4      # 78.0mm nominal OD + 0.4mm 3D-print tolerance
BEARING_POCKET_DEPTH = 9.5     # 0.5mm lip exposure to prevent turntable friction
BEARING_WIRE_THRU_DIA = 60.0   # Hollow passthrough core matching bearing ID

# 3. Central Actuator Pillar (DSSERVO RDS5160 per .antigravity_rules)
PILLAR_WIDTH = 84.0            # Outer X dimension of central pillar
PILLAR_DEPTH = 44.0            # Outer Y dimension of central pillar
PILLAR_HEIGHT = 70.0           # Height from top of base floor (maintaining 10mm roof gap)
SERVO_CUTOUT_X = 60.4          # 60.0mm body + 0.4mm clearance
SERVO_CUTOUT_Y = 30.4          # 30.0mm body + 0.4mm clearance
SERVO_BOLT_PITCH_X = 74.0      # Flange mounting screw pitch (length-wise)
SERVO_BOLT_PITCH_Y = 10.0      # Flange mounting screw pitch (width-wise)
PILOT_HOLE_M3 = 2.8            # Self-tapping hole for M3 screws

# 4. Electronics Mounting Standoff Parameters (Height above floor: 5.0mm)
STANDOFF_HEIGHT = 5.0
STANDOFF_OD = 6.0

# ESP32 NodeMCU (Right Wall: X: +52 to +80, Y: -26 to +26)
ESP32_CENTER_X = 64.0
ESP32_CENTER_Y = 0.0
ESP32_HOLE_SPACING_X = 23.0    
ESP32_HOLE_SPACING_Y = 47.0    

# XL4016 Buck Converter (Left Wall: X: -80 to -30, Y: -30.5 to +30.5)
XL4016_CENTER_X = -55.0
XL4016_CENTER_Y = 0.0
XL4016_HOLE_SPACING_X = 43.0
XL4016_HOLE_SPACING_Y = 54.0

# LM2596 Buck Converter (Front Clear Space: X: ~0, Y: +45 to +66)
LM2596_CENTER_X = 0.0
LM2596_CENTER_Y = 52.0
LM2596_HOLE_SPACING_X = 35.0
LM2596_HOLE_SPACING_Y = 15.0

# PCA9685 16-channel I2C PWM driver (Rear Clear Space: Y: -40 to -70)
PCA9685_CENTER_X = 0.0
PCA9685_CENTER_Y = -55.0
PCA9685_HOLE_SPACING_X = 56.0
PCA9685_HOLE_SPACING_Y = 19.0

# 5. 3S LiPo Battery Retaining Bay (Far Rear Wall)
LIPO_INNER_X = 78.0            # 75mm length + 3.0mm swell buffer
LIPO_INNER_Y = 38.0            # 35mm width + 3.0mm swell buffer
LIPO_WALL_THICK = 3.0
LIPO_BRACKET_HEIGHT = 15.0

# ==============================================================================
# 1. GENERATE MONOLITHIC D-PROFILE SOLID BLANK
# ==============================================================================
# Semicircle at front (Y >= 0) and rectangle at rear (Y <= 0)
d_profile = (
    cq.Workplane("XY")
    .moveTo(-BASE_RADIUS, 0)
    .threePointArc((0, BASE_RADIUS), (BASE_RADIUS, 0))
    .lineTo(BASE_RADIUS, -BAY_DEPTH)
    .lineTo(-BASE_RADIUS, -BAY_DEPTH)
    .close()
    .extrude(TOTAL_HEIGHT)
)

# Smooth outer rear corners (R15.0) to prevent peeling/warping
d_profile = (
    d_profile.edges("|Z and <Y")
    .fillet(15.0)
)

# ==============================================================================
# 2. SHELL INTERNAL CAVITY (Preserving Solid 5.0mm Floor & Roof Plate)
# ==============================================================================
inner_radius = BASE_RADIUS - WALL_THICKNESS
inner_depth = BAY_DEPTH - WALL_THICKNESS
inner_fillet = 15.0 - WALL_THICKNESS

cavity = (
    cq.Workplane("XY")
    .workplane(offset=FLOOR_THICKNESS)
    .moveTo(-inner_radius, 0)
    .threePointArc((0, inner_radius), (inner_radius, 0))
    .lineTo(inner_radius, -inner_depth)
    .lineTo(-inner_radius, -inner_depth)
    .close()
    .extrude(TOTAL_HEIGHT - FLOOR_THICKNESS - 4.0) # Leaves 4.0mm structural top roof
)

# Fillet the inner corners to maintain uniform wall thickness
cavity = (
    cavity.edges("|Z and <Y")
    .fillet(inner_fillet)
)

base_shell = d_profile.cut(cavity)

# ==============================================================================
# 3. 6812ZZ BEARING SEAT & AXIAL WIRE PASSTHROUGH (TOP ROOF)
# ==============================================================================
base_shell = (
    base_shell.faces(">Z")
    .workplane()
    # Outer race pocket recessed -9.5mm deep
    .circle(BEARING_POCKET_DIA / 2.0)
    .cutBlind(-BEARING_POCKET_DEPTH)
    # Central wire through-hole completely punching into the main cavity
    .circle(BEARING_WIRE_THRU_DIA / 2.0)
    .cutThruAll()
)

# ==============================================================================
# 4. CENTRAL SERVO PILLAR & DROP-IN MOUNT
# ==============================================================================
# Pillar body built upward from top of floor (Z = FLOOR_THICKNESS)
pillar = (
    cq.Workplane("XY")
    .workplane(offset=FLOOR_THICKNESS)
    .rect(PILLAR_WIDTH, PILLAR_DEPTH)
    .extrude(PILLAR_HEIGHT)
)

# Cut motor body drop-in pocket from top of pillar
pillar = (
    pillar.faces(">Z")
    .workplane()
    .rect(SERVO_CUTOUT_X, SERVO_CUTOUT_Y)
    .cutBlind(-PILLAR_HEIGHT)
)

# Servo flange M3 tapping pilot holes
flange_holes = [
    ( SERVO_BOLT_PITCH_X / 2.0,  SERVO_BOLT_PITCH_Y / 2.0),
    (-SERVO_BOLT_PITCH_X / 2.0,  SERVO_BOLT_PITCH_Y / 2.0),
    ( SERVO_BOLT_PITCH_X / 2.0, -SERVO_BOLT_PITCH_Y / 2.0),
    (-SERVO_BOLT_PITCH_X / 2.0, -SERVO_BOLT_PITCH_Y / 2.0),
]

pillar = (
    pillar.faces(">Z")
    .workplane()
    .pushPoints(flange_holes)
    .hole(PILOT_HOLE_M3, depth=12.0)
)

# Fuse pillar into base chassis
base_shell = base_shell.union(pillar)

# ==============================================================================
# 5. REAR ELECTRONICS STANDOFFS & BATTERY RETAINER
# ==============================================================================
def create_standoff_pair(pts):
    return (
        cq.Workplane("XY")
        .workplane(offset=FLOOR_THICKNESS)
        .pushPoints(pts)
        .circle(STANDOFF_OD / 2.0)
        .extrude(STANDOFF_HEIGHT)
        .faces(">Z")
        .workplane()
        .pushPoints(pts)
        .hole(PILOT_HOLE_M3, depth=STANDOFF_HEIGHT)
    )

# A. ESP32 NodeMCU Standoffs (Right Side)
esp_pts = [
    (ESP32_CENTER_X + ESP32_HOLE_SPACING_X / 2.0, ESP32_CENTER_Y + ESP32_HOLE_SPACING_Y / 2.0),
    (ESP32_CENTER_X - ESP32_HOLE_SPACING_X / 2.0, ESP32_CENTER_Y + ESP32_HOLE_SPACING_Y / 2.0),
    (ESP32_CENTER_X + ESP32_HOLE_SPACING_X / 2.0, ESP32_CENTER_Y - ESP32_HOLE_SPACING_Y / 2.0),
    (ESP32_CENTER_X - ESP32_HOLE_SPACING_X / 2.0, ESP32_CENTER_Y - ESP32_HOLE_SPACING_Y / 2.0),
]
base_shell = base_shell.union(create_standoff_pair(esp_pts))

# B. XL4016 Servo Buck Regulator Standoffs (Left Side)
xl_pts = [
    (XL4016_CENTER_X + XL4016_HOLE_SPACING_X / 2.0, XL4016_CENTER_Y + XL4016_HOLE_SPACING_Y / 2.0),
    (XL4016_CENTER_X - XL4016_HOLE_SPACING_X / 2.0, XL4016_CENTER_Y + XL4016_HOLE_SPACING_Y / 2.0),
    (XL4016_CENTER_X + XL4016_HOLE_SPACING_X / 2.0, XL4016_CENTER_Y - XL4016_HOLE_SPACING_Y / 2.0),
    (XL4016_CENTER_X - XL4016_HOLE_SPACING_X / 2.0, XL4016_CENTER_Y - XL4016_HOLE_SPACING_Y / 2.0),
]
base_shell = base_shell.union(create_standoff_pair(xl_pts))

# C. LM2596 Logic Regulator Standoffs (Front Semicircle Deck)
lm_pts = [
    (LM2596_CENTER_X + LM2596_HOLE_SPACING_X / 2.0, LM2596_CENTER_Y + LM2596_HOLE_SPACING_Y / 2.0),
    (LM2596_CENTER_X - LM2596_HOLE_SPACING_X / 2.0, LM2596_CENTER_Y + LM2596_HOLE_SPACING_Y / 2.0),
    (LM2596_CENTER_X + LM2596_HOLE_SPACING_X / 2.0, LM2596_CENTER_Y - LM2596_HOLE_SPACING_Y / 2.0),
    (LM2596_CENTER_X - LM2596_HOLE_SPACING_X / 2.0, LM2596_CENTER_Y - LM2596_HOLE_SPACING_Y / 2.0),
]
base_shell = base_shell.union(create_standoff_pair(lm_pts))

# D. PCA9685 16-channel I2C PWM driver Standoffs (Rear Open Deck)
pca_pts = [
    (PCA9685_CENTER_X + PCA9685_HOLE_SPACING_X / 2.0, PCA9685_CENTER_Y + PCA9685_HOLE_SPACING_Y / 2.0),
    (PCA9685_CENTER_X - PCA9685_HOLE_SPACING_X / 2.0, PCA9685_CENTER_Y + PCA9685_HOLE_SPACING_Y / 2.0),
    (PCA9685_CENTER_X + PCA9685_HOLE_SPACING_X / 2.0, PCA9685_CENTER_Y - PCA9685_HOLE_SPACING_Y / 2.0),
    (PCA9685_CENTER_X - PCA9685_HOLE_SPACING_X / 2.0, PCA9685_CENTER_Y - PCA9685_HOLE_SPACING_Y / 2.0),
]
base_shell = base_shell.union(create_standoff_pair(pca_pts))

# E. 3S LiPo Battery Retaining Walls (Far Back Center)
lipo_outer_x = LIPO_INNER_X + (2 * LIPO_WALL_THICK)
lipo_outer_y = LIPO_INNER_Y + LIPO_WALL_THICK
lipo_outer_center_y = -BAY_DEPTH + WALL_THICKNESS + (lipo_outer_y / 2.0)

battery_wall = (
    cq.Workplane("XY")
    .workplane(offset=FLOOR_THICKNESS)
    .moveTo(0, lipo_outer_center_y)
    .rect(lipo_outer_x, lipo_outer_y)
    .extrude(LIPO_BRACKET_HEIGHT)
    .faces(">Z")
    .workplane()
    # Shift cutout +Y to ensure exactly 3.0mm wall at the back and a fully open front
    .moveTo(0, lipo_outer_center_y + 5.0)
    .rect(LIPO_INNER_X, LIPO_INNER_Y + 10.0)
    .cutBlind(-LIPO_BRACKET_HEIGHT)
)
base_shell = base_shell.union(battery_wall)

# ==============================================================================
# 6. EXTERNAL I/O WINDOW & PASSIVE THERMAL VENTS
# ==============================================================================
# USB Flashing Window (Right Wall at X = +90, aligned with ESP32)
usb_cutout = (
    cq.Workplane("YZ")
    .workplane(offset=BASE_RADIUS - WALL_THICKNESS - 2.0)
    .moveTo(ESP32_CENTER_Y, FLOOR_THICKNESS + STANDOFF_HEIGHT + 4.0)
    .rect(14.0, 8.0)
    .extrude(WALL_THICKNESS + 6.0)
)
base_shell = base_shell.cut(usb_cutout)

# Passive Cooling Slots for XL4016 (Left Wall at X = -90)
for y_offset in [-20.0, -10.0, 0.0, 10.0, 20.0]:
    vent_slot = (
        cq.Workplane("YZ")
        .workplane(offset=-BASE_RADIUS - 2.0)
        .moveTo(XL4016_CENTER_Y + y_offset, 30.0)
        .rect(4.0, 20.0)
        .extrude(WALL_THICKNESS + 6.0)
    )
    base_shell = base_shell.cut(vent_slot)

# Thermal Louvers for Central RDS5160 Servo Pillar
for z_offset in [20.0, 35.0, 50.0]:
    # Left and Right walls of the pillar
    side_louver = (
        cq.Workplane("YZ")
        .workplane(offset=-PILLAR_WIDTH/2 - 2.0)
        .moveTo(0, z_offset)
        .rect(30.0, 6.0)
        .extrude(PILLAR_WIDTH + 4.0)
    )
    base_shell = base_shell.cut(side_louver)
    
    # Front wall of the pillar
    front_louver = (
        cq.Workplane("XZ")
        .workplane(offset=PILLAR_DEPTH/2 + 2.0)
        .moveTo(0, z_offset)
        .rect(50.0, 6.0)
        .extrude(-15.0) # Plunge into the front wall
    )
    base_shell = base_shell.cut(front_louver)

# Rear Exhaust Vents near PCA9685 (Left and Right Flat Walls)
for y_offset in [-70.0, -55.0, -40.0]:
    for z_offset in [30.0, 45.0, 60.0]:
        rear_vent = (
            cq.Workplane("YZ")
            .workplane(offset=-BASE_RADIUS - 2.0)
            .moveTo(y_offset, z_offset)
            .rect(10.0, 4.0)
            .extrude(BAY_WIDTH + 4.0) # Cuts through both left and right outer walls
        )
        base_shell = base_shell.cut(rear_vent)


# ==============================================================================
# EXPORT OUTPUTS
# ==============================================================================
if __name__ == "__main__":
    import os
    export_dir = os.path.expanduser("~/ros2_ws/src/five_dof_arm_description/cad_export/base_enclosure_fused_assembly")
    os.makedirs(export_dir, exist_ok=True)

    step_path = os.path.join(export_dir, "base_enclosure_fused.step")
    stl_path = os.path.join(export_dir, "base_enclosure_fused.stl")

    cq.exporters.export(base_shell, step_path)
    cq.exporters.export(base_shell, stl_path)
    print(f"[CAD Export] Successfully generated:")
    print(f" - STEP: {step_path}")
    print(f" - STL:  {stl_path}")
