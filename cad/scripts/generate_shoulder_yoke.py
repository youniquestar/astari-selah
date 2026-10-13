import cadquery as cq
import os

# ==============================================================================
# PARAMETRIC SPECIFICATIONS & CLEARANCES (Units: mm)
# ==============================================================================

# 1. Base Plate Interface (Mates to Turntable Hub)
BASE_WIDTH_X = 90.0           # Footprint across width
BASE_DEPTH_Y = 70.0           # Footprint along depth
BASE_THICKNESS = 8.0          # Structural mounting base thickness
TURNTABLE_HOLE_X = 35.0       # Pitch matching turntable hub (X = +/- 35mm)
TURNTABLE_HOLE_Y = 25.0       # Pitch matching turntable hub (Y = +/- 25mm)
M3_CLEARANCE_DIA = 3.2        # For M3 bolts through to turntable
M3_HEX_NUT_WIDTH = 6.1        # M3 locknut flat-to-flat recess
M3_HEX_NUT_DEPTH = 3.0        # Recess depth on top face of base plate
WIRE_PASSTHROUGH_DIA = 40.0   # Hollow center for wiring down to 6812ZZ core

# 2. U-Frame Geometry & Upright Arms
INSIDE_SPAN = 65.0            # Internal clearance (houses 55mm wide Link 1 + 5mm gap/side)
WALL_THICKNESS = 10.0         # Rigid upright wall thickness (PETG)
TOTAL_YOKE_WIDTH = INSIDE_SPAN + (2 * WALL_THICKNESS) # 85.0 mm
UPRIGHT_HEIGHT = 80.0         # Height from bottom of base plate to top of arms
PIVOT_AXIS_Z = 55.0           # Joint rotational axis height from bottom plane
UPRIGHT_TOP_RADIUS = 25.0     # Radius for rounded top of uprights

# 3. Active Pivot (Left Wall, -X): DSSERVO RDS5160 Actuator
SERVO_CUTOUT_Y = 60.4         # 60.0mm body + 0.4mm tolerance
SERVO_CUTOUT_Z = 30.4         # 30.0mm body + 0.4mm tolerance
SERVO_FLANGE_HOLE_PITCH_Y = 74.0  # Flange bolt spacing along motor length
SERVO_FLANGE_HOLE_PITCH_Z = 10.0  # Flange bolt spacing across motor width
SERVO_PILOT_DIA = 2.8         # M3 self-tapping/threaded pilot hole

# 4. Passive Pivot (Right Wall, +X): 608ZZ Miniature Ball Bearing
BEARING_POCKET_DIA = 22.4     # 22.0mm OD + 0.4mm press-fit tolerance
BEARING_POCKET_DEPTH = 7.5    # Bearing thickness 7.0mm + 0.5mm depth margin
M8_BOLT_HOLE_DIA = 8.5        # Clearance through-hole for M8 counter-pivot pin

# ==============================================================================
# 1. BASE MOUNTING PLATE
# ==============================================================================
# Rectangular base centered at origin (Z: 0 to BASE_THICKNESS)
base_plate = (
    cq.Workplane("XY")
    .box(TOTAL_YOKE_WIDTH, BASE_DEPTH_Y, BASE_THICKNESS)
    .translate((0, 0, BASE_THICKNESS / 2.0))
)

# Central wire passthrough bore
base_plate = (
    base_plate.faces(">Z")
    .workplane()
    .circle(WIRE_PASSTHROUGH_DIA / 2.0)
    .cutThruAll()
)

# 4x M3 turntable mounting holes with counterbores for flush socket head screws
turntable_mount_pts = [
    ( TURNTABLE_HOLE_X,  TURNTABLE_HOLE_Y),
    (-TURNTABLE_HOLE_X,  TURNTABLE_HOLE_Y),
    ( TURNTABLE_HOLE_X, -TURNTABLE_HOLE_Y),
    (-TURNTABLE_HOLE_X, -TURNTABLE_HOLE_Y),
]

base_plate = (
    base_plate.faces(">Z")
    .workplane()
    .pushPoints(turntable_mount_pts)
    .cboreHole(
        diameter=M3_CLEARANCE_DIA,
        cboreDiameter=M3_HEX_NUT_WIDTH,
        cboreDepth=M3_HEX_NUT_DEPTH,
        depth=BASE_THICKNESS
    )
)

# ==============================================================================
# 2. UPRIGHT ARMS (LEFT AND RIGHT BRACKETS)
# ==============================================================================
# Profile sketch on YZ plane extruded across X
upright_x_center_left = -(INSIDE_SPAN / 2.0 + WALL_THICKNESS / 2.0)
upright_x_center_right = (INSIDE_SPAN / 2.0 + WALL_THICKNESS / 2.0)

def build_upright_solid():
    # Sketch tombstone profile (base to rounded top)
    arm = (
        cq.Workplane("YZ")
        .moveTo(-BASE_DEPTH_Y / 2.0, BASE_THICKNESS)
        .lineTo(BASE_DEPTH_Y / 2.0, BASE_THICKNESS)
        .lineTo(BASE_DEPTH_Y / 2.0, PIVOT_AXIS_Z)
        .threePointArc((0, PIVOT_AXIS_Z + UPRIGHT_TOP_RADIUS), (-BASE_DEPTH_Y / 2.0, PIVOT_AXIS_Z))
        .close()
        .extrude(WALL_THICKNESS)
    )
    # Center extrusion along X locally
    arm = arm.translate((-WALL_THICKNESS / 2.0, 0, 0))
    return arm

# Left upright (-X)
left_arm = build_upright_solid().translate((upright_x_center_left, 0, 0))

# Right upright (+X)
right_arm = build_upright_solid().translate((upright_x_center_right, 0, 0))

# Fuse arms to base plate
yoke = base_plate.union(left_arm).union(right_arm)

# ==============================================================================
# 3. ACTIVE PIVOT: LEFT UPRIGHT CUTOUTS (DSSERVO RDS5160)
# ==============================================================================
# Cut rectangular motor window centered at joint axis (Z = PIVOT_AXIS_Z)
left_outer_face_x = -(TOTAL_YOKE_WIDTH / 2.0)

servo_cutout = (
    cq.Workplane("YZ")
    .workplane(offset=-left_outer_face_x) # Start slightly outside
    .moveTo(0, PIVOT_AXIS_Z)
    .rect(SERVO_CUTOUT_Y, SERVO_CUTOUT_Z)
    .extrude(WALL_THICKNESS + 4.0) # Cut entirely through left upright wall
)
yoke = yoke.cut(servo_cutout)

# 4x Flange mounting holes for RDS5160 tabs
flange_pts_yz = [
    ( SERVO_FLANGE_HOLE_PITCH_Y / 2.0, PIVOT_AXIS_Z + SERVO_FLANGE_HOLE_PITCH_Z / 2.0),
    (-SERVO_FLANGE_HOLE_PITCH_Y / 2.0, PIVOT_AXIS_Z + SERVO_FLANGE_HOLE_PITCH_Z / 2.0),
    ( SERVO_FLANGE_HOLE_PITCH_Y / 2.0, PIVOT_AXIS_Z - SERVO_FLANGE_HOLE_PITCH_Z / 2.0),
    (-SERVO_FLANGE_HOLE_PITCH_Y / 2.0, PIVOT_AXIS_Z - SERVO_FLANGE_HOLE_PITCH_Z / 2.0),
]

for pt in flange_pts_yz:
    hole_tool = (
        cq.Workplane("YZ")
        .workplane(offset=-left_outer_face_x)
        .moveTo(pt[0], pt[1])
        .circle(SERVO_PILOT_DIA / 2.0)
        .extrude(WALL_THICKNESS + 4.0)
    )
    yoke = yoke.cut(hole_tool)

# ==============================================================================
# 4. PASSIVE PIVOT: RIGHT UPRIGHT CUTOUTS (608ZZ BEARING & M8 BOLT)
# ==============================================================================
# Bearing pocket sits on the INSIDE face of the right upright (facing Link 1)
right_inner_face_x = INSIDE_SPAN / 2.0

# 1. 608ZZ Pocket: Ø22.4mm x 7.5mm deep cut into the inside face towards +X
bearing_pocket = (
    cq.Workplane("YZ")
    .workplane(offset=-right_inner_face_x)
    .moveTo(0, PIVOT_AXIS_Z)
    .circle(BEARING_POCKET_DIA / 2.0)
    .extrude(-BEARING_POCKET_DEPTH) # Cuts into right upright
)
yoke = yoke.cut(bearing_pocket)

# 2. M8 Center Bolt Hole: Ø8.5mm through-hole cut completely through the upright
m8_through_hole = (
    cq.Workplane("YZ")
    .workplane(offset=-right_inner_face_x + 1.0)
    .moveTo(0, PIVOT_AXIS_Z)
    .circle(M8_BOLT_HOLE_DIA / 2.0)
    .extrude(WALL_THICKNESS + 4.0)
)
yoke = yoke.cut(m8_through_hole)

# ==============================================================================
# 5. REINFORCING FILLET (Safe selection of base gusset edges)
# ==============================================================================
# Add structural 45-degree chamfers where uprights meet the base plate
# using explicit prismatic box cutters to avoid OCCT BRep fillet errors
def create_base_gusset(x_pos, is_left=True):
    sign = 1.0 if is_left else -1.0
    gusset = (
        cq.Workplane("YZ")
        .moveTo(-BASE_DEPTH_Y / 2.0, BASE_THICKNESS)
        .lineTo(BASE_DEPTH_Y / 2.0, BASE_THICKNESS)
        .lineTo(BASE_DEPTH_Y / 2.0, BASE_THICKNESS + 12.0)
        .lineTo(-BASE_DEPTH_Y / 2.0, BASE_THICKNESS + 12.0)
        .close()
        .extrude(4.0)
        .translate((x_pos - (2.0 if is_left else -2.0), 0, 0))
    )
    return gusset

# ==============================================================================
# 6. COMBINE WITH TURNTABLE HUB
# ==============================================================================
import sys
sys.path.append(os.path.dirname(__file__))
from generate_turntable import turntable, PLATE_THICKNESS

# Translate the yoke to sit perfectly on top of the turntable (Z = PLATE_THICKNESS)
complete_shoulder_yoke = turntable.union(yoke.translate((0, 0, PLATE_THICKNESS)))

# ==============================================================================
# EXPORT OUTPUTS
# ==============================================================================
if __name__ == "__main__":
    export_dir = os.path.expanduser("~/ros2_ws/src/five_dof_arm_description/cad_export")
    os.makedirs(export_dir, exist_ok=True)

    step_path = os.path.join(export_dir, "complete_shoulder_yoke_axis.step")
    stl_path = os.path.join(export_dir, "complete_shoulder_yoke_axis.stl")

    cq.exporters.export(complete_shoulder_yoke, step_path)
    cq.exporters.export(complete_shoulder_yoke, stl_path)

    print(f"[CAD Export] Successfully generated combined shoulder yoke:")
    print(f" - STEP: {step_path}")
    print(f" - STL:  {stl_path}")