import cadquery as cq
import os

# ==============================================================================
# PARAMETRIC SPECIFICATIONS & CLEARANCES (Units: mm)
# ==============================================================================

# 1. Structural Envelope (PLA+, 35% Gyroid Infill)
LINK_LENGTH = 220.0           # Center-to-center joint distance
LINK_WIDTH = 55.0             # Outer X-axis dimension
LINK_DEPTH = 45.0             # Outer Y-axis dimension
WALL_THICKNESS = 4.0          # Rigid 4.0mm outer walls

# 2. Proximal Joint (Shoulder Axis at Z = 0)
# Mates with RDS5160 on the left, 608ZZ bearing pin on the right
SHOULDER_HORN_POCKET_DIA = 25.4 # Metal round servo horn recess diameter
SHOULDER_HORN_POCKET_DEPTH = 2.0
M8_CLEARANCE_DIA = 8.5        # Right-side passive pivot bolt hole
M3_CLEARANCE_DIA = 3.2        # Horn mounting bolts

# 3. Distal Joint (Elbow Axis at Z = 220)
# Houses the TowerPro MG996R (11 kg.cm)
MG996R_POCKET_L = 41.0        # 40.7mm body + 0.3mm tolerance
MG996R_POCKET_W = 20.0        # 19.7mm body + 0.3mm tolerance
MG996R_FLANGE_PITCH_L = 48.0  # Lengthwise mounting hole pitch
MG996R_FLANGE_PITCH_W = 10.0  # Widthwise mounting hole pitch
M3_PILOT_DIA = 2.8            # Tapping hole for mounting screws

# ==============================================================================
# 1. MAIN STRUCTURAL BODY (Hollow Rectangular Tube)
# ==============================================================================

# Create the main solid envelope with rounded ends around the pivot axes
def create_outer_profile():
    return (
        cq.Workplane("XY")
        .moveTo(-LINK_WIDTH/2.0, -LINK_DEPTH/2.0)
        .lineTo(LINK_WIDTH/2.0, -LINK_DEPTH/2.0)
        .lineTo(LINK_WIDTH/2.0, LINK_DEPTH/2.0)
        .lineTo(-LINK_WIDTH/2.0, LINK_DEPTH/2.0)
        .close()
        .extrude(LINK_LENGTH)
    )

# Base solid body
link_body = create_outer_profile()

# Add semi-circular rounded ends at Z=0 and Z=220 for pivot clearance
bottom_cap = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .circle(LINK_WIDTH / 2.0)
    .extrude(LINK_DEPTH / 2.0, both=True)
)

top_cap = (
    cq.Workplane("XZ")
    .workplane(offset=0)
    .center(0, LINK_LENGTH)
    .circle(LINK_WIDTH / 2.0)
    .extrude(LINK_DEPTH / 2.0, both=True)
)

link_body = link_body.union(bottom_cap).union(top_cap)

# Hollow out the interior to leave exactly 4.0mm structural walls
inner_cavity = (
    cq.Workplane("XY")
    .rect(LINK_WIDTH - (2 * WALL_THICKNESS), LINK_DEPTH - (2 * WALL_THICKNESS))
    .extrude(LINK_LENGTH)
)
link_body = link_body.cut(inner_cavity)

# ==============================================================================
# 2. PROXIMAL JOINT CUTOUTS (Shoulder Pitch Interface)
# ==============================================================================

# Left Side (-X): RDS5160 Metal Horn Recess and Mounting Holes
horn_pocket = (
    cq.Workplane("YZ")
    .workplane(offset=-(LINK_WIDTH / 2.0))
    .moveTo(0, 0)
    .circle(SHOULDER_HORN_POCKET_DIA / 2.0)
    .extrude(SHOULDER_HORN_POCKET_DEPTH)
)
link_body = link_body.cut(horn_pocket)

# 4x M3 through-holes for securing the horn to the link wall
horn_bolt_points = [
    (14.0/2 * 0.707, 14.0/2 * 0.707),
    (-14.0/2 * 0.707, 14.0/2 * 0.707),
    (14.0/2 * 0.707, -14.0/2 * 0.707),
    (-14.0/2 * 0.707, -14.0/2 * 0.707)
]
for pt in horn_bolt_points:
    hole_cut = (
        cq.Workplane("YZ")
        .workplane(offset=-(LINK_WIDTH / 2.0))
        .moveTo(pt[0], pt[1])
        .circle(M3_CLEARANCE_DIA / 2.0)
        .extrude(WALL_THICKNESS + 2.0)
    )
    link_body = link_body.cut(hole_cut)

# Right Side (+X): M8 Clearance Hole for 608ZZ Bearing Pivot Bolt
m8_pivot = (
    cq.Workplane("YZ")
    .workplane(offset=(LINK_WIDTH / 2.0) - WALL_THICKNESS - 2.0)
    .moveTo(0, 0)
    .circle(M8_CLEARANCE_DIA / 2.0)
    .extrude(WALL_THICKNESS + 4.0)
)
link_body = link_body.cut(m8_pivot)

# ==============================================================================
# 3. DISTAL JOINT CUTOUTS (Elbow Pitch MG996R Servo)
# ==============================================================================

# Cut rectangular drop-in pocket for the MG996R at Z=220
mg996r_cutout = (
    cq.Workplane("YZ")
    .workplane(offset=-(LINK_WIDTH / 2.0 + 2.0))
    .moveTo(0, LINK_LENGTH)
    .rect(MG996R_POCKET_W, MG996R_POCKET_L)
    .extrude(LINK_WIDTH + 4.0)
)
link_body = link_body.cut(mg996r_cutout)

# Add 4x M3 Pilot holes for the MG996R mounting flanges
flange_pts = [
    ( MG996R_FLANGE_PITCH_W / 2.0, LINK_LENGTH + MG996R_FLANGE_PITCH_L / 2.0),
    (-MG996R_FLANGE_PITCH_W / 2.0, LINK_LENGTH + MG996R_FLANGE_PITCH_L / 2.0),
    ( MG996R_FLANGE_PITCH_W / 2.0, LINK_LENGTH - MG996R_FLANGE_PITCH_L / 2.0),
    (-MG996R_FLANGE_PITCH_W / 2.0, LINK_LENGTH - MG996R_FLANGE_PITCH_L / 2.0),
]

for pt in flange_pts:
    flange_hole = (
        cq.Workplane("YZ")
        .workplane(offset=-(LINK_WIDTH / 2.0))
        .moveTo(pt[0], pt[1])
        .circle(M3_PILOT_DIA / 2.0)
        .extrude(WALL_THICKNESS + 2.0)
    )
    link_body = link_body.cut(flange_hole)

# ==============================================================================
# 4. WIRE ROUTING PASSTHROUGH
# ==============================================================================

# Add a 20mm circular wire passthrough hole directly down the central spine
wire_bore = (
    cq.Workplane("XY")
    .workplane(offset=-20.0)
    .circle(10.0)
    .extrude(LINK_LENGTH + 40.0)
)
link_body = link_body.cut(wire_bore)

# ==============================================================================
# EXPORT OUTPUTS
# ==============================================================================
if __name__ == "__main__":
    export_dir = os.path.expanduser("~/ros2_ws/src/five_dof_arm_description/cad_export")
    os.makedirs(export_dir, exist_ok=True)

    step_path = os.path.join(export_dir, "link_1_upper_arm.step")
    stl_path = os.path.join(export_dir, "link_1_upper_arm.stl")

    cq.exporters.export(link_body, step_path)
    cq.exporters.export(link_body, stl_path)

    print(f"[CAD Export] Successfully generated:")
    print(f" - STEP: {step_path}")
    print(f" - STL:  {stl_path}")