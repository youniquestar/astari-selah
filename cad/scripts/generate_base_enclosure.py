import cadquery as cq

# ==============================================================================
# PARAMETRIC SPECIFICATIONS & CLEARANCES (FROM .antigravity_rules)
# ==============================================================================

# 1. Base Housing Geometry
BASE_DIAMETER = 180.0
BASE_HEIGHT = 85.0
FLOOR_THICKNESS = 5.0
WALL_THICKNESS = 4.0
ROOF_THICKNESS = 12.0
D_PROFILE_FLAT_Y = -75.0  # Flat surface for D-profile at the rear

# 2. 6812ZZ Bearing Interface (Top Roof)
BEARING_OD = 78.2
BEARING_DEPTH = 10.2
BEARING_THROUGH_HOLE = 62.0 # Allows the turntable boss to drop through freely

# 3. Servo Floor Mounting 
# Note: Prompt mentions RDS3235, but .antigravity_rules strictly specifies 
# DSSERVO RDS5160 (60.4 x 30.4) for the Base Yaw. Using the rule dimensions.
SERVO_POCKET_L = 60.4
SERVO_POCKET_W = 30.4
SERVO_PEDESTAL_H = 30.0
# The servo spline must be concentric with the bearing (0,0). 
# A standard heavy-duty servo has its spline approx 15mm from the body center.
SERVO_OFFSET_Y = 15.0  

# 4. Electronics Standoffs (ESP32 & XL4016)
STANDOFF_HEIGHT = 8.0
STANDOFF_OD = 6.0
STANDOFF_ID = 2.5 # Pilot hole for M3 self-tapping screws

# ESP32 NodeMCU Hole Pattern (approx 43mm x 23mm)
# Placed on the left side of the enclosure
ESP32_HOLES = [(x - 45, y - 25) for x in [-21.5, 21.5] for y in [-11.5, 11.5]]

# XL4016 Buck Converter Hole Pattern (approx 55mm x 25mm)
# Placed on the right side of the enclosure
XL4016_HOLES = [(x + 45, y - 25) for x in [-27.5, 27.5] for y in [-12.5, 12.5]]

# ==============================================================================
# CADQUERY GEOMETRIC CONSTRUCTION
# ==============================================================================

# Step 1: Base Shell (Outer D-Profile)
body_outer = (
    cq.Workplane("XY")
    .circle(BASE_DIAMETER / 2.0)
    .extrude(BASE_HEIGHT)
)
# Cut the flat for the D-Profile
flat_cut_outer = (
    cq.Workplane("XY", origin=(0, D_PROFILE_FLAT_Y - 50, 0))
    .rect(BASE_DIAMETER, 100)
    .extrude(BASE_HEIGHT)
)
body_outer = body_outer.cut(flat_cut_outer)

# Step 2: Hollow Interior (Inner D-Profile)
body_inner = (
    cq.Workplane("XY", origin=(0, 0, FLOOR_THICKNESS))
    .circle((BASE_DIAMETER / 2.0) - WALL_THICKNESS)
    .extrude(BASE_HEIGHT - FLOOR_THICKNESS - ROOF_THICKNESS)
)
flat_cut_inner = (
    cq.Workplane("XY", origin=(0, D_PROFILE_FLAT_Y - 50 + WALL_THICKNESS, FLOOR_THICKNESS))
    .rect(BASE_DIAMETER - 2 * WALL_THICKNESS, 100)
    .extrude(BASE_HEIGHT - FLOOR_THICKNESS - ROOF_THICKNESS)
)
body_inner = body_inner.cut(flat_cut_inner)

# Apply hollowing to create the shell
base = body_outer.cut(body_inner)

# Step 3: Top Bearing Seat & Through Hole
base = (
    base.faces(">Z").workplane()
    .circle(BEARING_OD / 2.0)
    .cutBlind(-BEARING_DEPTH)
    .faces(">Z").workplane()
    .circle(BEARING_THROUGH_HOLE / 2.0)
    .cutBlind(-(ROOF_THICKNESS + 1.0))
)

# Create an absolute workplane for the inner floor
base = base.workplane(offset=FLOOR_THICKNESS).tag("floor")

# Step 4: Servo Mounting Pedestal 
base = (
    base.workplaneFromTagged("floor")
    .center(0, SERVO_OFFSET_Y)
    .rect(SERVO_POCKET_L + 12, SERVO_POCKET_W + 12)
    .extrude(SERVO_PEDESTAL_H)
    .workplaneFromTagged("floor")
    .workplane(offset=SERVO_PEDESTAL_H) # Workplane at top of pedestal
    .center(0, SERVO_OFFSET_Y)
    .rect(SERVO_POCKET_L, SERVO_POCKET_W)
    .cutBlind(-SERVO_PEDESTAL_H) # Pocket for the servo body
)

# Step 5: Electronics Standoffs
all_standoffs = ESP32_HOLES + XL4016_HOLES

# Extrude standoff posts
base = (
    base.workplaneFromTagged("floor")
    .pushPoints(all_standoffs)
    .circle(STANDOFF_OD / 2.0)
    .extrude(STANDOFF_HEIGHT)
)
# Cut pilot holes for self-tapping screws
base = (
    base.workplaneFromTagged("floor")
    .workplane(offset=STANDOFF_HEIGHT)
    .pushPoints(all_standoffs)
    .circle(STANDOFF_ID / 2.0)
    .cutBlind(-STANDOFF_HEIGHT)
)

# Step 6: Power & Data Wire Passthrough on the D-Profile Flat
wire_hole = (
    cq.Workplane("XZ", origin=(0, D_PROFILE_FLAT_Y - 5, FLOOR_THICKNESS + 15))
    .circle(8.0)
    .extrude(20) # Punches through the flat wall
)
base = base.cut(wire_hole)

# ==============================================================================
# EXPORT OUTPUTS
# ==============================================================================
if __name__ == "__main__":
    import os
    export_dir = os.path.expanduser("~/ros2_ws/src/five_dof_arm_description/cad_export")
    os.makedirs(export_dir, exist_ok=True)

    step_path = os.path.join(export_dir, "base_enclosure.step")
    stl_path = os.path.join(export_dir, "base_enclosure.stl")

    cq.exporters.export(base, step_path)
    cq.exporters.export(base, stl_path)
    print(f"[CAD Export] Successfully generated:")
    print(f" - STEP: {step_path}")
    print(f" - STL:  {stl_path}")
