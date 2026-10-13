import cadquery as cq
import math

# ==============================================================================
# PARAMETRIC SPECIFICATIONS & CLEARANCES
# ==============================================================================

# 1. Main Turntable Disk Geometry
PLATE_DIAMETER = 140.0         # Outer diameter of the rotating platform (mm)
PLATE_THICKNESS = 8.0          # Main structural disk thickness (mm)

# 2. 6812ZZ Bearing Interface (Nominal: 60mm ID x 78mm OD x 10mm Width)
BEARING_ID_NOMINAL = 60.0
BEARING_WIDTH = 10.0
# Turntable inner centering boss drops into the 60mm ID bearing ring
# 0.2mm radial clearance for a smooth slip-fit into the bearing race
BOSS_DIAMETER = 59.6           
# Boss height is kept slightly shorter than bearing width to avoid floor scraping
BOSS_HEIGHT = 9.0              
BOSS_LEAD_IN_CHAMFER = 1.0     # 45-deg chamfer for easy drop-in assembly

# 3. RDS3235 Standard Round Metal Servo Horn Interface
# Metal horn pocket recessed into the underside of the boss
HORN_POCKET_DIAMETER = 25.4    # Diameter of standard 25T round aluminum horn pocket (mm)
HORN_POCKET_DEPTH = 2.0       # Recess depth ensuring 1.0mm vertical air gap to base roof
HORN_CENTER_HOLE_DIA = 6.0     # Center spline bolt access hole (mm)
HORN_BOLT_PCD = 14.0           # Pitch Circle Diameter for M3 horn attachment screws (mm)
HORN_BOLT_HOLE_DIA = 3.2       # Through-hole for M3 bolts into the horn (mm)

# 4. Wire Passthrough Slots (Kidney-Bean Profiles)
# Allows shoulder, elbow, wrist, and camera wiring to drop past the central motor
SLOT_INNER_RADIUS = 15.0       # Inner boundary radius (mm)
SLOT_OUTER_RADIUS = 25.0       # Outer boundary radius (mm)
SLOT_ANGLE_SPAN = 70.0         # Half-arc angular span from Y-axis (degrees)

# 5. Dual-Pivot Shoulder Yoke Mounting Flanges
# Symmetrical mounting pattern on top surface for M3 hardware / heat-set inserts
YOKE_MOUNT_X_OFFSET = 35.0     # Offset across the shoulder span (mm)
YOKE_MOUNT_Y_OFFSET = 25.0     # Offset front-to-back (mm)
YOKE_MOUNT_HOLE_DIA = 3.2      # M3 clearance hole (mm)
YOKE_COUNTERBORE_DIA = 6.2     # Socket head cap screw recess (mm)
YOKE_COUNTERBORE_DEPTH = 3.0   # Counterbore depth (mm)


# ==============================================================================
# CADQUERY GEOMETRIC CONSTRUCTION
# ==============================================================================

# Step 1: Base Platform Disk (Z = 0 to Z = +PLATE_THICKNESS)
turntable = (
    cq.Workplane("XY")
    .circle(PLATE_DIAMETER / 2.0)
    .extrude(PLATE_THICKNESS)
)

# Step 2: Underside Centering Boss (Drops into 6812ZZ Bearing Inner Race)
# Extruded downward from the bottom face (Z = 0 to Z = -BOSS_HEIGHT)
turntable = (
    turntable.faces("<Z")
    .workplane()
    .circle(BOSS_DIAMETER / 2.0)
    .extrude(BOSS_HEIGHT)  # Pushes outward normal to <Z, into negative Z
)

# Apply lead-in chamfer to bottom edge of boss for easy insertion
turntable = (
    turntable.edges("<Z")
    .chamfer(BOSS_LEAD_IN_CHAMFER)
)

# Step 3: Recessed Servo Horn Pocket & Spline Center Hole
# Cut into the bottom face of the centering boss
turntable = (
    turntable.faces("<Z")
    .workplane()
    .circle(HORN_POCKET_DIAMETER / 2.0)
    .cutBlind(-HORN_POCKET_DEPTH)
)

# Central M6 through-hole for spline retention screw access
turntable = (
    turntable.faces("<Z")
    .workplane()
    .circle(HORN_CENTER_HOLE_DIA / 2.0)
    .cutThruAll()
)

# Step 4: Servo Horn M3 Fastener Bolt Pattern (4x holes at 90 deg on 14mm PCD)
horn_bolt_points = [
    ( (HORN_BOLT_PCD / 2.0) * math.cos(math.radians(a)),
      (HORN_BOLT_PCD / 2.0) * math.sin(math.radians(a)) )
    for a in [0, 90, 180, 270]
]

turntable = (
    turntable.faces("<Z")
    .workplane()
    .pushPoints(horn_bolt_points)
    .hole(HORN_BOLT_HOLE_DIA, depth=PLATE_THICKNESS + BOSS_HEIGHT)
)

# Step 5: Symmetrical Kidney-Bean Wire Passthroughs
# Sweeps two circular wire slots that route down through the 60mm hollow bearing core
def create_kidney_wire_slot(workplane, angle_center_deg):
    r_in = SLOT_INNER_RADIUS
    r_out = SLOT_OUTER_RADIUS
    half_angle = SLOT_ANGLE_SPAN / 2.0
    a1 = math.radians(angle_center_deg - half_angle)
    a2 = math.radians(angle_center_deg + half_angle)

    # Calculate corner vertices for sector
    p1 = (r_in * math.cos(a1), r_in * math.sin(a1))
    p2 = (r_out * math.cos(a1), r_out * math.sin(a1))
    p3 = (r_out * math.cos(a2), r_out * math.sin(a2))
    p4 = (r_in * math.cos(a2), r_in * math.sin(a2))

    # Arc midpoints for 3-point arc sketching
    amid = math.radians(angle_center_deg)
    p_arc_out = (r_out * math.cos(amid), r_out * math.sin(amid))
    p_arc_in = (r_in * math.cos(amid), r_in * math.sin(amid))

    slot = (
        workplane
        .moveTo(p1[0], p1[1])
        .lineTo(p2[0], p2[1])
        .threePointArc(p_arc_out, p3)
        .lineTo(p4[0], p4[1])
        .threePointArc(p_arc_in, p1)
        .close()
    )
    return slot

# Cut Left and Right wire slots through the entire body
top_face = turntable.faces(">Z").workplane()
turntable = create_kidney_wire_slot(top_face, angle_center_deg=90).cutThruAll()

top_face = turntable.faces(">Z").workplane()
turntable = create_kidney_wire_slot(top_face, angle_center_deg=270).cutThruAll()

# Step 6: Dual-Pivot Shoulder Yoke Mounting Holes
# 4x M3 counterbored holes on the top platform
yoke_mount_points = [
    ( YOKE_MOUNT_X_OFFSET,  YOKE_MOUNT_Y_OFFSET),
    (-YOKE_MOUNT_X_OFFSET,  YOKE_MOUNT_Y_OFFSET),
    ( YOKE_MOUNT_X_OFFSET, -YOKE_MOUNT_Y_OFFSET),
    (-YOKE_MOUNT_X_OFFSET, -YOKE_MOUNT_Y_OFFSET),
]

turntable = (
    turntable.faces(">Z")
    .workplane()
    .pushPoints(yoke_mount_points)
    .cboreHole(
        diameter=YOKE_MOUNT_HOLE_DIA,
        cboreDiameter=YOKE_COUNTERBORE_DIA,
        cboreDepth=YOKE_COUNTERBORE_DEPTH,
        depth=PLATE_THICKNESS
    )
)


# Step 7: Top Perimeter Fillet (Only rounds the outer rim)
turntable = (
    turntable.edges(cq.selectors.RadiusNthSelector(0))  # Selects largest circular edge
    .fillet(0.5)
)

# ==============================================================================
# EXPORT OUTPUTS
# ==============================================================================
if __name__ == "__main__":
    import os
    export_dir = os.path.expanduser("~/ros2_ws/src/five_dof_arm_description/cad_export")
    os.makedirs(export_dir, exist_ok=True)

    step_path = os.path.join(export_dir, "turntable_hub_6812zz.step")
    stl_path = os.path.join(export_dir, "turntable_hub_6812zz.stl")

    cq.exporters.export(turntable, step_path)
    cq.exporters.export(turntable, stl_path)
    print(f"[CAD Export] Successfully generated:")
    print(f" - STEP: {step_path}")
    print(f" - STL:  {stl_path}")