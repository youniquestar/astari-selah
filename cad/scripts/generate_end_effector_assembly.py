import cadquery as cq
import os

# ==============================================================================
# PARAMETRIC SPECIFICATIONS & CLEARANCES (Units: mm)
# ==============================================================================

# 1. Structural Envelope (PETG)
CLAW_LENGTH = 90.0            # Total length of the gripper claw from pivot
CLAW_THICKNESS = 10.0         # Thickness for rigid grasping

# 2. Haptic Force Sensor Interface (FSR 402)
FSR_POCKET_DIA = 19.0
FSR_POCKET_DEPTH = 1.0
FSR_Z_CENTER = 75.0           # Center of FSR near the tip

# 3. Gear Mechanism & Pivots
PIVOT_DISTANCE = 25.0         # Distance between left and right pivots
GEAR_PITCH_RADIUS = PIVOT_DISTANCE / 2.0  # 12.5mm
GEAR_MODULE = 2.5             # Module 2.5 -> 10 teeth for full gear
SERVO_HORN_DIA = 25.4         # MG996R round horn
SERVO_HORN_DEPTH = 2.0

# 4. Gripper Base (Mates to Link 3)
LINK3_WIDTH = 40.0
LINK3_HEIGHT = 35.0
SLEEVE_Z_START = 60.0
SLEEVE_Z_END = 80.0
BASE_Z_END = 120.0
BASE_W = 48.4                 # Outer width (X: -24.2 to 24.2)
BASE_H = 43.4                 # Outer height (Y: -21.7 to 21.7)

# Servo Position in Gripper Base (Offset to place left pivot at X=-12.5)
SERVO_X = -12.5
SERVO_Z = 95.0
SERVO_Y = 0.0                 # Center vertically
SERVO_SPLINE_Z = 105.5        # Spline is 10.5mm offset from center

# ==============================================================================
# 1. GRIPPER BASE MODULE
# ==============================================================================

# Solid bounding box
base_body = (
    cq.Workplane("XY")
    .rect(BASE_W, BASE_H)
    .extrude(BASE_Z_END)
)

# Hollow out the space from Z=0 to Z=60 (Link 3 free space)
cut_0_60 = cq.Workplane("XY").rect(BASE_W+2, BASE_H+2).extrude(60.0)
base_body = base_body.cut(cut_0_60)

# Inner sleeve to slip over Link 3 (Z=59 to 81 for clearance)
sleeve_inner = (
    cq.Workplane("XY")
    .workplane(offset=59.0)
    .rect(LINK3_WIDTH + 0.4, LINK3_HEIGHT + 0.4) # 0.2mm tolerance
    .extrude(22.0)
)
base_body = base_body.cut(sleeve_inner)

# Wire routing channel straight into Link 3's 14mm core
wire_hole = cq.Workplane("XY").workplane(offset=79.0).circle(7.0).extrude(20.0)
base_body = base_body.cut(wire_hole)

# Horizontal MG996R Servo Pocket (Centered at X=-12.5, Z=95.0)
servo_pocket = (
    cq.Workplane("XZ")
    .workplane(offset=-30.0) 
    .moveTo(SERVO_X, SERVO_Z)
    .rect(20.4, 41.4)
    .extrude(60.0) # Cut completely through Y
)
base_body = base_body.cut(servo_pocket)

# FSR wire bypass channel (Right of servo pocket)
fsr_bypass = (
    cq.Workplane("XZ")
    .workplane(offset=-30.0)
    .moveTo(0.0, SERVO_Z)
    .rect(4.0, 42.0)
    .extrude(60.0)
)
base_body = base_body.cut(fsr_bypass)

# 4x M3 Flange holes for the Servo
flange_pts = [
    (SERVO_X + 5.0, SERVO_Z + 24.0),
    (SERVO_X - 5.0, SERVO_Z + 24.0),
    (SERVO_X + 5.0, SERVO_Z - 24.0),
    (SERVO_X - 5.0, SERVO_Z - 24.0),
]
for pt in flange_pts:
    flange_hole = cq.Workplane("XZ").workplane(offset=21.7).moveTo(pt[0], pt[1]).circle(1.4).extrude(-15.0)
    base_body = base_body.cut(flange_hole)

# Right Pivot Hole (M4 Bolt clearance at X=+12.5, Z=105.5)
right_pivot_hole = (
    cq.Workplane("XZ")
    .workplane(offset=-30.0)
    .moveTo(12.5, SERVO_SPLINE_Z)
    .circle(4.2 / 2.0) # M4 clearance
    .extrude(60.0) 
)
base_body = base_body.cut(right_pivot_hole)

# Base corners left un-filleted to avoid OpenCascade topological collisions with flange holes

# ==============================================================================
# 2. GEAR GENERATOR UTILITY
# ==============================================================================
def create_gear_base(phase_offset_deg):
    gear = cq.Workplane("XY").circle(15.0).extrude(CLAW_THICKNESS)
    for i in range(10):
        angle = i * 36.0 + phase_offset_deg
        cutter = (
            cq.Workplane("XY")
            .transformed(rotate=cq.Vector(0, 0, angle))
            .polyline([(16.0, 2.5), (9.0, 1.2), (9.0, -1.2), (16.0, -2.5)])
            .close()
            .extrude(CLAW_THICKNESS)
        )
        gear = gear.cut(cutter)
    return gear

# ==============================================================================
# 3. LEFT FINGER (ACTIVE, ATTACHES TO SERVO)
# ==============================================================================
# Gear base with gap at 0 degrees
left_gear = create_gear_base(0)

# Arm extending to 90mm. Grasping face at X = +12.5
left_arm = (
    cq.Workplane("XY")
    .moveTo(12.5, 12.0)
    .lineTo(20.0, 12.0)
    .lineTo(15.0, CLAW_LENGTH)
    .lineTo(12.5, CLAW_LENGTH)
    .close()
    .extrude(CLAW_THICKNESS)
)
left_bridge = cq.Workplane("XY").moveTo(0, 0).lineTo(20.0, 12.0).lineTo(12.5, 12.0).close().extrude(CLAW_THICKNESS)
left_finger = left_gear.union(left_arm).union(left_bridge)

# Horn Recess cut from bottom
horn_recess = cq.Workplane("XY").circle(SERVO_HORN_DIA / 2.0).extrude(SERVO_HORN_DEPTH)
left_finger = left_finger.cut(horn_recess)

# Spline screw pilot hole
spline_hole = cq.Workplane("XY").circle(1.5).extrude(CLAW_THICKNESS)
left_finger = left_finger.cut(spline_hole)

# 4x M3 Horn mounting holes (14mm PCD)
for pt in [ (7.0*0.707, 7.0*0.707), (-7.0*0.707, 7.0*0.707), (7.0*0.707, -7.0*0.707), (-7.0*0.707, -7.0*0.707) ]:
    hole = cq.Workplane("XY").moveTo(pt[0], pt[1]).circle(3.2 / 2.0).extrude(CLAW_THICKNESS)
    left_finger = left_finger.cut(hole)

# FSR 402 Pocket on inner face (+12.5)
fsr_cut = cq.Workplane("YZ").workplane(offset=12.5).moveTo(CLAW_THICKNESS / 2.0, FSR_Z_CENTER).circle(FSR_POCKET_DIA / 2.0).extrude(FSR_POCKET_DEPTH)
left_finger = left_finger.cut(fsr_cut)

# Extend ribbon channel all the way to the base (Z=0)
ribbon = cq.Workplane("YZ").workplane(offset=12.5).moveTo(CLAW_THICKNESS / 2.0, FSR_Z_CENTER / 2.0).rect(4.0, FSR_Z_CENTER).extrude(FSR_POCKET_DEPTH)
left_finger = left_finger.cut(ribbon)

# Through-bore in gear base for FSR wire to drop into Gripper Base bypass channel
fsr_wire_hole = cq.Workplane("XY").moveTo(0, -4.5).circle(1.5).extrude(CLAW_THICKNESS)
left_finger = left_finger.cut(fsr_wire_hole)

# Edges left un-filleted to prevent OpenCascade topological collisions

# ==============================================================================
# 4. RIGHT FINGER (PASSIVE, GEARED)
# ==============================================================================
# Gear base shifted by 18 degrees to mesh perfectly
right_gear = create_gear_base(18)

# Arm extending to 90mm. Grasping face at X = -12.5
right_arm = (
    cq.Workplane("XY")
    .moveTo(-12.5, 12.0)
    .lineTo(-20.0, 12.0)
    .lineTo(-15.0, CLAW_LENGTH)
    .lineTo(-12.5, CLAW_LENGTH)
    .close()
    .extrude(CLAW_THICKNESS)
)
right_bridge = cq.Workplane("XY").moveTo(0, 0).lineTo(-20.0, 12.0).lineTo(-12.5, 12.0).close().extrude(CLAW_THICKNESS)
right_finger = right_gear.union(right_arm).union(right_bridge)

# Center pivot hole (M4 clearance)
pivot_hole = cq.Workplane("XY").circle(4.2 / 2.0).extrude(CLAW_THICKNESS)
right_finger = right_finger.cut(pivot_hole)

# Edges left un-filleted to prevent OpenCascade topological collisions


# ==============================================================================
# EXPORT OUTPUTS
# ==============================================================================
if __name__ == "__main__":
    export_dir = os.path.expanduser("~/ros2_ws/src/five_dof_arm_description/cad_export/gripper_assembly")
    os.makedirs(export_dir, exist_ok=True)

    base_step = os.path.join(export_dir, "gripper_base.step")
    base_stl = os.path.join(export_dir, "gripper_base.stl")
    cq.exporters.export(base_body, base_step)
    cq.exporters.export(base_body, base_stl)

    left_step = os.path.join(export_dir, "gripper_left_finger.step")
    left_stl = os.path.join(export_dir, "gripper_left_finger.stl")
    cq.exporters.export(left_finger, left_step)
    cq.exporters.export(left_finger, left_stl)

    right_step = os.path.join(export_dir, "gripper_right_finger.step")
    right_stl = os.path.join(export_dir, "gripper_right_finger.stl")
    cq.exporters.export(right_finger, right_step)
    cq.exporters.export(right_finger, right_stl)

    print(f"[CAD Export] Successfully generated Geared End-Effector:")
    print(f" - BASE:  {base_step}")
    print(f" - LEFT:  {left_step}")
    print(f" - RIGHT: {right_step}")