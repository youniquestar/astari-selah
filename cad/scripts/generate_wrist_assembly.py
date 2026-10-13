import cadquery as cq
import os

# ==============================================================================
# PARAMETRIC SPECIFICATIONS & CLEARANCES (Units: mm)
# ==============================================================================

# 1. Structural Envelope (PETG, Solid Walls)
AXIS_TO_AXIS = 60.0           # Center of proximal pivot to center of distal spline
LINK_WIDTH = 40.0             # Outer X-axis dimension
LINK_HEIGHT = 35.0            # Outer Y-axis dimension
WALL_THICKNESS = 4.0          # Solid 4.0mm structural outer walls
TOTAL_LENGTH = 80.0           # Total physical bounding box length

# 2. Proximal Clevis (Z=0) - Mates with 42mm dia Forearm
CLEVIS_INNER_SPAN = 44.0      # 42mm Forearm + 1mm clearance per side
CLEVIS_WALL_THICK = 5.0
CLEVIS_OUTER_SPAN = CLEVIS_INNER_SPAN + (2 * CLEVIS_WALL_THICK)
SHOULDER_HORN_DIA = 25.4      # MG996R round horn recess
M8_CLEARANCE_DIA = 8.5        # Dummy bolt / counter pivot hole

# 3. Distal Joint (TowerPro MG996R Gripper Servo)
MG996R_POCKET_L = 41.0
MG996R_POCKET_W = 20.0
MG996R_FLANGE_PITCH_L = 48.0
MG996R_FLANGE_PITCH_W = 10.0
M3_PILOT_DIA = 2.8

# 4. Wire Routing
INTERNAL_CHANNEL_DIA = 14.0   # Main core routing diameter

# ==============================================================================
# 1. MAIN STRUCTURAL BRACKET
# ==============================================================================

# Main Body from Z=20 to Z=TOTAL_LENGTH
main_body = (
    cq.Workplane("XY")
    .workplane(offset=20.0)
    .rect(LINK_WIDTH, LINK_HEIGHT)
    .extrude(TOTAL_LENGTH - 20.0)
)

# Proximal Clevis Block
clevis_outer = (
    cq.Workplane("XY")
    .rect(CLEVIS_OUTER_SPAN, LINK_HEIGHT)
    .extrude(20.0)
)
# Rounded bottom for the clevis arms (at Z=0, rotating around X)
clevis_bottom = (
    cq.Workplane("YZ")
    .workplane(offset=-CLEVIS_OUTER_SPAN / 2.0)
    .circle(LINK_HEIGHT / 2.0)
    .extrude(CLEVIS_OUTER_SPAN)
)
clevis = clevis_outer.union(clevis_bottom)

# Cut the inner span to fit the 42mm Forearm
clevis_cut = (
    cq.Workplane("YZ")
    .workplane(offset=-CLEVIS_INNER_SPAN / 2.0)
    .moveTo(0, 0)
    .circle(44.0 / 2.0) # Radius 22.0
    .extrude(CLEVIS_INNER_SPAN)
).union(
    cq.Workplane("XY")
    .workplane(offset=0)
    .rect(CLEVIS_INNER_SPAN, LINK_HEIGHT + 10.0)
    .extrude(25.0)
)
clevis = clevis.cut(clevis_cut)

# Left Clevis Arm (-X): MG996R servo horn pocket
horn_pocket = (
    cq.Workplane("YZ")
    .workplane(offset=-CLEVIS_INNER_SPAN / 2.0)
    .circle(SHOULDER_HORN_DIA / 2.0)
    .extrude(-2.0) # Cut 2mm into the left arm
)
clevis = clevis.cut(horn_pocket)

# 4x M3 mounting holes for the servo horn (14mm pitch circle)
m3_pts = [
    ( 7.0 * 0.707,  7.0 * 0.707), 
    (-7.0 * 0.707,  7.0 * 0.707),
    ( 7.0 * 0.707, -7.0 * 0.707), 
    (-7.0 * 0.707, -7.0 * 0.707)
]
for pt in m3_pts:
    hole = (
        cq.Workplane("YZ")
        .workplane(offset=-CLEVIS_INNER_SPAN / 2.0)
        .moveTo(pt[0], pt[1])
        .circle(3.2 / 2.0)
        .extrude(-15.0)
    )
    clevis = clevis.cut(hole)

# Right Clevis Arm (+X): M8 counter-pivot dummy hole
m8_hole = (
    cq.Workplane("YZ")
    .workplane(offset=CLEVIS_INNER_SPAN / 2.0)
    .circle(M8_CLEARANCE_DIA / 2.0)
    .extrude(15.0)
)
clevis = clevis.cut(m8_hole)

# Fuse clevis and main body
wrist_body = main_body.union(clevis)

# ==============================================================================
# 2. INTERNAL CABLE ROUTING
# ==============================================================================

# Central wire routing channel (handles wiring up to the wrist servo)
wire_channel = (
    cq.Workplane("XY")
    .workplane(offset=-25.0)
    .circle(INTERNAL_CHANNEL_DIA / 2.0)
    .extrude(TOTAL_LENGTH)
)
wrist_body = wrist_body.cut(wire_channel)

# (Distal servo has been moved to the Gripper Base assembly, 
# so Link 3 remains a solid block from Z=60 to Z=80 for secure mounting)

# ==============================================================================
# 4. AESTHETIC / CLEARANCE FILLETS
# ==============================================================================

# Round the distal end corners for smooth profile around the gripper base
wrist_body = (
    wrist_body.faces(">Z").edges("|Y")
    .fillet(3.0) # Gentle 3mm fillet
)

# ==============================================================================
# EXPORT OUTPUTS
# ==============================================================================
if __name__ == "__main__":
    export_dir = os.path.expanduser("~/ros2_ws/src/five_dof_arm_description/cad_export")
    os.makedirs(export_dir, exist_ok=True)

    step_path = os.path.join(export_dir, "link_3_wrist_assembly.step")
    stl_path = os.path.join(export_dir, "link_3_wrist_assembly.stl")

    cq.exporters.export(wrist_body, step_path)
    cq.exporters.export(wrist_body, stl_path)

    print(f"[CAD Export] Successfully generated:")
    print(f" - STEP: {step_path}")
    print(f" - STL:  {stl_path}")