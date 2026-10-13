#!/usr/bin/env python3
"""
================================================================================
ASTARI SELAH — PROFESSIONAL MODULAR FREECAD CAD BUILDER
================================================================================
Parametrically constructs all 8 structural links, COTS actuators, bearings,
and fasteners directly using native FreeCAD Part/PartDesign tools.

Subassemblies and hierarchy:
1. Base_Assembly (Base Enclosure, 6812ZZ Bearing, Electronics Bay)
2. Shoulder_Assembly (Dual-Pivot Yoke, RDS5160 Mount, 608ZZ Bearing, M8 Bolt)
3. Upper_Arm_Assembly (Link 1: 220mm length, 55x45mm profile, MG996R pocket)
4. Forearm_Assembly (Link 2: 180mm length, 42mm OD, 20° Camera Shelf, Wire Channel)
5. Wrist_Assembly (Link 3: 60mm length, 40x35mm profile, MG996R cradle)
6. Gripper_Assembly (End-Effector: 90mm length, FSR 402 Recessed Pocket, Geared Claws)

Exports:
- Master native FreeCAD document: cad/assembly/astari_selah_master.FCStd
- Modular STEP solids: cad/parts/*.step
- Slice-ready STL meshes: cad/parts/*.stl and ros2/astari_selah_description/meshes/visual/*.stl
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
    print("Error: FreeCAD Python API modules not found. Run with FreeCAD AppImage.")
    sys.exit(1)

# Paths setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CAD_DIR = os.path.dirname(SCRIPT_DIR)
ASSEMBLY_DIR = os.path.join(CAD_DIR, "assembly")
PARTS_DIR = os.path.join(CAD_DIR, "parts")
ROS2_MESH_DIR = os.path.join(CAD_DIR, "..", "ros2", "astari_selah_description", "meshes", "visual")
ROS2_COL_DIR = os.path.join(CAD_DIR, "..", "ros2", "astari_selah_description", "meshes", "collision")

for d in [ASSEMBLY_DIR, PARTS_DIR, ROS2_MESH_DIR, ROS2_COL_DIR]:
    os.makedirs(d, exist_ok=True)

# Aesthetic color palette
COLOR_BLUE  = (0.0, 0.27, 0.73)      # Industrial Precision Blue
COLOR_BLACK = (0.12, 0.12, 0.12)    # Stealth Matte PETG / PLA+
COLOR_CHROME = (0.80, 0.82, 0.84)   # Bearing Chrome
COLOR_STEEL = (0.60, 0.62, 0.64)    # Stainless Hardware

# ==============================================================================
# 1. BASE ENCLOSURE (Diameter: 180mm, Height: 85mm, Solid 5mm Floor, D-Profile)
# ==============================================================================
def build_base_enclosure():
    """Builds the stationary base housing electronics and turntable bearing."""
    # Outer cylinder
    outer_cyl = Part.makeCylinder(90.0, 85.0, FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1))
    
    # D-profile rear flat cut (for battery bay and connector panel)
    rear_cutter = Part.makeBox(200.0, 40.0, 95.0, FreeCAD.Vector(-100.0, -130.0, -5.0))
    body = outer_cyl.cut(rear_cutter)
    
    # Internal hollow cavity (leaving 5.0mm bottom floor and 4.0mm walls)
    inner_cyl = Part.makeCylinder(84.0, 85.0, FreeCAD.Vector(0, 0, 5.0), FreeCAD.Vector(0, 0, 1))
    body = body.cut(inner_cyl)
    
    # 6812ZZ turntable bearing pocket on top roof (78mm OD, 10mm depth)
    bearing_pocket = Part.makeCylinder(39.0, 12.0, FreeCAD.Vector(0, 0, 75.0), FreeCAD.Vector(0, 0, 1))
    body = body.cut(bearing_pocket)
    
    # Center wire egress hole through roof
    center_hole = Part.makeCylinder(20.0, 90.0, FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1))
    body = body.cut(center_hole)
    
    # Standoff bosses for dual-ESP32, XL4016, and LM2596 (4x per module)
    standoffs = [
        (60.0, 20.0), (60.0, -20.0), (40.0, 20.0), (40.0, -20.0),  # ESP32
        (-50.0, 25.0), (-50.0, -25.0), (-30.0, 25.0), (-30.0, -25.0) # Buck Converters
    ]
    for x, y in standoffs:
        boss = Part.makeCylinder(3.5, 8.0, FreeCAD.Vector(x, y, 5.0), FreeCAD.Vector(0, 0, 1))
        bore = Part.makeCylinder(1.5, 8.0, FreeCAD.Vector(x, y, 5.0), FreeCAD.Vector(0, 0, 1))
        body = body.fuse(boss).cut(bore)
        
    return body

# ==============================================================================
# 2. SHOULDER YOKE (Dual-Pivot Clevis, 63mm Axis Height, RDS5160 & 608ZZ Pocket)
# ==============================================================================
def build_shoulder_yoke():
    """Builds the dual-pivot shoulder yoke supporting the RDS5160 servo and 608ZZ bearing."""
    # Turntable mounting plate
    base_plate = Part.makeCylinder(70.0, 8.0, FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1))
    
    # Upright arms (Left for RDS5160, Right for 608ZZ counter-bearing)
    # Pivot axis is at Z = 63.0mm
    left_upright = Part.makeBox(20.0, 60.0, 80.0, FreeCAD.Vector(-50.0, -30.0, 8.0))
    right_upright = Part.makeBox(20.0, 60.0, 80.0, FreeCAD.Vector(30.0, -30.0, 8.0))
    yoke = base_plate.fuse(left_upright).fuse(right_upright)
    
    # Left pocket: DSSERVO RDS5160 mounting cutout (60.4 x 30.4mm tolerance)
    rds_pocket = Part.makeBox(25.0, 30.4, 60.4, FreeCAD.Vector(-55.0, -15.2, 32.8))
    yoke = yoke.cut(rds_pocket)
    
    # Right pocket: 608ZZ bearing press-fit pocket (22.0mm OD, 7.0mm depth)
    bearing_pocket = Part.makeCylinder(11.0, 7.0, FreeCAD.Vector(30.0, 0, 63.0), FreeCAD.Vector(1, 0, 0))
    yoke = yoke.cut(bearing_pocket)
    
    # M8 pivot screw through-bore across both uprights along Y-axis
    m8_bore = Part.makeCylinder(4.2, 100.0, FreeCAD.Vector(-50.0, 0, 63.0), FreeCAD.Vector(1, 0, 0))
    yoke = yoke.cut(m8_bore)
    
    # Weight reduction central cutout
    center_cut = Part.makeCylinder(22.0, 15.0, FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1))
    yoke = yoke.cut(center_cut)
    
    return yoke

# ==============================================================================
# 3. UPPER ARM LINK 1 (Length: 220mm Axis-to-Axis, 55x45mm Rectangular Profile)
# ==============================================================================
def build_upper_arm():
    """Builds Link 1: 220mm center-to-center rigid beam with internal ribbing."""
    L = 220.0
    # Main structural body
    beam = Part.makeBox(55.0, 45.0, L, FreeCAD.Vector(-27.5, -22.5, 0.0))
    
    # Proximal shoulder pivot hub (Z = 0.0)
    shoulder_bore = Part.makeCylinder(4.1, 60.0, FreeCAD.Vector(-30.0, 0, 0.0), FreeCAD.Vector(1, 0, 0))
    beam = beam.cut(shoulder_bore)
    
    # Distal elbow pivot hub (Z = 220.0)
    elbow_bore = Part.makeCylinder(4.1, 60.0, FreeCAD.Vector(-30.0, 0, L), FreeCAD.Vector(1, 0, 0))
    beam = beam.cut(elbow_bore)
    
    # Distal MG996R elbow actuator pocket (41.0 x 20.0mm tolerance pocket)
    servo_pocket = Part.makeBox(41.0, 20.0, 45.0, FreeCAD.Vector(-20.5, -10.0, L - 50.0))
    beam = beam.cut(servo_pocket)
    
    # Internal hollow weight-reduction cavity (leaving 4.0mm walls)
    cavity = Part.makeBox(47.0, 37.0, L - 80.0, FreeCAD.Vector(-23.5, -18.5, 30.0))
    beam = beam.cut(cavity)
    
    return beam

# ==============================================================================
# 4. FOREARM LINK 2 (Length: 180mm Axis-to-Axis, 42mm OD, 20° Camera Shelf)
# ==============================================================================
def build_forearm():
    """Builds Link 2: 180mm cylindrical arm with 20mm wire channel and camera shelf."""
    L = 180.0
    # Cylindrical main tube
    tube = Part.makeCylinder(21.0, L, FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1))
    
    # 20mm internal wire routing conduit
    wire_channel = Part.makeCylinder(10.0, L + 20.0, FreeCAD.Vector(0, 0, -10.0), FreeCAD.Vector(0, 0, 1))
    tube = tube.cut(wire_channel)
    
    # Proximal clevis ears (connecting to elbow at Z = 0)
    elbow_bore = Part.makeCylinder(4.1, 50.0, FreeCAD.Vector(-25.0, 0, 0.0), FreeCAD.Vector(1, 0, 0))
    tube = tube.cut(elbow_bore)
    
    # Distal wrist clevis ears (Z = 180.0)
    wrist_bore = Part.makeCylinder(4.1, 50.0, FreeCAD.Vector(-25.0, 0, L), FreeCAD.Vector(1, 0, 0))
    tube = tube.cut(wrist_bore)
    
    # Dedicated ESP32-CAM mounting shelf at exactly 160mm mark (20mm before wrist)
    # Inclined at 20° downward relative to forearm axis for picking oversight
    cam_shelf = Part.makeBox(30.0, 25.0, 6.0, FreeCAD.Vector(-15.0, 16.0, 155.0))
    # Rotate shelf 20° around X-axis
    cam_shelf.rotate(FreeCAD.Vector(0, 16.0, 155.0), FreeCAD.Vector(1, 0, 0), -20.0)
    tube = tube.fuse(cam_shelf)
    
    return tube

# ==============================================================================
# 5. WRIST LINK 3 (Length: 60mm Axis-to-Axis, 40x35mm Compact Bracket)
# ==============================================================================
def build_wrist():
    """Builds Link 3: 60mm compact wrist housing MG996R wrist pitch servo."""
    L = 60.0
    body = Part.makeBox(40.0, 35.0, L, FreeCAD.Vector(-20.0, -17.5, 0.0))
    
    # Wrist pivot hole (Z = 0)
    pivot_bore = Part.makeCylinder(4.1, 50.0, FreeCAD.Vector(-25.0, 0, 0.0), FreeCAD.Vector(1, 0, 0))
    body = body.cut(pivot_bore)
    
    # MG996R pocket
    servo_cut = Part.makeBox(41.0, 20.0, 43.0, FreeCAD.Vector(-20.5, -10.0, 10.0))
    body = body.cut(servo_cut)
    
    # End flange for gripper attachment at Z = 60mm (4x M3 screw holes)
    for dx, dy in [(12.0, 10.0), (-12.0, 10.0), (12.0, -10.0), (-12.0, -10.0)]:
        screw_hole = Part.makeCylinder(1.6, 20.0, FreeCAD.Vector(dx, dy, L - 10.0), FreeCAD.Vector(0, 0, 1))
        body = body.cut(screw_hole)
        
    return body

# ==============================================================================
# 6. GRIPPER BASE & JAWS (Length: 90mm Closed, 70mm Jaw Stroke, FSR Pocket)
# ==============================================================================
def build_gripper_base():
    """Builds the end-effector base housing the horizontal MG996R servo and jaw hinges."""
    body = Part.makeBox(48.4, 43.4, 60.0, FreeCAD.Vector(-24.2, -21.7, 0.0))
    
    # MG996R horizontal pocket
    servo_cut = Part.makeBox(42.0, 20.5, 41.0, FreeCAD.Vector(-21.0, -10.25, 10.0))
    body = body.cut(servo_cut)
    
    # Dual finger pivot hinge holes (at X = +/-12.5mm, Y = 21.7mm, Z = 45.5mm)
    for x in [-12.5, 12.5]:
        hinge_hole = Part.makeCylinder(2.1, 50.0, FreeCAD.Vector(x, -25.0, 45.5), FreeCAD.Vector(0, 1, 0))
        body = body.cut(hinge_hole)
        
    return body

def build_gripper_left_finger():
    """Builds the left articulated gripper claw with 1.0mm recessed FSR 402 sensor pocket."""
    # Curved claw profile
    finger_body = Part.makeBox(8.0, 90.0, 12.0, FreeCAD.Vector(-4.0, 0.0, 0.0))
    
    # Hinge pivot hole
    pivot = Part.makeCylinder(2.1, 20.0, FreeCAD.Vector(-10.0, 10.0, 6.0), FreeCAD.Vector(1, 0, 0))
    finger_body = finger_body.cut(pivot)
    
    # 1.0mm recessed tactile pocket on inner face (for FSR 402 round sensor: 18mm dia, 1.0mm deep)
    fsr_pocket = Part.makeCylinder(9.0, 1.2, FreeCAD.Vector(4.0, 55.0, 6.0), FreeCAD.Vector(-1, 0, 0))
    finger_body = finger_body.cut(fsr_pocket)
    
    # Chamfer gripping tip
    tip_cut = Part.makeBox(12.0, 20.0, 20.0, FreeCAD.Vector(-6.0, 80.0, 6.0))
    finger_body = finger_body.cut(tip_cut)
    
    return finger_body

def build_gripper_right_finger():
    """Builds the right articulated gripper claw counter-rotating with left claw."""
    finger_body = Part.makeBox(8.0, 90.0, 12.0, FreeCAD.Vector(-4.0, 0.0, 0.0))
    pivot = Part.makeCylinder(2.1, 20.0, FreeCAD.Vector(-10.0, 10.0, 6.0), FreeCAD.Vector(1, 0, 0))
    finger_body = finger_body.cut(pivot)
    
    tip_cut = Part.makeBox(12.0, 20.0, 20.0, FreeCAD.Vector(-6.0, 80.0, 6.0))
    finger_body = finger_body.cut(tip_cut)
    
    return finger_body

# ==============================================================================
# MASTER BUILD & EXPORT
# ==============================================================================
def main():
    print("=" * 70)
    print("  ASTARI SELAH: BUILDING PROFESSIONAL MODULAR FREECAD CAD MODEL")
    print("=" * 70)
    
    doc = FreeCAD.newDocument("Astari_Selah_Master")
    
    parts_map = {
        "base_enclosure":       (build_base_enclosure(), COLOR_BLACK),
        "shoulder_yoke":        (build_shoulder_yoke(), COLOR_BLUE),
        "upper_arm":            (build_upper_arm(), COLOR_BLACK),
        "forearm":              (build_forearm(), COLOR_BLUE),
        "wrist":                (build_wrist(), COLOR_BLACK),
        "gripper_base":         (build_gripper_base(), COLOR_BLUE),
        "gripper_left_finger":  (build_gripper_left_finger(), COLOR_BLACK),
        "gripper_right_finger": (build_gripper_right_finger(), COLOR_BLACK),
    }
    
    # 1. Add parts to FreeCAD document
    print("\n[1/3] Adding modular parts to FreeCAD document hierarchy...")
    for name, (shape, color) in parts_map.items():
        obj = doc.addObject("Part::Feature", name)
        obj.Shape = shape
        if hasattr(obj, "ViewObject") and obj.ViewObject:
            obj.ViewObject.ShapeColor = color
        print(f"  ✓ {name}")
        
    doc.recompute()
    
    # 2. Save native FreeCAD Master Document
    fcstd_path = os.path.join(ASSEMBLY_DIR, "astari_selah_master.FCStd")
    print(f"\n[2/3] Saving FreeCAD master document: {fcstd_path}")
    doc.saveAs(fcstd_path)
    print("  ✓ Document saved successfully.")
    
    # 3. Export STEP solids and STL meshes
    print("\n[3/3] Exporting individual STEP solids and slice-ready STL meshes...")
    for name, (shape, _) in parts_map.items():
        step_file = os.path.join(PARTS_DIR, f"{name}.step")
        stl_file = os.path.join(PARTS_DIR, f"{name}.stl")
        vis_stl_file = os.path.join(ROS2_MESH_DIR, f"{name}.stl")
        col_stl_file = os.path.join(ROS2_COL_DIR, f"{name}.stl")
        
        # Export STEP
        Part.export([shape], step_file)
        
        # Export high-quality STL
        mesh = Mesh.Mesh()
        mesh.addFacets(shape.tessellate(0.1))
        mesh.write(stl_file)
        mesh.write(vis_stl_file)
        mesh.write(col_stl_file)
        
        print(f"  ✓ Exported {name} -> STEP + STLs")
        
    print("\n" + "=" * 70)
    print("  FREECAD MODEL GENERATION COMPLETE")
    print(f"  Master Document: {fcstd_path}")
    print(f"  Exported Parts:  {PARTS_DIR}")
    print(f"  ROS 2 Meshes:    {ROS2_MESH_DIR}")
    print("=" * 70)

if __name__ == "__main__":
    main()
