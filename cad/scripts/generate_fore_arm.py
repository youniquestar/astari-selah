import cadquery as cq
import os

# ==============================================================================
# PARAMETRIC SPECIFICATIONS & CLEARANCES (Units: mm)
# ==============================================================================

# 1. Structural Envelope (PLA+, 35% Gyroid Infill)
LINK_LENGTH = 180.0           # Center-to-center joint distance (Elbow to Wrist)
OUTER_DIA = 42.0              # Cylindrical outer profile
INTERNAL_CHANNEL_DIA = 20.0   # Hollow core for cable routing
WALL_THICKNESS = 4.0          # Nominal structural wall thickness

# 2. Elbow Clevis (Z=0) - Mates with 55mm wide Upper Arm
CLEVIS_INNER_SPAN = 57.0      # 55mm Upper Arm + 1mm clearance per side
CLEVIS_WALL_THICK = 8.0
CLEVIS_OUTER_SPAN = CLEVIS_INNER_SPAN + (2 * CLEVIS_WALL_THICK)
SHOULDER_HORN_DIA = 25.4      # MG996R round horn recess
M8_CLEARANCE_DIA = 8.5        # Dummy bolt / counter pivot hole

# 3. Wrist Servo (Z=180) - Houses MG996R for Wrist Pitch
MG996R_L = 41.0
MG996R_W = 20.0
MG996R_FLANGE_L = 48.0
M3_PILOT_DIA = 2.8

# 4. ESP32-CAM Mounting Shelf
CAM_SHELF_Z = 130.0           # Relocated to avoid wrist servo
CAM_LIFT = 10.0               # Raised to clear the wrist joint from field of view
CAM_ANGLE = 15.0              # Adjusted depression angle
CAM_SHELF_WIDTH = 32.0        # Width of the ESP32-CAM PCB support
CAM_SHELF_LENGTH = 42.0       # Length of the ESP32-CAM PCB support
CAM_SHELF_THICK = 5.0         # Structural thickness of the shelf

# ==============================================================================
# 1. MAIN BODY & WRIST PIVOT
# ==============================================================================

# Cylinder from Z=20 to Z=180 (Leaves Z=0 for the clevis)
main_body = (
    cq.Workplane("XY")
    .workplane(offset=20.0)
    .circle(OUTER_DIA / 2.0)
    .extrude(LINK_LENGTH - 20.0)
)

# Add rounded pivot cap at the Wrist (Z=180)
wrist_pivot = (
    cq.Workplane("XZ")
    .workplane(offset=0)
    .center(0, LINK_LENGTH)
    .circle(OUTER_DIA / 2.0)
    .extrude(OUTER_DIA / 2.0, both=True)
)

forearm = main_body.union(wrist_pivot)

# ==============================================================================
# 2. ELBOW CLEVIS (Z=0)
# ==============================================================================

# Solid U-block that blends into the cylinder at Z=20
clevis_outer = (
    cq.Workplane("XY")
    .rect(CLEVIS_OUTER_SPAN, OUTER_DIA)
    .extrude(20.0)
)
clevis_bottom = (
    cq.Workplane("YZ")
    .workplane(offset=-CLEVIS_OUTER_SPAN / 2.0)
    .circle(OUTER_DIA / 2.0)
    .extrude(CLEVIS_OUTER_SPAN)
)
clevis = clevis_outer.union(clevis_bottom)

# Cut the inner span to fit the 55mm Upper Arm
clevis_cut = (
    cq.Workplane("YZ")
    .workplane(offset=-CLEVIS_INNER_SPAN / 2.0)
    .moveTo(0, 0)
    .circle(28.5) # Upper arm is 55mm top cap -> radius 27.5 + 1mm clearance
    .extrude(CLEVIS_INNER_SPAN)
).union(
    cq.Workplane("XY")
    .workplane(offset=0)
    .rect(CLEVIS_INNER_SPAN, OUTER_DIA + 20.0)
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
        .extrude(-10.0)
    )
    clevis = clevis.cut(hole)

# Right Clevis Arm (+X): M8 counter-pivot hole
m8_hole = (
    cq.Workplane("YZ")
    .workplane(offset=CLEVIS_INNER_SPAN / 2.0)
    .circle(M8_CLEARANCE_DIA / 2.0)
    .extrude(10.0)
)
clevis = clevis.cut(m8_hole)

forearm = forearm.union(clevis)

# ==============================================================================
# 3. INTERNAL CABLE ROUTING CHANNEL
# ==============================================================================

# Hollow out the 20mm central channel straight through the entire link
wire_channel = (
    cq.Workplane("XY")
    .workplane(offset=-25.0) # Start below the clevis
    .circle(INTERNAL_CHANNEL_DIA / 2.0)
    .extrude(LINK_LENGTH + 50.0)
)
forearm = forearm.cut(wire_channel)

# ==============================================================================
# 4. WRIST SERVO CUTOUT (Z=180)
# ==============================================================================

# MG996R placed lengthwise. The servo body is 40.7mm long, spline is ~10mm from top edge.
# To align the spline perfectly with Z=180, the pocket center is offset to Z=169.5.
servo_cutout = (
    cq.Workplane("YZ")
    .workplane(offset=-30.0) # Start completely outside the arm
    .moveTo(0, 169.5)
    .rect(MG996R_W, MG996R_L)
    .extrude(60.0) # Plunge entirely through the 42mm cylinder width
)
forearm = forearm.cut(servo_cutout)

# Add 4x M3 Pilot holes for the MG996R mounting flanges on the left wall (-X)
flange_pts = [
    ( 10.0 / 2.0, 169.5 + MG996R_FLANGE_L / 2.0),
    (-10.0 / 2.0, 169.5 + MG996R_FLANGE_L / 2.0),
    ( 10.0 / 2.0, 169.5 - MG996R_FLANGE_L / 2.0),
    (-10.0 / 2.0, 169.5 - MG996R_FLANGE_L / 2.0),
]

for pt in flange_pts:
    flange_hole = (
        cq.Workplane("YZ")
        .workplane(offset=-OUTER_DIA / 2.0) # Start on the left outer surface
        .moveTo(pt[0], pt[1])
        .circle(M3_PILOT_DIA / 2.0)
        .extrude(10.0) # Plunge 10mm into the cylinder wall
    )
    forearm = forearm.cut(flange_hole)

# ==============================================================================
# 5. ESP32-CAM ANGLED MOUNTING SHELF
# ==============================================================================

# Create the shelf base, lifted radially by 10mm to clear the wrist pivot
cam_shelf = (
    cq.Workplane("XY")
    .transformed(
        offset=cq.Vector(0, OUTER_DIA / 2.0 + CAM_LIFT, CAM_SHELF_Z), 
        rotate=cq.Vector(-CAM_ANGLE, 0, 0)
    )
    .box(CAM_SHELF_WIDTH, CAM_SHELF_LENGTH, CAM_SHELF_THICK, centered=(True, False, False))
)

# Create a structural stalk to connect the shelf to the cylindrical body
cam_stalk = (
    cq.Workplane("XY")
    .transformed(
        offset=cq.Vector(0, OUTER_DIA / 2.0 - 5.0, CAM_SHELF_Z), 
        rotate=cq.Vector(-CAM_ANGLE, 0, 0)
    )
    # The stalk bridges the 15mm gap (+5mm into the cylinder for solid union)
    .box(CAM_SHELF_WIDTH, CAM_SHELF_LENGTH, CAM_LIFT + 5.0, centered=(True, False, False))
)

forearm = forearm.union(cam_shelf).union(cam_stalk)

# Cut a wire passthrough hole directly behind the camera shelf into the main core
cam_wire_hole = (
    cq.Workplane("XY")
    .transformed(
        offset=cq.Vector(0, OUTER_DIA / 2.0 + CAM_LIFT - 5.0, CAM_SHELF_Z + 5.0), 
        rotate=cq.Vector(-CAM_ANGLE, 0, 0)
    )
    .circle(5.0)
    .extrude(-40.0) # Plunge downward into the central 20mm routing core
)

forearm = forearm.cut(cam_wire_hole)

# ==============================================================================
# EXPORT OUTPUTS
# ==============================================================================
if __name__ == "__main__":
    export_dir = os.path.expanduser("~/ros2_ws/src/five_dof_arm_description/cad_export")
    os.makedirs(export_dir, exist_ok=True)

    step_path = os.path.join(export_dir, "link_2_forearm.step")
    stl_path = os.path.join(export_dir, "link_2_forearm.stl")

    cq.exporters.export(forearm, step_path)
    cq.exporters.export(forearm, stl_path)

    print(f"[CAD Export] Successfully generated:")
    print(f" - STEP: {step_path}")
    print(f" - STL:  {stl_path}")